from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel

model = joblib.load('logistic_model.joblib')
scaler = joblib.load('Scaler1.joblib')
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
    games_injured: int 
    award: int 
    highest_value: int 
    current_value_category_encoded: int
    


def preprocessing(input_features: InputFeatures):
    dict_f = {
                'appearance': input_features.appearance,
                'games_injured': input_features.games_injured,
                'award': input_features.award,
                'highest_value': input_features.highest_value,
                'current_value_category_encoded': input_features.current_value_category_encoded,
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

