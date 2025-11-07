# ML Implementation Guide - Complete Kundali Analysis

**Date:** November 8, 2025
**Status:** Ready for Implementation
**Level:** Step-by-Step Instructions

---

## 📋 QUICK START GUIDE

### Step 1: Install Required Dependencies

```bash
pip install requests pandas numpy scikit-learn tensorflow keras
pip install matplotlib seaborn plotly jupyter
pip install xgboost lightgbm
```

### Step 2: Generate Synthetic Data (Script Ready)

**File:** `server/ml/synthetic_data_generator.py`

```bash
cd server/ml

# Generate 10,000 synthetic records
python synthetic_data_generator.py

# Output: training_data.csv (200+ features, 8 targets)
```

### Step 3: Validate Dataset Quality

Create `server/ml/data_validator.py` with the validation code

```bash
python data_validator.py

# Output: validation_report.json
```

### Step 4: Split Data for Training

```bash
# 70% training, 15% validation, 15% test
python -c "
import pandas as pd
df = pd.read_csv('training_data.csv')
n = len(df)

train = df.iloc[:int(0.7*n)]
val = df.iloc[int(0.7*n):int(0.85*n)]
test = df.iloc[int(0.85*n):]

train.to_csv('train_data.csv', index=False)
val.to_csv('val_data.csv', index=False)
test.to_csv('test_data.csv', index=False)
"
```

### Step 5: Train ML Models

Create `server/ml/train_models.py` (see below)

```bash
python train_models.py

# Output: trained_models/ directory with all models
```

---

## 🎯 DETAILED IMPLEMENTATION FILES

### File 1: Synthetic Data Generator

**Location:** `server/ml/synthetic_data_generator.py`

**Status:** ✅ READY (Already created)

**Key Features:**
- Generates 10,000+ synthetic records
- Calls backend `/kundali/generate_kundali` API
- Extracts 200+ features
- Generates 8 target variables
- Saves to CSV

**Usage:**
```python
from synthetic_data_generator import SyntheticKundaliGenerator

generator = SyntheticKundaliGenerator(api_url="http://localhost:8000")
dataset = generator.generate_dataset(num_records=10000, output_file='training_data.csv')
```

---

### File 2: Data Validator

**Location:** `server/ml/data_validator.py`

**Create this file with:**

```python
import pandas as pd
import numpy as np
import json

class DataValidator:
    # Validate 200+ features
    # Check ranges, missing values, duplicates
    # Detect outliers
    # Calculate quality score
    # Generate report
    pass
```

**Key Checks:**
- ✓ No duplicates
- ✓ All features in valid ranges
- ✓ < 5% missing values
- ✓ Balanced target distribution
- ✓ Outlier detection
- ✓ Quality score > 85%

---

### File 3: ML Training Pipeline

**Location:** `server/ml/train_models.py`

**Create with:**

```python
import tensorflow as tf
from tensorflow import keras
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class KundaliMLTrainer:
    """Train ML models for complete Kundali analysis"""

    def __init__(self, csv_file='training_data.csv'):
        self.df = pd.read_csv(csv_file)
        self.scaler = StandardScaler()
        self.models = {}

    def prepare_data(self):
        """Prepare features and targets"""
        # Separate features and targets
        feature_cols = [col for col in self.df.columns
                        if col not in ['id', 'birth_date', 'birth_time', 'location', 'is_synthetic',
                                       'career_potential', 'wealth_potential', 'marriage_happiness',
                                       'children_prospects', 'health_status', 'spiritual_inclination',
                                       'chart_strength', 'life_ease_score']]

        target_cols = ['career_potential', 'wealth_potential', 'marriage_happiness',
                       'children_prospects', 'health_status', 'spiritual_inclination',
                       'chart_strength', 'life_ease_score']

        X = self.df[feature_cols]
        y = self.df[target_cols]

        # Normalize features
        X_normalized = self.scaler.fit_transform(X)
        X_df = pd.DataFrame(X_normalized, columns=feature_cols)

        return X_df, y

    def build_neural_network(self, input_dim, output_dim):
        """Build neural network for multi-task learning"""
        model = keras.Sequential([
            keras.layers.Input(shape=(input_dim,)),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.3),

            keras.layers.Dense(64, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.2),

            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dropout(0.1),

            keras.layers.Dense(output_dim, activation='sigmoid')
        ])

        return model

    def train_models(self, X, y):
        """Train multiple models for different prediction tasks"""

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train neural network (multi-task)
        nn_model = self.build_neural_network(X.shape[1], y.shape[1])
        nn_model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae', 'rmse']
        )

        nn_model.fit(
            X_train, y_train,
            batch_size=32,
            epochs=100,
            validation_split=0.15,
            verbose=1,
            callbacks=[
                keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=15,
                    restore_best_weights=True
                ),
                keras.callbacks.ReduceLROnPlateau(
                    monitor='val_loss',
                    factor=0.5,
                    patience=5,
                    min_lr=1e-6
                )
            ]
        )

        # Train XGBoost (gradient boosting)
        xgb_model = xgb.XGBRegressor(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            objective='reg:squarederror'
        )

        xgb_model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            early_stopping_rounds=20,
            verbose=10
        )

        # Evaluate
        train_loss = nn_model.evaluate(X_train, y_train, verbose=0)
        test_loss = nn_model.evaluate(X_test, y_test, verbose=0)

        xgb_train_score = xgb_model.score(X_train, y_train)
        xgb_test_score = xgb_model.score(X_test, y_test)

        results = {
            'neural_network': {
                'train_loss': train_loss,
                'test_loss': test_loss,
                'model': nn_model
            },
            'xgboost': {
                'train_score': xgb_train_score,
                'test_score': xgb_test_score,
                'model': xgb_model
            }
        }

        return results

# Usage
if __name__ == "__main__":
    trainer = KundaliMLTrainer('training_data.csv')
    X, y = trainer.prepare_data()
    results = trainer.train_models(X, y)
    print(results)
```

