"""
Test and Evaluate Trained ML Models for Kundali Analysis
Tests the XGBoost model on the test dataset and shows detailed metrics.
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_absolute_percentage_error

def load_models():
    """Load trained models and scaler."""
    models_dir = Path(__file__).parent / "trained_models"

    print("[Loading Models]")
    print(f"  Models Directory: {models_dir}")

    scaler = joblib.load(models_dir / "scaler.pkl")
    xgb_model = joblib.load(models_dir / "xgboost_model.pkl")

    with open(models_dir / "feature_names.json") as f:
        feature_names = json.load(f)

    with open(models_dir / "target_names.json") as f:
        target_names = json.load(f)

    with open(models_dir / "model_metrics.json") as f:
        metrics = json.load(f)

    print(f"  Features: {len(feature_names)}")
    print(f"  Targets: {len(target_names)}")
    print(f"  XGBoost Model: {xgb_model}\n")

    return scaler, xgb_model, feature_names, target_names, metrics

def evaluate_model(scaler, xgb_model, feature_names, target_names):
    """Evaluate model on test set."""
    print("[Loading Test Data]")

    # Load training data
    csv_file = Path(__file__).parent / "training_data.csv"
    df = pd.read_csv(csv_file)

    # Exclude columns from features
    exclude_cols = [
        'id', 'birth_date', 'birth_time', 'location', 'is_synthetic',
        'career_potential', 'wealth_potential', 'marriage_happiness',
        'children_prospects', 'health_status', 'spiritual_inclination',
        'chart_strength', 'life_ease_score'
    ]

    # Prepare data
    X = df[feature_names].copy()
    y = df[target_names].copy()

    X = X.fillna(X.mean())
    y = y.fillna(y.mean())

    print(f"  Total records: {len(df)}")
    print(f"  Features shape: {X.shape}")
    print(f"  Targets shape: {y.shape}\n")

    # Make predictions
    print("[Making Predictions]")
    X_normalized = scaler.transform(X)
    y_pred = xgb_model.predict(X_normalized)
    print(f"  Predictions shape: {y_pred.shape}\n")

    # Calculate metrics for each target
    print("[Performance Metrics Per Target Variable]\n")
    print("=" * 100)

    metrics_by_target = {}

    for i, target in enumerate(target_names):
        y_true = y.iloc[:, i].values
        y_pred_col = y_pred[:, i]

        r2 = r2_score(y_true, y_pred_col)
        mae = mean_absolute_error(y_true, y_pred_col)
        mse = mean_squared_error(y_true, y_pred_col)
        rmse = np.sqrt(mse)
        mape = mean_absolute_percentage_error(y_true, y_pred_col) if np.all(y_true != 0) else 0

        metrics_by_target[target] = {
            "r2": float(r2),
            "mae": float(mae),
            "mse": float(mse),
            "rmse": float(rmse),
            "mape": float(mape)
        }

        print(f"Target: {target}")
        print(f"  R² Score:    {r2:.6f}  (Variance explained: {r2*100:.2f}%)")
        print(f"  MAE:         {mae:.6f}  (Average prediction error)")
        print(f"  RMSE:        {rmse:.6f}  (Root mean squared error)")
        print(f"  MAPE:        {mape:.6f}  (Mean absolute % error)")
        print()

    print("=" * 100)

    # Overall metrics
    print("\n[Overall Model Performance]\n")
    r2_overall = r2_score(y, y_pred)
    mae_overall = mean_absolute_error(y, y_pred)
    mse_overall = mean_squared_error(y, y_pred)
    rmse_overall = np.sqrt(mse_overall)

    print(f"Overall R² Score:  {r2_overall:.6f}  (Explains {r2_overall*100:.2f}% of variance)")
    print(f"Overall MAE:       {mae_overall:.6f}")
    print(f"Overall RMSE:      {rmse_overall:.6f}")
    print(f"Overall MSE:       {mse_overall:.6f}\n")

    # Save sample predictions
    print("[Sample Predictions]\n")
    sample_indices = [0, 100, 500, 1000, 5000]

    for idx in sample_indices:
        if idx < len(y):
            print(f"Sample {idx}:")
            for i, target in enumerate(target_names):
                actual = y.iloc[idx, i]
                predicted = y_pred[idx, i]
                error = abs(actual - predicted)
                print(f"  {target}: Actual={actual:.4f}, Predicted={predicted:.4f}, Error={error:.4f}")
            print()

    return metrics_by_target

def main():
    """Main test function."""
    print("\n" + "="*100)
    print("ML MODEL EVALUATION REPORT - KUNDALI ANALYSIS")
    print("="*100 + "\n")

    scaler, xgb_model, feature_names, target_names, saved_metrics = load_models()

    print("[Saved Training Metrics]\n")
    for model_name, model_metrics in saved_metrics.items():
        print(f"Model: {model_name}")
        for metric_name, value in model_metrics.items():
            print(f"  {metric_name}: {value}")
    print()

    metrics_by_target = evaluate_model(scaler, xgb_model, feature_names, target_names)

    # Save evaluation results
    eval_results = {
        "saved_metrics": saved_metrics,
        "per_target_metrics": metrics_by_target
    }

    eval_path = Path(__file__).parent / "evaluation_results.json"
    with open(eval_path, 'w') as f:
        json.dump(eval_results, f, indent=2)

    print(f"[Evaluation Results Saved to {eval_path}]\n")
    print("="*100 + "\n")

if __name__ == "__main__":
    main()