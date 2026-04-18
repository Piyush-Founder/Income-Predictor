from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os

model = joblib.load("xgboost_model.pkl")
columns = joblib.load("columns.pkl")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class InputData(BaseModel):
    age: int
    workclass: str
    fnlwgt: int
    education: str
    education_num: int
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/predict-page", response_class=HTMLResponse)
def predict_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.post("/predict")
def predict(data: InputData):
    try:
        input_dict = {
            "age": data.age,
            "workclass": data.workclass,
            "fnlwgt": data.fnlwgt,
            "education": data.education,
            "education.num": data.education_num,
            "marital.status": data.marital_status,
            "occupation": data.occupation,
            "relationship": data.relationship,
            "race": data.race,
            "sex": data.sex,
            "capital.gain": data.capital_gain,
            "capital.loss": data.capital_loss,
            "hours.per.week": data.hours_per_week,
            "native.country": data.native_country
        }

        input_df = pd.DataFrame([input_dict])
        input_df = pd.get_dummies(input_df, drop_first=True)
        input_df = input_df.reindex(columns=columns, fill_value=0)

        prediction = model.predict(input_df)[0]
        return {"prediction": int(prediction)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
