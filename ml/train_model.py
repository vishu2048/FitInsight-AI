
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "fitness_dataset.csv"

MODEL_DIR = BASE_DIR / "ml"
MODEL_PATH = MODEL_DIR / "weight_model.pkl"

FEATURES = [
    "weight",
    "steps",
    "sleep_duration",
    "workout_duration",
    "calories_burned",
    "calories_consumed",
    "water_intake",
]

TARGET = "future_weight"


def validate_dataset(dataframe):
    """Check dataset columns and numeric values."""

    required_columns = FEATURES + [TARGET]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Dataset is missing columns: "
            + ", ".join(missing_columns)
        )

    dataframe = dataframe[required_columns].copy()

    for column in required_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

    dataframe = dataframe.replace(
        [np.inf, -np.inf],
        np.nan,
    ).dropna()

    if len(dataframe) < 20:
        raise ValueError(
            "At least 20 complete rows are required "
            "for this training demonstration."
        )

    if (dataframe["weight"] <= 0).any():
        raise ValueError(
            "Weight values must be positive."
        )

    if (dataframe[TARGET] <= 0).any():
        raise ValueError(
            "Target weight values must be positive."
        )

    return dataframe


def train_model():
    print("=" * 50)
    print("FitInsight AI - Model Training")
    print("=" * 50)

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Create or provide data/fitness_dataset.csv first."
        )

    dataframe = pd.read_csv(DATA_PATH)
    dataframe = validate_dataset(dataframe)

    print(f"Usable rows: {len(dataframe)}")

    X = dataframe[FEATURES]
    y = dataframe[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        min_samples_leaf=2,
        n_jobs=-1,
    )

    print("Training Random Forest Regression...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )
    r2 = r2_score(y_test, predictions)

    print("\nEvaluation on held-out test data")
    print("-" * 40)
    print(f"MAE  : {mae:.4f} kg")
    print(f"RMSE : {rmse:.4f} kg")
    print(f"R²   : {r2:.4f}")

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_bundle = {
        "model": model,
        "features": FEATURES,
        "target": TARGET,
        "metrics": {
            "mae": float(mae),
            "rmse": float(rmse),
            "r2": float(r2),
        },
        "training_rows": int(len(X_train)),
        "testing_rows": int(len(X_test)),
    }

    joblib.dump(
        model_bundle,
        MODEL_PATH,
    )

    print(f"\nModel saved to: {MODEL_PATH}")
    print("Training completed successfully.")


if __name__ == "__main__":
    try:
        train_model()
    except Exception as error:
        print(f"\nTraining failed: {error}")
        raise
