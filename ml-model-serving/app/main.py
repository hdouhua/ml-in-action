import gzip

from fastapi import FastAPI
from joblib import load

import app.models.ml.classifier as clf
from app.config import MODEL_FILE
from app.routes.home import app_home
from app.routes.v1.iris import app_iris_predict_v1

app = FastAPI(title="Iris ML API", description="API for iris dataset ml model", version="1.0")


@app.on_event('startup')
async def load_model():
    clf.model = load(gzip.open(MODEL_FILE, 'rb'))


app.include_router(app_home)
app.include_router(app_iris_predict_v1, prefix='/v1')
