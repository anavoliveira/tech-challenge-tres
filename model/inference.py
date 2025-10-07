import joblib
import json
import numpy as np
import os

try:
    import xgboost
except ModuleNotFoundError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "xgboost"])
    import xgboost


def model_fn(model_dir):
    model_path = os.path.join(model_dir, "multioutput_xgb.joblib")
    model = joblib.load(model_path)
    return model

def input_fn(request_body, request_content_type):
    # Supondo JSON com lista de features
    if request_content_type == "application/json":
        return np.array(json.loads(request_body))
    raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    return model.predict(input_data).tolist()

def output_fn(prediction, content_type):
    return json.dumps(prediction)
