from fastapi import FastAPI
from app.pace import pace_from_time
from app.predictor import riegel_predict
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from app.pace import time_to_minutes, minutes_to_time_str

templates = Jinja2Templates(directory="templates")

some_safe_data = {"distance": 5, "time": "00:25:00", "unit": "km"}

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "RaceCalc API"}


@app.get("/pace")
def pace_api(distance: float, time: float):
    if distance <= 0:
        raise HTTPException(status_code=400, detail="Distance must be greater than zero")
    if time <= 0:  # ← DODAJ TĘ LINIĘ
        raise HTTPException(status_code=400, detail="Time must be greater than zero")
    pace = time / distance
    return {"pace": pace}

@app.get("/predict")
def predict(distance: float, time: float, target: float):
    if distance <= 0 or time <= 0 or target <= 0:
        raise HTTPException(status_code=400, detail="All values must be > 0")

    result = riegel_predict(distance, time, target)
    return {"predicted_time": result}

templates = Jinja2Templates(directory="templates")

@app.get("/ui")
async def ui(request: Request):
    some_safe_data = {"example": 123}  # jeśli potrzebujesz
    
    return templates.TemplateResponse(
    request,  # ← PIERWSZY ARGUMENT
    "ui.html",
    {"distance_options": ["5","10","21","42"], "other_data": some_safe_data}
)

from typing import Optional

@app.get("/pace-ui")
def pace_ui(request: Request,
            distance_choice: str = "",
            pace_custom_distance: Optional[float] = None,  # ← ZMIEŃ tutaj
            hours: int = 0,
            minutes: int = 0,
            seconds: int = 0):
    
    # Jeśli pace_custom_distance jest None, ustaw na 0
    custom_distance = pace_custom_distance if pace_custom_distance is not None else 0
    
    distance = resolve_distance(distance_choice, custom_distance)
    total_time = time_to_minutes(hours, minutes, seconds)
    
    if distance <= 0 or total_time <= 0:
        raise HTTPException(status_code=400, detail="Invalid distance or time")
    
    pace = pace_from_time(distance, total_time)
    pace_str = minutes_to_time_str(pace)
    
    return templates.TemplateResponse(
        request,
        "pace.html",
        {"result": pace_str}
    )

from app.predictor import riegel_predict  # ← Dodaj import

@app.get("/predict-ui")
def predict_ui(request: Request,
               distance_choice: str = "",
               predict_custom_distance: Optional[float] = None,
               target: float = 0,
               hours: int = 0,
               minutes: int = 0,
               seconds: int = 0):
    
    custom_distance = predict_custom_distance if predict_custom_distance is not None else 0
    
    distance = resolve_distance(distance_choice, custom_distance)
    total_time = time_to_minutes(hours, minutes, seconds)
    
    if distance <= 0 or total_time <= 0 or target <= 0:
        raise HTTPException(status_code=400, detail="Invalid distance or time")
    
    predicted_time = riegel_predict(distance, total_time, target)
    predicted_str = minutes_to_time_str(predicted_time)
    
    return templates.TemplateResponse(
        request,
        "predict.html",  # ← ZMIEŃ z index.html na predict.html
        {"result": predicted_str}
    )

def resolve_distance(choice, custom):
    if choice == "custom":
        return float(custom)
    return float(choice)