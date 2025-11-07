"""
ML Predictions API Endpoints
Provides endpoints for making predictions using trained ML models.

Endpoints:
- POST /ml/predict - Single Kundali prediction
- POST /ml/predict-batch - Batch predictions

Author: ML Pipeline
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
import json
from pathlib import Path
import numpy as np
import pandas as pd

# Optional TensorFlow imports
try:
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except Exception as e:
    logger_temp = logging.getLogger(__name__)
    logger_temp.warning(f"TensorFlow not available: {str(e)}")
    TF_AVAILABLE = False

import joblib

from server.pydantic_schemas.api_response import APIResponse, success_response, error_response

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ML Predictions"])

# Model paths
MODELS_DIR = Path(__file__).parent.parent / "ml" / "trained_models"

# Load models on startup (only if TensorFlow is available)
nn_model = None
xgb_model = None
scaler = None
feature_names = []
target_names = []
MODELS_LOADED = False

if TF_AVAILABLE:
    try:
        logger.info("Loading trained models...")
        nn_model = keras.models.load_model(str(MODELS_DIR / "neural_network_model.h5"))
        xgb_model = joblib.load(str(MODELS_DIR / "xgboost_model.pkl"))
        scaler = joblib.load(str(MODELS_DIR / "scaler.pkl"))

        with open(MODELS_DIR / "feature_names.json") as f:
            feature_names = json.load(f)

        with open(MODELS_DIR / "target_names.json") as f:
            target_names = json.load(f)

        logger.info("Models loaded successfully")
        MODELS_LOADED = True

    except Exception as e:
        logger.warning(f"Could not load models: {str(e)}")
else:
    logger.warning("TensorFlow not available - ML predictions will not be functional")


class PredictionRequest(BaseModel):
    """Single prediction request with 200+ features."""
    features: List[float]
    use_ensemble: bool = True


class BatchPredictionRequest(BaseModel):
    """Batch prediction request."""
    records: List[List[float]]  # List of feature lists
    use_ensemble: bool = True


class PredictionResponse(BaseModel):
    """Prediction response."""
    career_potential: float
    wealth_potential: float
    marriage_happiness: float
    children_prospects: float
    health_status: float
    spiritual_inclination: float
    chart_strength: float
    life_ease_score: float
    model_type: str
    confidence: Optional[float] = None


def normalize_features(features: List[float]) -> np.ndarray:
    """
    Normalize features using fitted scaler.

    Args:
        features: List of raw feature values

    Returns:
        Normalized feature array
    """
    if scaler is None:
        raise ValueError("Scaler not loaded")

    return scaler.transform([features])


def make_prediction(features_normalized: np.ndarray, use_ensemble: bool = True) -> Dict:
    """
    Make prediction using trained models.

    Args:
        features_normalized: Normalized feature array
        use_ensemble: Whether to use ensemble (average NN and XGB)

    Returns:
        Dictionary with predictions
    """
    if not MODELS_LOADED:
        raise ValueError("Models not loaded")

    predictions = {}

    # Neural Network prediction
    if nn_model is not None:
        try:
            nn_pred = nn_model.predict(features_normalized, verbose=0)[0]
            predictions['neural_network'] = nn_pred
        except Exception as e:
            logger.error(f"NN prediction error: {str(e)}")
            raise

    # XGBoost prediction
    if xgb_model is not None:
        try:
            xgb_pred = xgb_model.predict(features_normalized)[0]
            predictions['xgboost'] = xgb_pred
        except Exception as e:
            logger.error(f"XGB prediction error: {str(e)}")
            raise

    # Ensemble prediction (average both models)
    if use_ensemble and len(predictions) == 2:
        ensemble_pred = (predictions['neural_network'] + predictions['xgboost']) / 2
        return {
            'predictions': ensemble_pred,
            'model_type': 'ensemble',
            'individual_predictions': {
                'neural_network': predictions['neural_network'].tolist(),
                'xgboost': predictions['xgboost'].tolist()
            }
        }
    elif 'neural_network' in predictions:
        return {
            'predictions': predictions['neural_network'],
            'model_type': 'neural_network',
            'individual_predictions': None
        }
    else:
        raise ValueError("No models available for prediction")


@router.post("/predict", response_model=APIResponse)
async def predict_single(request: PredictionRequest) -> APIResponse:
    """
    Make a single prediction using trained ML models.

    Args:
        request: Prediction request with 200+ features

    Returns:
        APIResponse with 8 predictions
    """
    try:
        if not MODELS_LOADED:
            return error_response(
                message="Models not loaded",
                detail="Trained models are not available",
                status_code=503
            )

        # Validate feature count
        if len(request.features) != len(feature_names):
            return error_response(
                message="Invalid feature count",
                detail=f"Expected {len(feature_names)} features, got {len(request.features)}",
                status_code=422
            )

        # Normalize features
        features_normalized = normalize_features(request.features)

        # Make prediction
        result = make_prediction(features_normalized, use_ensemble=request.use_ensemble)

        # Format response
        predictions = result['predictions']

        response_data = {
            'career_potential': float(predictions[0]),
            'wealth_potential': float(predictions[1]),
            'marriage_happiness': float(predictions[2]),
            'children_prospects': float(predictions[3]),
            'health_status': float(predictions[4]),
            'spiritual_inclination': float(predictions[5]),
            'chart_strength': float(predictions[6]),
            'life_ease_score': float(predictions[7]),
            'model_type': result['model_type'],
            'confidence': None,
            'individual_predictions': result.get('individual_predictions')
        }

        logger.info(f"Prediction successful - Model: {result['model_type']}")

        return success_response(
            data=response_data,
            message="Prediction completed successfully"
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return error_response(
            message="Validation error",
            detail=str(e),
            status_code=422
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return error_response(
            message="Error making prediction",
            detail=str(e),
            status_code=500
        )


@router.post("/predict-batch", response_model=APIResponse)
async def predict_batch(request: BatchPredictionRequest) -> APIResponse:
    """
    Make batch predictions for multiple records.

    Args:
        request: Batch prediction request

    Returns:
        APIResponse with list of predictions
    """
    try:
        if not MODELS_LOADED:
            return error_response(
                message="Models not loaded",
                detail="Trained models are not available",
                status_code=503
            )

        # Validate records
        if len(request.records) == 0:
            return error_response(
                message="Empty batch",
                detail="No records provided for prediction",
                status_code=422
            )

        # Validate feature count in first record
        if len(request.records[0]) != len(feature_names):
            return error_response(
                message="Invalid feature count",
                detail=f"Expected {len(feature_names)} features per record",
                status_code=422
            )

        batch_predictions = []

        logger.info(f"Processing batch of {len(request.records)} records...")

        for i, features in enumerate(request.records):
            try:
                # Normalize features
                features_normalized = normalize_features(features)

                # Make prediction
                result = make_prediction(features_normalized, use_ensemble=request.use_ensemble)
                predictions = result['predictions']

                # Format response
                prediction_dict = {
                    'record_id': i,
                    'career_potential': float(predictions[0]),
                    'wealth_potential': float(predictions[1]),
                    'marriage_happiness': float(predictions[2]),
                    'children_prospects': float(predictions[3]),
                    'health_status': float(predictions[4]),
                    'spiritual_inclination': float(predictions[5]),
                    'chart_strength': float(predictions[6]),
                    'life_ease_score': float(predictions[7]),
                    'model_type': result['model_type']
                }

                batch_predictions.append(prediction_dict)

            except Exception as e:
                logger.error(f"Error predicting record {i}: {str(e)}")
                batch_predictions.append({
                    'record_id': i,
                    'error': str(e)
                })

        logger.info(f"Batch prediction complete - {len(batch_predictions)} records processed")

        return success_response(
            data={
                'total_records': len(request.records),
                'successful_predictions': sum(1 for p in batch_predictions if 'error' not in p),
                'predictions': batch_predictions
            },
            message="Batch prediction completed"
        )

    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return error_response(
            message="Error in batch prediction",
            detail=str(e),
            status_code=500
        )


@router.get("/model-info", response_model=APIResponse)
async def get_model_info() -> APIResponse:
    """
    Get information about loaded models.

    Returns:
        APIResponse with model information
    """
    try:
        if not MODELS_LOADED:
            return error_response(
                message="Models not loaded",
                status_code=503
            )

        # Load metrics
        with open(MODELS_DIR / "model_metrics.json") as f:
            metrics = json.load(f)

        info = {
            'models_loaded': MODELS_LOADED,
            'available_models': ['neural_network', 'xgboost'],
            'input_features': len(feature_names),
            'output_targets': len(target_names),
            'target_variables': target_names,
            'metrics': metrics
        }

        return success_response(
            data=info,
            message="Model information retrieved successfully"
        )

    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return error_response(
            message="Error retrieving model information",
            detail=str(e),
            status_code=500
        )


@router.get("/health", response_model=APIResponse)
async def ml_health_check() -> APIResponse:
    """
    Check ML models health status.

    Returns:
        APIResponse with health status
    """
    health_status = {
        'models_loaded': MODELS_LOADED,
        'neural_network_loaded': nn_model is not None,
        'xgboost_loaded': xgb_model is not None,
        'scaler_loaded': scaler is not None,
        'status': 'healthy' if MODELS_LOADED else 'unhealthy'
    }

    return success_response(
        data=health_status,
        message="ML health check complete"
    )