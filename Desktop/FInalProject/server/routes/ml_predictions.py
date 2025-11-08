"""
ML Predictions API Endpoints
Provides endpoints for making predictions using trained ML models.

Endpoints:
- POST /ml/predict - Single prediction with 53 features
- POST /ml/predict-from-kundali - Generate Kundali, extract features, and predict
- POST /ml/predict-batch - Batch predictions
- GET /ml/test-scenarios - Test model on 3 predefined scenarios
- GET /ml/model-info - Model information
- GET /ml/health - Health check

Author: ML Pipeline
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import logging
import json
from pathlib import Path
import numpy as np
import pandas as pd

import joblib

from server.pydantic_schemas.api_response import APIResponse, success_response, error_response
from server.pydantic_schemas.kundali_schema import KundaliRequest
from server.ml.feature_extractor import KundaliFeatureExtractor
from server.services.logic import generate_kundali_logic

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ML Predictions"])

# Model paths
MODELS_DIR = Path(__file__).parent.parent / "ml" / "trained_models"

# Load models on startup
xgb_model = None
scaler = None
feature_names = []
target_names = []
feature_extractor = None
MODELS_LOADED = False

try:
    logger.info("Loading trained ML models...")
    xgb_model = joblib.load(str(MODELS_DIR / "xgboost_model.pkl"))
    scaler = joblib.load(str(MODELS_DIR / "scaler.pkl"))

    with open(MODELS_DIR / "feature_names.json") as f:
        feature_names = json.load(f)

    with open(MODELS_DIR / "target_names.json") as f:
        target_names = json.load(f)

    feature_extractor = KundaliFeatureExtractor()

    logger.info(f"Models loaded successfully - {len(feature_names)} features, {len(target_names)} targets")
    MODELS_LOADED = True

except Exception as e:
    logger.error(f"Could not load models: {str(e)}")
    MODELS_LOADED = False


class PredictionRequest(BaseModel):
    """Single prediction request with 53 features."""
    features: Dict[str, float]  # Feature dictionary


class FeaturesListRequest(BaseModel):
    """Prediction request with features as list."""
    features: List[float]


class BatchPredictionRequest(BaseModel):
    """Batch prediction request."""
    records: List[List[float]]  # List of feature lists


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
    average_score: float
    interpretation: str
    model_type: str = "xgboost"


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


def make_prediction(features_normalized: np.ndarray) -> Dict:
    """
    Make prediction using XGBoost model.

    Args:
        features_normalized: Normalized feature array

    Returns:
        Dictionary with predictions
    """
    if not MODELS_LOADED or xgb_model is None:
        raise ValueError("Models not loaded")

    try:
        xgb_pred = xgb_model.predict(features_normalized)[0]
        return {
            'predictions': xgb_pred,
            'model_type': 'xgboost'
        }
    except Exception as e:
        logger.error(f"XGBoost prediction error: {str(e)}")
        raise


def interpret_prediction(predictions: np.ndarray) -> str:
    """
    Interpret prediction as human-readable text.

    Args:
        predictions: Array of 8 prediction values

    Returns:
        Interpretation string
    """
    avg_score = float(np.mean(predictions))

    if avg_score >= 80:
        return "This chart indicates a very fortunate life with excellent prospects across all areas."
    elif avg_score >= 70:
        return "This chart shows good overall potential with balanced opportunities and challenges."
    elif avg_score >= 60:
        return "This chart indicates average potential with some strengths to leverage and some areas to work on."
    elif avg_score >= 50:
        return "This chart shows mixed results - will need effort to overcome challenges and maximize potential."
    else:
        return "This chart indicates significant challenges ahead - strong will and spiritual growth recommended."


def interpret_target_value(target_name: str, value: float) -> str:
    """Interpret individual target value."""
    if value < 30:
        return "POOR"
    elif value < 50:
        return "BELOW AVERAGE"
    elif value < 70:
        return "AVERAGE"
    elif value < 85:
        return "GOOD"
    else:
        return "EXCELLENT"


@router.post("/predict", response_model=APIResponse)
async def predict_from_features(request: FeaturesListRequest) -> APIResponse:
    """
    Make a prediction from a list of 53 features.

    Args:
        request: Prediction request with 53 features as a list

    Returns:
        APIResponse with 8 life outcome predictions
    """
    try:
        if not MODELS_LOADED:
            return error_response(
                code="MODELS_NOT_LOADED",
                message="Models not loaded"
            )

        # Validate feature count
        if len(request.features) != len(feature_names):
            return error_response(
                code="INVALID_FEATURE_COUNT",
                message=f"Invalid feature count: expected {len(feature_names)}, got {len(request.features)}"
            )

        # Normalize features
        features_normalized = normalize_features(request.features)

        # Make prediction
        result = make_prediction(features_normalized)
        predictions = result['predictions']

        # Interpret predictions
        avg_score = float(np.mean(predictions))
        interpretation = interpret_prediction(predictions)

        response_data = {
            'career_potential': float(predictions[0]),
            'wealth_potential': float(predictions[1]),
            'marriage_happiness': float(predictions[2]),
            'children_prospects': float(predictions[3]),
            'health_status': float(predictions[4]),
            'spiritual_inclination': float(predictions[5]),
            'chart_strength': float(predictions[6]),
            'life_ease_score': float(predictions[7]),
            'average_score': avg_score,
            'interpretation': interpretation,
            'model_type': result['model_type']
        }

        logger.info(f"Prediction successful - Average score: {avg_score:.2f}")

        return success_response(
            data=response_data,
            message="Prediction completed successfully"
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return error_response(
            code="VALIDATION_ERROR",
            message="Validation error",
            details={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return error_response(
            code="PREDICTION_ERROR",
            message="Error making prediction",
            details={"error": str(e)}
        )


@router.post("/predict-from-kundali", response_model=APIResponse)
async def predict_from_kundali(request: KundaliRequest) -> APIResponse:
    """
    Generate Kundali, extract features, and make predictions.

    This endpoint:
    1. Takes birth details
    2. Generates complete Kundali
    3. Extracts 53 ML features
    4. Makes predictions for 8 life outcomes

    Args:
        request: Birth details (date, time, location, timezone)

    Returns:
        APIResponse with Kundali and predictions
    """
    try:
        if not MODELS_LOADED:
            return error_response(
                code="MODELS_NOT_LOADED",
                message="Models not loaded"
            )

        # Generate Kundali
        logger.info(f"Generating Kundali for: {request.birthDate} {request.birthTime}")
        kundali = await generate_kundali_logic(request)
        kundali_dict = kundali.model_dump(exclude_none=True)

        # Extract features
        logger.info("Extracting ML features from Kundali...")
        features_dict, missing = feature_extractor.extract_features(kundali_dict)

        if missing:
            logger.warning(f"Missing {len(missing)} features: {missing}")

        # Validate features
        is_valid, issues = feature_extractor.validate_features(features_dict)
        if not is_valid:
            logger.warning(f"Feature validation issues: {issues}")

        # Convert dict to ordered list
        features_list = [features_dict.get(name, 0.0) for name in feature_names]

        # Normalize
        features_normalized = normalize_features(features_list)

        # Predict
        result = make_prediction(features_normalized)
        predictions = result['predictions']

        # Interpret
        avg_score = float(np.mean(predictions))
        interpretation = interpret_prediction(predictions)

        response_data = {
            'kundali': kundali_dict,
            'features_extracted': len(features_dict),
            'features_missing': len(missing),
            'predictions': {
                'career_potential': float(predictions[0]),
                'wealth_potential': float(predictions[1]),
                'marriage_happiness': float(predictions[2]),
                'children_prospects': float(predictions[3]),
                'health_status': float(predictions[4]),
                'spiritual_inclination': float(predictions[5]),
                'chart_strength': float(predictions[6]),
                'life_ease_score': float(predictions[7]),
                'average_score': avg_score,
                'interpretation': interpretation
            },
            'model_type': result['model_type']
        }

        logger.info(f"Kundali prediction successful - Average score: {avg_score:.2f}")

        return success_response(
            data=response_data,
            message="Kundali generated and predictions completed successfully"
        )

    except Exception as e:
        logger.error(f"Error in Kundali prediction: {str(e)}", exc_info=True)
        return error_response(
            code="KUNDALI_PREDICTION_ERROR",
            message="Error in Kundali prediction",
            details={"error": str(e)}
        )


@router.post("/predict-batch", response_model=APIResponse)
async def predict_batch(request: BatchPredictionRequest) -> APIResponse:
    """
    Make batch predictions for multiple records.

    Args:
        request: Batch prediction request with list of feature lists

    Returns:
        APIResponse with list of predictions
    """
    try:
        if not MODELS_LOADED:
            return error_response(
                code="MODELS_NOT_LOADED",
                message="Models not loaded"
            )

        # Validate records
        if len(request.records) == 0:
            return error_response(
                code="EMPTY_BATCH",
                message="Empty batch: No records provided for prediction"
            )

        # Validate feature count in first record
        if len(request.records[0]) != len(feature_names):
            return error_response(
                code="INVALID_FEATURE_COUNT",
                message=f"Invalid feature count: expected {len(feature_names)} features per record"
            )

        batch_predictions = []

        logger.info(f"Processing batch of {len(request.records)} records...")

        for i, features in enumerate(request.records):
            try:
                # Normalize features
                features_normalized = normalize_features(features)

                # Make prediction
                result = make_prediction(features_normalized)
                predictions = result['predictions']

                # Interpret
                avg_score = float(np.mean(predictions))

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
                    'average_score': avg_score,
                    'model_type': result['model_type']
                }

                batch_predictions.append(prediction_dict)

            except Exception as e:
                logger.error(f"Error predicting record {i}: {str(e)}")
                batch_predictions.append({
                    'record_id': i,
                    'error': str(e)
                })

        successful = sum(1 for p in batch_predictions if 'error' not in p)
        logger.info(f"Batch prediction complete - {successful}/{len(batch_predictions)} successful")

        return success_response(
            data={
                'total_records': len(request.records),
                'successful_predictions': successful,
                'predictions': batch_predictions
            },
            message="Batch prediction completed"
        )

    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return error_response(
            code="BATCH_PREDICTION_ERROR",
            message="Error in batch prediction",
            details={"error": str(e)}
        )


@router.get("/test-scenarios", response_model=APIResponse)
async def test_scenarios() -> APIResponse:
    """
    Test the model on 3 predefined chart scenarios:
    1. Strong Chart (Well-Aspected, Multiple Yogas)
    2. Weak Chart (Afflicted, Few Yogas)
    3. Average Chart (Balanced)

    This demonstrates model behavior across chart quality spectrum.

    Returns:
        APIResponse with test results
    """
    try:
        if not MODELS_LOADED:
            return error_response(
                code="MODELS_NOT_LOADED",
                message="Models not loaded"
            )

        test_scenarios = {}

        # Strong Chart
        logger.info("Testing strong chart scenario...")
        strong_features = {
            'sun_degree': 45, 'moon_degree': 120, 'mercury_degree': 50, 'venus_degree': 60,
            'mars_degree': 200, 'jupiter_degree': 90, 'saturn_degree': 150, 'rahu_degree': 30,
            'ketu_degree': 210, 'ascendant_degree': 0,
        }
        for h in range(1, 13):
            strong_features[f'house_{h}_planets'] = min(2, np.random.randint(1, 3))
            strong_features[f'house_{h}_lord_strength'] = float(np.random.uniform(70, 95))
        for planet in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'rahu', 'ketu']:
            strong_features[f'{planet}_strength'] = float(np.random.uniform(70, 95))
        strong_features['total_yoga_count'] = 6
        strong_features['benefic_yoga_count'] = 5
        strong_features['malefic_yoga_count'] = 1
        strong_features['neutral_yoga_count'] = 0
        for i in range(1, 7):
            strong_features[f'aspect_strength_{i}'] = float(np.random.uniform(60, 90))

        strong_list = [strong_features.get(name, 0.0) for name in feature_names]
        strong_norm = normalize_features(strong_list)
        strong_pred = make_prediction(strong_norm)['predictions']
        strong_avg = float(np.mean(strong_pred))

        test_scenarios['strong_chart'] = {
            'name': 'Strong Chart (Well-Aspected, Multiple Yogas)',
            'predictions': {
                'career_potential': float(strong_pred[0]),
                'wealth_potential': float(strong_pred[1]),
                'marriage_happiness': float(strong_pred[2]),
                'children_prospects': float(strong_pred[3]),
                'health_status': float(strong_pred[4]),
                'spiritual_inclination': float(strong_pred[5]),
                'chart_strength': float(strong_pred[6]),
                'life_ease_score': float(strong_pred[7]),
            },
            'average_score': strong_avg,
            'interpretation': interpret_prediction(strong_pred)
        }

        # Weak Chart
        logger.info("Testing weak chart scenario...")
        weak_features = {}
        for key in strong_features.keys():
            if '_degree' in key:
                weak_features[key] = (strong_features[key] + 180) % 360
            elif '_planets' in key:
                weak_features[key] = 0
            elif '_lord_strength' in key or '_strength' in key:
                weak_features[key] = float(np.random.uniform(20, 40))
            elif '_yoga_count' in key:
                weak_features[key] = 0 if 'benefic' in key else (1 if 'malefic' in key else 1)
            elif 'aspect_strength' in key:
                weak_features[key] = float(np.random.uniform(10, 30))

        weak_list = [weak_features.get(name, 0.0) for name in feature_names]
        weak_norm = normalize_features(weak_list)
        weak_pred = make_prediction(weak_norm)['predictions']
        weak_avg = float(np.mean(weak_pred))

        test_scenarios['weak_chart'] = {
            'name': 'Weak Chart (Afflicted, Few Yogas)',
            'predictions': {
                'career_potential': float(weak_pred[0]),
                'wealth_potential': float(weak_pred[1]),
                'marriage_happiness': float(weak_pred[2]),
                'children_prospects': float(weak_pred[3]),
                'health_status': float(weak_pred[4]),
                'spiritual_inclination': float(weak_pred[5]),
                'chart_strength': float(weak_pred[6]),
                'life_ease_score': float(weak_pred[7]),
            },
            'average_score': weak_avg,
            'interpretation': interpret_prediction(weak_pred)
        }

        # Average Chart
        logger.info("Testing average chart scenario...")
        avg_features = {}
        for key in strong_features.keys():
            if '_degree' in key:
                avg_features[key] = float(np.random.uniform(0, 360))
            elif '_planets' in key:
                avg_features[key] = float(np.random.randint(0, 2))
            elif '_lord_strength' in key or '_strength' in key:
                avg_features[key] = float(np.random.uniform(45, 65))
            elif '_yoga_count' in key:
                if 'total' in key:
                    avg_features[key] = 3
                elif 'benefic' in key:
                    avg_features[key] = 2
                elif 'malefic' in key:
                    avg_features[key] = 1
                else:
                    avg_features[key] = 0
            elif 'aspect_strength' in key:
                avg_features[key] = float(np.random.uniform(40, 60))

        avg_list = [avg_features.get(name, 0.0) for name in feature_names]
        avg_norm = normalize_features(avg_list)
        avg_pred = make_prediction(avg_norm)['predictions']
        avg_avg = float(np.mean(avg_pred))

        test_scenarios['average_chart'] = {
            'name': 'Average Chart (Balanced)',
            'predictions': {
                'career_potential': float(avg_pred[0]),
                'wealth_potential': float(avg_pred[1]),
                'marriage_happiness': float(avg_pred[2]),
                'children_prospects': float(avg_pred[3]),
                'health_status': float(avg_pred[4]),
                'spiritual_inclination': float(avg_pred[5]),
                'chart_strength': float(avg_pred[6]),
                'life_ease_score': float(avg_pred[7]),
            },
            'average_score': avg_avg,
            'interpretation': interpret_prediction(avg_pred)
        }

        logger.info(f"Test scenarios complete - Strong: {strong_avg:.1f}, Weak: {weak_avg:.1f}, Avg: {avg_avg:.1f}")

        return success_response(
            data=test_scenarios,
            message="Test scenarios completed successfully"
        )

    except Exception as e:
        logger.error(f"Test scenario error: {str(e)}", exc_info=True)
        return error_response(
            code="TEST_SCENARIO_ERROR",
            message="Error running test scenarios",
            details={"error": str(e)}
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
                code="MODELS_NOT_LOADED",
                message="Models not loaded"
            )

        # Load metrics
        with open(MODELS_DIR / "model_metrics.json") as f:
            metrics = json.load(f)

        info = {
            'models_loaded': MODELS_LOADED,
            'available_models': ['neural_network', 'xgboost'],
            'input_features': len(feature_names),
            'output_targets': len(target_names),
            'target_names': target_names,
            'metrics': metrics
        }

        return success_response(
            data=info,
            message="Model information retrieved successfully"
        )

    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return error_response(
            code="MODEL_INFO_ERROR",
            message="Error retrieving model information",
            details={"error": str(e)}
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