import models.ml.classifier as clf
from fastapi import FastAPI
from joblib import load
import gzip
from routes.v1.iris import app_iris_predict_v1
from routes.home import app_home
from config import model_file

app = FastAPI(title="Iris ML API",
              description="API for iris dataset ml model",
              version="1.0")


@app.on_event('startup')
async def load_model():
  clf.model = load(gzip.open(model_file, 'rb'))


app.include_router(app_home)
app.include_router(app_iris_predict_v1, prefix='/v1')
