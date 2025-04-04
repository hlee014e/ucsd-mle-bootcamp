import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.parameters import ParameterString, ParameterInteger
from sagemaker.workflow.steps import ProcessingStep, TuningStep
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.conditions import ConditionGreaterThan
from sagemaker.workflow.functions import JsonGet
from sagemaker.workflow.step_collections import RegisterModel
from sagemaker.workflow.properties import PropertyFile
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.inputs import TrainingInput
from sagemaker.model_metrics import MetricsSource, ModelMetrics
from sagemaker.estimator import Estimator
from sagemaker.tuner import HyperparameterTuner, ContinuousParameter, IntegerParameter
from sagemaker.network import NetworkConfig
from sagemaker.processing import ScriptProcessor
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.workflow.functions import Join

def get_pipeline(region, role, default_bucket, model_package_group_name="ChurnModelPackageGroup", 
                 pipeline_name="ChurnModelPipeline", sklearn_processor_version="0.23-1"):

    sagemaker_session = PipelineSession()

    processing_instance_type_param = ParameterString(name="ProcessingInstanceType", default_value="ml.t3.medium")
    processing_instance_count_param = ParameterInteger(name="ProcessingInstanceCount", default_value=1)
    training_instance_type_param = ParameterString(name="TrainingInstanceType", default_value="ml.t3.medium")
    input_data = ParameterString(name="InputData", default_value=f"s3://{default_bucket}/churn/churndata.csv")
    batch_data = ParameterString(name="BatchData", default_value=f"s3://{default_bucket}/data/batch/batch.csv")

    network_config = NetworkConfig(
        security_group_ids=["sg-0aad6fd2b7e2b0b8e", "sg-0a419771d915d0781"],
        subnets=["subnet-0e5b3c09a7803aec1"]
    )

    # Preprocessing step
    sklearn_processor = SKLearnProcessor(
        framework_version=sklearn_processor_version,
        instance_type="ml.t3.medium",
        instance_count=1,
        role=role,
        sagemaker_session=sagemaker_session,
        network_config=network_config
    )

    step_process = ProcessingStep(
        name="ChurnPreprocessing",
        step_args=sklearn_processor.run(
            inputs=[
                ProcessingInput(source=input_data.default_value, destination="/opt/ml/processing/input")
            ],
            outputs=[
                ProcessingOutput(output_name="train", source="/opt/ml/processing/train"),
                ProcessingOutput(output_name="validation", source="/opt/ml/processing/validation"),
                ProcessingOutput(output_name="test", source="/opt/ml/processing/test"),
            ],
            code="pipelines/customerchurn/Preprocess.py"
        )
    )

    image_uri = sagemaker.image_uris.retrieve("xgboost", region=region, version="1.0-1")

    xgb_estimator = Estimator(
        image_uri=image_uri,
        instance_type="ml.t3.medium",
        instance_count=1,
        hyperparameters={
            "eval_metric": "auc",
            "objective": "binary:logistic",
            "num_round": "100",
            "rate_drop": "0.3",
            "tweedie_variance_power": "1.4",
        },
        output_path=f"s3://{default_bucket}/output",
        base_job_name="churn-train",
        role=role,
        sagemaker_session=sagemaker_session,
        network_config=network_config
    )

    hpo_ranges = {
        "eta": ContinuousParameter(0, 1),
        "min_child_weight": ContinuousParameter(1, 10),
        "alpha": ContinuousParameter(0, 2),
        "max_depth": IntegerParameter(1, 10),
    }

    tuner = HyperparameterTuner(
        estimator=xgb_estimator,
        objective_metric_name="validation:auc",
        hyperparameter_ranges=hpo_ranges,
        max_jobs=10,
        max_parallel_jobs=2,
    )

    step_tuning = TuningStep(
        name="ChurnModelTuning",
        tuner=tuner,
        inputs={
            "train": TrainingInput(
                s3_data=step_process.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri,
                content_type="text/csv",
            ),
            "validation": TrainingInput(
                s3_data=step_process.properties.ProcessingOutputConfig.Outputs["validation"].S3Output.S3Uri,
                content_type="text/csv",
            ),
        },
    )

    script_eval = ScriptProcessor(
        image_uri=image_uri,
        command=["python3"],
        instance_type="ml.t3.medium",
        instance_count=1,
        role=role,
        sagemaker_session=sagemaker_session,
        network_config=network_config
    )

    evaluation_report = PropertyFile(
        name="EvaluationReport",
        output_name="evaluation",
        path="evaluation.json",
    )

    step_eval = ProcessingStep(
        name="EvaluateModel",
        step_args=script_eval.run(
            inputs=[
                ProcessingInput(
                    source=step_tuning.get_top_model_s3_uri(top_k=0, s3_bucket=default_bucket, prefix="output"),
                    destination="/opt/ml/processing/model"
                ),
                ProcessingInput(
                    source=step_process.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri,
                    destination="/opt/ml/processing/test"
                )
            ],
            outputs=[
                ProcessingOutput(output_name="evaluation", source="/opt/ml/processing/evaluation")
            ],
            code="pipelines/customerchurn/Evaluate.py"
        ),
        property_files=[evaluation_report],
    )

    model_metrics = ModelMetrics(
        model_statistics=MetricsSource(
            s3_uri=Join(
                on="/",
                values=[
                    step_eval.properties.ProcessingOutputConfig.Outputs["evaluation"].S3Output.S3Uri,
                    "evaluation.json"
                ]
            ),
            content_type="application/json",
        )
    )

    step_register = RegisterModel(
        name="RegisterChurnModel",
        estimator=xgb_estimator,
        model_data=step_tuning.get_top_model_s3_uri(top_k=0, s3_bucket=default_bucket, prefix="output"),
        content_types=["text/csv"],
        response_types=["text/csv"],
        inference_instances=["ml.t2.medium", "ml.m5.large"],
        transform_instances=["ml.m5.large"],
        model_package_group_name=model_package_group_name,
        model_metrics=model_metrics,
    )

    step_cond = ConditionStep(
        name="CheckAUCCondition",
        conditions=[
            ConditionGreaterThan(
                left=JsonGet(step_name="EvaluateModel", property_file="EvaluationReport", json_path="binary_classification_metrics.auc.value"),
                right=0.75,
            )
        ],
        if_steps=[step_register],
        else_steps=[],
    )

    pipeline = Pipeline(
        name=pipeline_name,
        parameters=[processing_instance_type_param, processing_instance_count_param, training_instance_type_param, input_data, batch_data],
        steps=[step_process, step_tuning, step_eval, step_cond],
        sagemaker_session=sagemaker_session,
    )

    return pipeline
