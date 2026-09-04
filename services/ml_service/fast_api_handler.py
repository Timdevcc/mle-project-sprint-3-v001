from sklearn.pipeline import Pipeline
import dill
import numpy as np
import pandas as pd
from typing import Dict
import sys

#для корректной работы pipeline, загруженного с помощью dill
sys.modules['__main__'].np = np

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
        except Exception as e:
            print(f"Failed to load model: {e}")

    def check_required_query_params(self, query_params: Dict) -> bool:
        if "user_id" not in query_params or "model_params" not in query_params:
            return False
        
        if not isinstance(query_params["user_id"], self.param_types["user_id"]):
            return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        return True

    def check_required_model_params(self, model_params: Dict) -> bool:
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False

    def validate_params(self, params: dict):
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
    
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True

    def price_predict(self, model_params):
        data = pd.DataFrame([model_params])
        return float(self.model.predict(data)[0])

    def handle(self, params: dict):
        try:
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = params["model_params"]
                user_id = params["user_id"]
                pred = self.price_predict(model_params)
                return {"user_id": user_id, "prediction": pred}
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response 
