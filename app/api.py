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


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "RaceCalc API"}


@app.get("/pace")
def pace_api(distance: float, time: float):
    if distance <= 0:
        raise HTTPException(status_code=400, detail="Distance must be greater than zero")
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
    context = {
        "request": request,
        "distance_options": ["5", "10", "21", "42"],  # przykład
        "other_data": some_safe_data  # upewnij się, że nie zawiera dict z dict
    }
    return templates.TemplateResponse("ui.html", context)
@app.get("/pace-ui")
def pace_ui(request: Request,
            distance_choice: str,
            custom_distance: float = 0,
            hours: int = 0,
            minutes: int = 0,
            seconds: int = 0):

    distance = resolve_distance(distance_choice, custom_distance)
    total_time = time_to_minutes(hours, minutes, seconds)

    pace = pace_from_time(distance, total_time)

    pace_str = minutes_to_time_str(pace)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": f"Pace: {pace_str} min/km"}
)

@app.get("/predict-ui")
def predict_ui(request: Request,
               distance_choice: str,
               custom_distance: float = 0,
               target: float = 10,
               hours: int = 0,
               minutes: int = 0,
               seconds: int = 0):

    distance = resolve_distance(distance_choice, custom_distance)
    total_time = time_to_minutes(hours, minutes, seconds)

    result = riegel_predict(distance, total_time, target)

    result_str = minutes_to_time_str(result)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": f"Predicted time: {result_str}"
        },
    )

def resolve_distance(choice, custom):
    if choice == "custom":
        return float(custom)
    return float(choice)