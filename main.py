from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel

model = joblib.load('reg.joblib')
scaler = joblib.load('scaler.joblib')
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
    appearance: int
    highest_value: int 


def preprocessing(input_features: InputFeatures):
    dict_f = {
                'appearance': input_features.appearance,
                'highest_value': input_features.highest_value,
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