---

## 📊 DATASET STRUCTURE FOR TRAINING

### Features (200+)

```
CATEGORY 1: Planet Positions
- sun_degree, moon_degree, mars_degree, ... (9 planets)
- sun_house, moon_house, mars_house, ... (9 planets)
- sun_sign_encoded, moon_sign_encoded, ... (9 planets)

CATEGORY 2: House Analysis
- planets_in_house_1 to planets_in_house_12
- house_1_lord_strength to house_12_lord_strength

CATEGORY 3: Planetary Strengths (Shad Bala)
- sun_strength, sun_sthana_bala, sun_dig_bala, ...
- (6 components × 7 planets = 42 features)

CATEGORY 4: Yoga & Aspects
- total_yoga_count, benefic_yoga_count
- raj_yoga_present, parivartana_yoga_present, ...

CATEGORY 5: Divisional Charts
- d1_d9_alignment, d1_d2_alignment, ...
- chart_quality_score

CATEGORY 6: Other
- retrograde_planet_count
- current_dasha_remaining_years
```

### Targets (8 Variables - What Model Predicts)

```
1. career_potential (0-100)       → Career opportunities
2. wealth_potential (0-100)       → Financial success
3. marriage_happiness (0-100)     → Marriage prospects
4. children_prospects (0-100)     → Fertility
5. health_status (0-100)          → Overall health
6. spiritual_inclination (0-100)  → Spiritual bent
7. chart_strength (0-100)         → Overall chart strength
8. life_ease_score (0-100)        → Life ease index
```

---

## 🚀 STEP-BY-STEP WORKFLOW

### Phase 1: Data Generation (2-3 hours)

```
1. Run synthetic data generator
   └─ Generates 10,000 records
   └─ Each record calls API
   └─ Saves to training_data.csv

2. Validate quality
   └─ Check ranges
   └─ Check for duplicates
   └─ Calculate quality score
   └─ Save validation_report.json
```

**Expected Output:**
- `training_data.csv` (10,000 rows × 210 columns)
- `validation_report.json` (Quality metrics)

### Phase 2: Feature Engineering (30 minutes)

```
1. Load training_data.csv
2. Separate features (200+) from targets (8)
3. Normalize features using StandardScaler
4. Handle missing values
5. Remove outliers
6. Create feature importance matrix
```

### Phase 3: Data Splitting (10 minutes)

```
Total: 10,000 records
├─ Training: 7,000 (70%)
├─ Validation: 1,500 (15%)
└─ Test: 1,500 (15%)

Save as:
├─ train_data.csv
├─ val_data.csv
└─ test_data.csv
```

### Phase 4: Model Training (4-6 hours)

```
Train 2 models:

1. Neural Network (Multi-task Learning)
   ├─ Input: 200 features
   ├─ Layers: 128 → 64 → 32 → 8
   ├─ Activation: ReLU
   ├─ Output: 8 targets (sigmoid)
   └─ Epochs: 100 (with early stopping)

2. XGBoost (Gradient Boosting)
   ├─ 200 estimators
   ├─ Max depth: 6
   ├─ Learning rate: 0.1
   └─ Early stopping: 20 rounds
```

### Phase 5: Model Evaluation & Deployment

```
Metrics to Calculate:
├─ R² Score (coefficient of determination)
├─ RMSE (root mean squared error)
├─ MAE (mean absolute error)
├─ Correlation with actual
└─ Per-target performance

Save Models:
├─ neural_network_model.h5
├─ xgboost_model.pkl
└─ scaler.pkl (for prediction)
```

---

## 💾 EXPECTED RESULTS

