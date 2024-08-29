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

# GET request for testing
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

def map_prediction_to_category(prediction):
    if prediction == 0:
        return "cheap price"
    elif prediction == 1:
        return "mid price"
    elif prediction == 2:
        return "high price"
    else:
        raise ValueError("Unexpected prediction value")

@app.post("/predict")
async def predict(input_features: InputFeatures):
    try:
        data = preprocessing(input_features)
        y_pred = model.predict(data)[0]  # Assuming model.predict returns a list-like structure
        category = map_prediction_to_category(y_pred)
        return {"sale_price_category": category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
