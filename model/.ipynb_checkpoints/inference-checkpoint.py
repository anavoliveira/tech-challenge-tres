import joblib
import json
import numpy as np
import pandas as pd

def model_fn(model_dir):
    return joblib.load(f"{model_dir}/model_temp.pkl")

def input_fn(request_body, request_content_type):
    if request_content_type == "application/json":
        data = pd.DataFrame(json.loads(request_body))
        return data
    raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    preds = model.predict(input_data)
    return preds.tolist()

def output_fn(prediction, content_type):
    if content_type == "application/json":
        return json.dumps(prediction)
    raise ValueError(f"Unsupported content type: {content_type}")