### Data Generation
- ✅ 10,000 synthetic records
- ✅ 210 total columns (200+ features + 8 targets + metadata)
- ✅ 0 duplicates
- ✅ Quality score: 90%+
- ✅ Balanced target distribution

### Model Performance Targets
- ✅ Career Potential R²: > 0.75
- ✅ Wealth Potential R²: > 0.75
- ✅ Marriage Happiness R²: > 0.70
- ✅ Chart Strength R²: > 0.80
- ✅ Overall Accuracy: > 80%

### Files Generated
```
server/ml/
├── training_data.csv           (10K records)
├── train_data.csv              (7K records)
├── val_data.csv                (1.5K records)
├── test_data.csv               (1.5K records)
├── validation_report.json
├── trained_models/
│   ├── neural_network_model.h5
│   ├── xgboost_model.pkl
│   ├── scaler.pkl
│   └── model_metrics.json
└── visualizations/
    ├── feature_importance.png
    ├── target_distribution.png
    └── model_performance.png
```

---

## 🔄 PREDICTION API ENDPOINT

### Add to routes

```python
# File: server/routes/ml_predictions.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
from tensorflow import keras

router = APIRouter(prefix="/ml", tags=["ML Predictions"])

# Load trained models
nn_model = keras.models.load_model('server/ml/trained_models/neural_network_model.h5')
xgb_model = joblib.load('server/ml/trained_models/xgboost_model.pkl')
scaler = joblib.load('server/ml/trained_models/scaler.pkl')

class KundaliMLRequest(BaseModel):
    features: List[float]  # 200 features

@router.post("/predict")
async def predict_kundali_analysis(request: KundaliMLRequest):
    """
    Predict complete Kundali analysis using ML model

    Input: 200 features from Kundali
    Output: 8 predictions (career, wealth, marriage, etc.)
    """
    try:
        # Normalize features
        features_normalized = scaler.transform([request.features])

        # Get predictions from both models
        nn_predictions = nn_model.predict(features_normalized, verbose=0)[0]
        xgb_predictions = xgb_model.predict(features_normalized)[0]

        # Ensemble: Average both models
        ensemble_predictions = (nn_predictions + xgb_predictions) / 2

        return {
            'success': True,
            'predictions': {
                'career_potential': float(ensemble_predictions[0]),
                'wealth_potential': float(ensemble_predictions[1]),
                'marriage_happiness': float(ensemble_predictions[2]),
                'children_prospects': float(ensemble_predictions[3]),
                'health_status': float(ensemble_predictions[4]),
                'spiritual_inclination': float(ensemble_predictions[5]),
                'chart_strength': float(ensemble_predictions[6]),
                'life_ease_score': float(ensemble_predictions[7]),
            },
            'model_type': 'ensemble'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## ⏱️ TIMELINE & EFFORT

### Week 1: Data Generation & Validation
- Generate synthetic data: 2-3 hours
- Validate quality: 30 minutes
- Fix any issues: 1-2 hours
- **Total: 4-6 hours**

### Week 2: Feature Engineering & Preparation
- Load and explore data: 1 hour
- Feature engineering: 2 hours
- Data splitting: 30 minutes
- **Total: 3.5 hours**

### Week 3: Model Training
- Train neural network: 3-4 hours
- Train XGBoost: 2-3 hours
- Evaluation & tuning: 2-3 hours
- **Total: 7-10 hours**

### Week 4: Deployment & Integration
- Create prediction API: 2 hours
- Test predictions: 1-2 hours
- Documentation: 2 hours
- **Total: 5-6 hours**

**Grand Total: 20-26 hours**

---

## ✅ CHECKLIST

### Before Starting
- [ ] Backend API running (`python -m uvicorn server.main:app --reload`)
- [ ] All dependencies installed
- [ ] At least 50GB free disk space (for data + models)
- [ ] Python 3.8+ installed

### Data Generation
- [ ] Synthetic data generator created
- [ ] Generate 10,000 records
- [ ] Data validator created
- [ ] Validation quality score > 85%
- [ ] No duplicates or out-of-range values

### Model Training
- [ ] Features normalized
- [ ] Data split (70/15/15)
- [ ] Neural network trained
- [ ] XGBoost trained
- [ ] Models evaluated
- [ ] Models saved

### Deployment
- [ ] Prediction API created
- [ ] Models loaded correctly
- [ ] Predictions tested
- [ ] API documentation created
- [ ] Integration complete

---

## 🎯 SUCCESS CRITERIA

✅ **Complete when:**
1. 10,000 synthetic Kundali records generated
2. Data quality score > 85%
3. ML models trained with R² > 0.75
4. Prediction API functional
5. Accuracy > 80% on test data
6. All 8 targets predicted correctly

**You'll have:** Complete ML system for Kundali analysis predicting 8 life areas!
