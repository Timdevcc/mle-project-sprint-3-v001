from fastapi import FastAPI, Body
from ml_service.fast_api_handler import FastApiHandler
from typing import Dict
import numpy as np
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Counter

app = FastAPI()
app.handler = FastApiHandler()
instrumentator = Instrumentator()

instrumentator.instrument(app).expose(app)

main_app_predictions = Histogram(
    "main_app_predictions",
    "Histogram of predictions",
    buckets=(2, 4, 6, 8, 10, 13, 16, 20, 25, 30, 40, 60)
)

main_app_predictions_counter = Counter(
    "main_app_predictions_counter",
    "count of predictions"
)

example_apartment = {
    "floor": 7,
    "kitchen_area": 10.5,
    "living_area": 32.0,
    "rooms": 2,
    "is_apartment": False,
    "total_area": 54.2,
    "build_year": 2005,
    "building_type_int": 4,
    "latitude": 55.751244,
    "longitude": 37.618423,
    "ceiling_height": 2.7,
    "flats_count": 180,
    "floors_total": 14,
    "has_elevator": True
}


@app.post("/api/apartments/predict-price")
def make_prediction(user_id: int,
                    model_params: Dict = Body(..., openapi_examples={"default": {"summary": "Пример квартиры", "value": example_apartment}})):
    all_params = {"user_id": user_id, "model_params": model_params}
    user_pred = app.handler.handle(all_params)
    main_app_predictions.observe(float(user_pred['prediction']) / 1_000_000)
    main_app_predictions_counter.inc()
    return user_pred