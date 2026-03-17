from fastapi import FastAPI
from app.pace import pace_from_time
from app.predictor import riegel_predict

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "RaceCalc API"}


@app.get("/pace")
def get_pace(distance: float, time: float):
    pace = pace_from_time(distance, time)
    return {"pace": pace}


@app.get("/predict")
def predict(distance: float, time: float, target: float):
    result = riegel_predict(distance, time, target)
    return {"predicted_time": result}