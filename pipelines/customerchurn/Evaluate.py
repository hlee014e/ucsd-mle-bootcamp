import os
import json
import pathlib
import tarfile
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score

if __name__ == "__main__":

    base_dir = "/opt/ml/processing"

    model_path = os.path.join(base_dir, "model", "model.tar.gz")
    with tarfile.open(model_path) as tar:
        tar.extractall(path=".")

    model = pickle.load(open("xgboost-model", "rb"))

    test_path = os.path.join(base_dir, "test", "test.csv")
    df = pd.read_csv(test_path, header=None)
    y_true = df.iloc[:, 0].astype(int).to_numpy()
    X_test = df.iloc[:, 1:]

    y_pred = model.predict_proba(X_test)[:, 1]
    auc_score = roc_auc_score(y_true, y_pred)

    report_dict = {
        "binary_classification_metrics": {
            "auc": {
                "value": auc_score
            }
        }
    }

    output_dir = os.path.join(base_dir, "evaluation")
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(output_dir, "evaluation.json"), "w") as f:
        json.dump(report_dict, f)

