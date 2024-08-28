from fastapi import FastAPI, HTTPException
import requests
import joblib
from pydantic import BaseModel

model = joblib.load('Log_Reg.joblib')
scaler = joblib.load('Scaler.joblib')
app = FastAPI()

# GET request
@app.get("/")

def read_root():
    return {"message": "Welcome to Tuwaiq Academy"}
# get request

@app.get("/try/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

class InputFeatures(BaseModel):
    Engine_Size: float
    Mileage: float


def preprocessing(input_features: InputFeatures):
    dict_f = {
                'Engine_Size': input_features.Engine_Size,
                'Mileage': input_features.Mileage,
}
    feature_list = [dict_f[key] for key in sorted(dict_f)]
    return scaler.transform([list(dict_f.values())])

@app.get("/predict")
def predict(input_features: InputFeatures):
    return preprocessing(input_features)


@app.post("/predict")
async def predict(input_features: InputFeatures):
    data = preprocessing(input_features)
    y_pred = model.predict(data)
    return {"pred": y_pred.tolist()[0]}

