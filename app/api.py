from fastapi import FastAPI
from app.pace import pace_from_time
from app.predictor import riegel_predict
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

templates = Jinja2Templates(directory="templates")


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "RaceCalc API"}


@app.get("/pace")
def get_pace(distance: float, time: float):
    if distance <= 0:
        raise HTTPException(status_code=400, detail="Distance must be > 0")

    if time <= 0:
        raise HTTPException(status_code=400, detail="Time must be > 0")

    pace = pace_from_time(distance, time)
    return {"pace": pace}

@app.get("/predict")
def predict(distance: float, time: float, target: float):
    if distance <= 0 or time <= 0 or target <= 0:
        raise HTTPException(status_code=400, detail="All values must be > 0")

    result = riegel_predict(distance, time, target)
    return {"predicted_time": result}

@app.get("/ui")
def ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/pace-ui")
def pace_ui(request: Request, distance: float, time: float):
    pace = pace_from_time(distance, time)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": f"Pace: {pace:.2f} min/km"
        },
    )


@app.get("/predict-ui")
def predict_ui(request: Request, distance: float, time: float, target: float):
    result = riegel_predict(distance, time, target)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": f"Predicted time: {result:.2f} min"
        },
    )