from sklearn.pipeline import Pipeline
import dill
import numpy as np
import pandas as pd
from typing import Dict
import sys
import logging
from fastapi import HTTPException

#для корректной работы pipeline, загруженного с помощью dill
sys.modules['__main__'].np = np

logger = logging.getLogger(__name__)
class FastApiHandler:
    def __init__(self):
        self.param_types = {
            "user_id": int,
            "model_params": Dict
        }

        self.model_path = "./models/model.pkl"
        self.load_model(model_path=self.model_path)
        self.required_model_params = ["floor",
                                    "kitchen_area",
                                    "living_area",
                                    "rooms",
                                    "is_apartment",
                                    "total_area",
                                    "build_year",
                                    "building_type_int",
                                    "latitude",
                                    "longitude",
                                    "ceiling_height",
                                    "flats_count",
                                    "floors_total",
                                    "has_elevator"]

    def load_model(self, model_path):
        try:
            with open(model_path, 'rb') as f:
                self.model = dill.load(f)
            if self.model is None:
                raise ValueError("Loaded model object is None")
            logger.info("Model successfully loaded from %s", model_path)
        except Exception as e:
            logger.critical("Critical error: Failed to load model from %s: %s", model_path, e)
            raise RuntimeError(f"Cannot start service without model: {e}") from e

    def check_required_query_params(self, query_params: Dict) -> bool:
        if "user_id" not in query_params or "model_params" not in query_params:
            return False
        
        if not isinstance(query_params["user_id"], self.param_types["user_id"]):
            return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        return True

    def check_required_model_params(self, model_params: Dict) -> bool:
        missing_keys = set(self.required_model_params) - set(model_params.keys())
        if missing_keys:
            logger.warning("Missing required model parameters: %s", missing_keys)
            return False
        return True

    def validate_params(self, params: dict):
        if not self.check_required_query_params(params):
            logger.warning("Not all query params exist or type mismatch")
            return False

        if not self.check_required_model_params(params["model_params"]):
            logger.warning("Not all model params exist")
            return False

        logger.info("All parameters successfully validated")
        return True

    def price_predict(self, model_params):
        ordered_features = {param: model_params[param] for param in self.required_model_params}
        data = pd.DataFrame([ordered_features])
        return float(self.model.predict(data)[0])

    def handle(self, params: dict):
        if not self.validate_params(params):
            logger.warning("Error while handling request")
            raise HTTPException(
                status_code=400,
                detail="Request validation failed: check required fields and types."
            )
        try:
            user_id = params["user_id"]
            model_params = params["model_params"]
            pred = self.price_predict(model_params)
            return {
                "user_id": user_id,
                "prediction": pred
            }
        except Exception as e:
            logger.exception("Unexpected error during model inference: %s", e)
            raise HTTPException(
                status_code=500,
                detail="Internal model execution error."
            )
