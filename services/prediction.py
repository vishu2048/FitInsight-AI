
from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "weight_model.pkl"


def load_model_bundle():
    """Load the trained model and its metadata."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found.\n"
            "Train it first using:\n"
            "python ml/train_model.py"
        )

    bundle = joblib.load(MODEL_PATH)

    # Support both the newer model bundle and the older
    # plain RandomForestRegressor file.
    if isinstance(bundle, dict) and "model" in bundle:
        model = bundle["model"]
        features = bundle.get(
            "features",
            [
                "weight",
                "steps",
                "sleep_duration",
                "workout_duration",
                "calories_burned",
                "calories_consumed",
                "water_intake",
            ],
        )
        metrics = bundle.get("metrics", {})
    else:
        model = bundle
        features = [
            "weight",
            "steps",
            "sleep_duration",
            "workout_duration",
            "calories_burned",
            "calories_consumed",
            "water_intake",
        ]
        metrics = {}

    return model, features, metrics


def predict_weight(
    weight,
    steps,
    sleep_duration,
    workout_duration,
    calories_burned,
    calories_consumed,
    water_intake,
):
    """Predict weight using the saved local ML model."""

    model, features, _ = load_model_bundle()

    input_data = {
        "weight": weight,
        "steps": steps,
        "sleep_duration": sleep_duration,
        "workout_duration": workout_duration,
        "calories_burned": calories_burned,
        "calories_consumed": calories_consumed,
        "water_intake": water_intake,
    }

    dataframe = pd.DataFrame([input_data])

    # Preserve the feature order used during training.
    dataframe = dataframe[features]

    prediction = model.predict(dataframe)

    return float(prediction[0])


def get_model_metrics():
    """Return evaluation metrics, if stored in the model bundle."""

    _, _, metrics = load_model_bundle()
    return metrics
