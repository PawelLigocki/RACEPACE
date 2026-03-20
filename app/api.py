from fastapi import FastAPI
from app.pace import pace_from_time
from app.predictor import riegel_predict
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse


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

@app.get("/ui")
def ui(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

from fastapi.responses import JSONResponse, HTMLResponse

@app.get("/pace-ui")
def pace_ui(request: Request, distance: float = None, time: float = None):
    if distance is not None and time is not None:
        pace = time / distance
        content = f"""
        <html>
            <body>
                <h1>Pace</h1>
                <p>Pace: {pace}</p>
            </body>
        </html>
        """
        return HTMLResponse(content=content)

    return templates.TemplateResponse(request, "index.html", {})

@app.get("/predict-ui")
def predict_ui(request: Request, distance: float, time: float, target: float):
    result = riegel_predict(distance, time, target)

    return templates.TemplateResponse(
    request,
    "index.html",
    {
        "result": f"Predicted time: {result:.2f} min"
    },
)