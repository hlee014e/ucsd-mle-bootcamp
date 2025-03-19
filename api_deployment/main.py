import pickle
import numpy as np
import xgboost as xgb
from fastapi import FastAPI
from pydantic import BaseModel
from preprocess import  clean_preprocess, clean_text, extract_date, extract_source
import joblib

# ✅ Load the trained XGBoost model
model = joblib.load("log_reg_model.pkl")

# Initialize FastAPI app
app = FastAPI()



# Define input data model using Pydantic
class TextInput(BaseModel):
    text: str
    date_source_text: str  # 
    name_text: str  # 

@app.post("/predict")
def predict(input_data: TextInput):
    try:
        # clean and preprocess
        preprocessed_single_data = clean_preprocess(input_data.text,input_data.date_source_text,input_data.name_text)

        # Make a prediction
        prediction = model.predict(preprocessed_single_data)

        prediction_dict ={0:'True',1:'Mostly True',2:'Half True',3:'MOstly False', 4:'False',5:'Full Flop',6:'Pant on Fire'}
 

        # Convert prediction to list to be JSON serializable
        prediction_list = prediction_dict[prediction[0]]


        return {
            "prediction": prediction_list,
        }
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}
