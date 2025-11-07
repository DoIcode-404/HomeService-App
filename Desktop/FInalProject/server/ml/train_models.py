"""
ML Training Pipeline for Kundali Analysis
Trains neural network and gradient boosting models for complete Kundali analysis.

Models:
1. Neural Network (Keras) - Multi-task learning for 8 predictions
2. XGBoost - Gradient boosting for ensemble predictions

Author: ML Pipeline
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Dict, Tuple
import json

# Optional TensorFlow imports
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    from tensorflow.keras.optimizers import Adam
    TF_AVAILABLE = True
except Exception as e:
    TF_AVAILABLE = False
    tf = None
    keras = None
    layers = None
    print(f"[WARNING] TensorFlow not available: {str(e)}")
    print("[WARNING] Neural Network training will be skipped")

import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

import joblib

logger = logging.getLogger(__name__)


class KundaliMLTrainer:
    """Train ML models for complete Kundali analysis."""

    def __init__(self, csv_file: str = 'training_data.csv', random_state: int = 42):
        """
        Initialize the ML trainer.

        Args:
            csv_file: Path to training data CSV
            random_state: Random seed for reproducibility
        """
        self.csv_file = csv_file
        self.random_state = random_state
        self.df = None
        self.X_train = None
        self.X_val = None
        self.X_test = None
        self.y_train = None
        self.y_val = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.models = {}
        self.metrics = {}

        # Target variables to predict
        self.target_cols = [
            'career_potential',
            'wealth_potential',
            'marriage_happiness',
            'children_prospects',
            'health_status',
            'spiritual_inclination',
            'chart_strength',
            'life_ease_score'
        ]

        # Columns to exclude from features
        self.exclude_cols = [
            'id', 'birth_date', 'birth_time', 'location', 'is_synthetic',
            'career_potential', 'wealth_potential', 'marriage_happiness',
            'children_prospects', 'health_status', 'spiritual_inclination',
            'chart_strength', 'life_ease_score'
        ]

    def load_data(self) -> bool:
        """Load training data from CSV."""
        try:
            logger.info(f"Loading data from {self.csv_file}...")
            self.df = pd.read_csv(self.csv_file)
            logger.info(f"Loaded {len(self.df)} records with {len(self.df.columns)} columns")
            return True
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False

    def prepare_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Prepare features and targets for training.

        Returns:
            Tuple of (features_df, targets_df)
        """
        try:
            logger.info("Preparing data...")

            # Get feature columns (all except excluded)
            feature_cols = [col for col in self.df.columns if col not in self.exclude_cols]

            X = self.df[feature_cols].copy()
            y = self.df[self.target_cols].copy()

            # Handle missing values
            X = X.fillna(X.mean())
            y = y.fillna(y.mean())

            logger.info(f"Features shape: {X.shape}")
            logger.info(f"Targets shape: {y.shape}")

            return X, y

        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            return None, None

    def split_data(self, X: pd.DataFrame, y: pd.DataFrame) -> bool:
        """
        Split data into train, validation, and test sets.

        Args:
            X: Features dataframe
            y: Targets dataframe

        Returns:
            True if successful
        """
        try:
            logger.info("Splitting data (70/15/15)...")

            # First split: 70% train, 30% temp
            X_train, X_temp, y_train, y_temp = train_test_split(
                X, y,
                test_size=0.3,
                random_state=self.random_state
            )

            # Second split: split temp into 50% val, 50% test
            X_val, X_test, y_val, y_test = train_test_split(
                X_temp, y_temp,
                test_size=0.5,
                random_state=self.random_state
            )

            # Normalize features
            logger.info("Normalizing features...")
            X_train_normalized = self.scaler.fit_transform(X_train)
            X_val_normalized = self.scaler.transform(X_val)
            X_test_normalized = self.scaler.transform(X_test)

            # Convert back to DataFrames
            self.X_train = pd.DataFrame(X_train_normalized, columns=X_train.columns)
            self.X_val = pd.DataFrame(X_val_normalized, columns=X_val.columns)
            self.X_test = pd.DataFrame(X_test_normalized, columns=X_test.columns)

            self.y_train = y_train.reset_index(drop=True)
            self.y_val = y_val.reset_index(drop=True)
            self.y_test = y_test.reset_index(drop=True)

            logger.info(f"Train: {self.X_train.shape[0]}, Val: {self.X_val.shape[0]}, Test: {self.X_test.shape[0]}")

            return True

        except Exception as e:
            logger.error(f"Error splitting data: {str(e)}")
            return False

    def build_neural_network(self):
        """
        Build neural network for multi-task learning.

        Returns:
            Compiled Keras model, or None if TensorFlow is not available
        """
        if not TF_AVAILABLE:
            logger.warning("TensorFlow not available - skipping neural network")
            return None

        input_dim = self.X_train.shape[1]
        output_dim = len(self.target_cols)

        logger.info(f"Building neural network: {input_dim} inputs -> {output_dim} outputs")

        model = keras.Sequential([
            keras.layers.Input(shape=(input_dim,)),

            # First dense block
            keras.layers.Dense(128, activation='relu', name='dense_1'),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.3),

            # Second dense block
            keras.layers.Dense(64, activation='relu', name='dense_2'),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.2),

            # Third dense block
            keras.layers.Dense(32, activation='relu', name='dense_3'),
            keras.layers.Dropout(0.1),

            # Output layer (8 targets with sigmoid for 0-1 range)
            keras.layers.Dense(output_dim, activation='sigmoid', name='output')
        ])

        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )

        logger.info("Neural network model compiled")
        return model

    def train_neural_network(self, model) -> Dict:
        """
        Train neural network.

        Args:
            model: Keras model to train

        Returns:
            Training metrics dictionary
        """
        if model is None:
            logger.warning("No model provided - skipping neural network training")
            return {}

        try:
            logger.info("Starting neural network training...")

            callbacks = [
                EarlyStopping(
                    monitor='val_loss',
                    patience=15,
                    restore_best_weights=True,
                    verbose=1
                ),
                ReduceLROnPlateau(
                    monitor='val_loss',
                    factor=0.5,
                    patience=5,
                    min_lr=1e-6,
                    verbose=1
                )
            ]

            history = model.fit(
                self.X_train, self.y_train,
                batch_size=32,
                epochs=100,
                validation_data=(self.X_val, self.y_val),
                callbacks=callbacks,
                verbose=1
            )

            # Evaluate on test set
            test_loss, test_mae = model.evaluate(self.X_test, self.y_test, verbose=0)

            # Get predictions
            y_train_pred = model.predict(self.X_train, verbose=0)
            y_val_pred = model.predict(self.X_val, verbose=0)
            y_test_pred = model.predict(self.X_test, verbose=0)

            # Calculate R² scores
            train_r2 = r2_score(self.y_train, y_train_pred)
            val_r2 = r2_score(self.y_val, y_val_pred)
            test_r2 = r2_score(self.y_test, y_test_pred)

            metrics = {
                'model_type': 'neural_network',
                'test_loss': float(test_loss),
                'test_mae': float(test_mae),
                'train_r2': float(train_r2),
                'val_r2': float(val_r2),
                'test_r2': float(test_r2),
                'epochs_trained': len(history.history['loss'])
            }

            logger.info(f"Neural Network - Test R²: {test_r2:.4f}, Test Loss: {test_loss:.4f}")

            self.models['neural_network'] = model
            self.metrics['neural_network'] = metrics

            return metrics

        except Exception as e:
            logger.error(f"Error training neural network: {str(e)}")
            return {}

    def train_xgboost(self) -> Dict:
        """
        Train XGBoost model.

        Returns:
            Training metrics dictionary
        """
        try:
            logger.info("Starting XGBoost training...")

            # Create XGBoost model
            xgb_model = xgb.XGBRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=self.random_state,
                objective='reg:squarederror',
                tree_method='hist',
                verbose=1
            )

            # Train
            xgb_model.fit(
                self.X_train, self.y_train,
                eval_set=[(self.X_val, self.y_val), (self.X_test, self.y_test)],
                verbose=10
            )

            # Get predictions
            y_train_pred = xgb_model.predict(self.X_train)
            y_val_pred = xgb_model.predict(self.X_val)
            y_test_pred = xgb_model.predict(self.X_test)

            # Calculate metrics
            train_r2 = r2_score(self.y_train, y_train_pred)
            val_r2 = r2_score(self.y_val, y_val_pred)
            test_r2 = r2_score(self.y_test, y_test_pred)
            test_mse = mean_squared_error(self.y_test, y_test_pred)
            test_mae = mean_absolute_error(self.y_test, y_test_pred)

            metrics = {
                'model_type': 'xgboost',
                'test_r2': float(test_r2),
                'val_r2': float(val_r2),
                'train_r2': float(train_r2),
                'test_mse': float(test_mse),
                'test_mae': float(test_mae),
                'n_estimators': 200
            }

            logger.info(f"XGBoost - Test R²: {test_r2:.4f}, Test MAE: {test_mae:.4f}")

            self.models['xgboost'] = xgb_model
            self.metrics['xgboost'] = metrics

            return metrics

        except Exception as e:
            logger.error(f"Error training XGBoost: {str(e)}")
            return {}

    def save_models(self, output_dir: str = 'trained_models') -> bool:
        """
        Save trained models to disk.

        Args:
            output_dir: Directory to save models

        Returns:
            True if successful
        """
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)

            logger.info(f"Saving models to {output_dir}...")

            # Save neural network
            if 'neural_network' in self.models:
                nn_path = output_path / 'neural_network_model.h5'
                self.models['neural_network'].save(str(nn_path))
                logger.info(f"Saved neural network to {nn_path}")

            # Save XGBoost
            if 'xgboost' in self.models:
                xgb_path = output_path / 'xgboost_model.pkl'
                joblib.dump(self.models['xgboost'], str(xgb_path))
                logger.info(f"Saved XGBoost to {xgb_path}")

            # Save scaler
            scaler_path = output_path / 'scaler.pkl'
            joblib.dump(self.scaler, str(scaler_path))
            logger.info(f"Saved scaler to {scaler_path}")

            # Save metrics
            metrics_path = output_path / 'model_metrics.json'
            with open(metrics_path, 'w') as f:
                json.dump(self.metrics, f, indent=2)
            logger.info(f"Saved metrics to {metrics_path}")

            # Save feature names
            feature_names_path = output_path / 'feature_names.json'
            feature_names = list(self.X_train.columns)
            with open(feature_names_path, 'w') as f:
                json.dump(feature_names, f, indent=2)
            logger.info(f"Saved feature names to {feature_names_path}")

            # Save target names
            target_names_path = output_path / 'target_names.json'
            with open(target_names_path, 'w') as f:
                json.dump(self.target_cols, f, indent=2)
            logger.info(f"Saved target names to {target_names_path}")

            return True

        except Exception as e:
            logger.error(f"Error saving models: {str(e)}")
            return False

    def print_summary(self):
        """Print training summary."""
        print("\n" + "="*70)
        print("ML MODEL TRAINING SUMMARY")
        print("="*70)

        print("\nData:")
        print(f"  Training samples: {len(self.X_train)}")
        print(f"  Validation samples: {len(self.X_val)}")
        print(f"  Test samples: {len(self.X_test)}")
        print(f"  Features: {self.X_train.shape[1]}")
        print(f"  Targets: {len(self.target_cols)}")

        print("\nNeural Network Metrics:")
        if 'neural_network' in self.metrics:
            nn_metrics = self.metrics['neural_network']
            print(f"  Test R²: {nn_metrics.get('test_r2', 'N/A'):.4f}")
            print(f"  Test Loss: {nn_metrics.get('test_loss', 'N/A'):.4f}")
            print(f"  Test MAE: {nn_metrics.get('test_mae', 'N/A'):.4f}")
        else:
            print("  Not trained")

        print("\nXGBoost Metrics:")
        if 'xgboost' in self.metrics:
            xgb_metrics = self.metrics['xgboost']
            print(f"  Test R²: {xgb_metrics.get('test_r2', 'N/A'):.4f}")
            print(f"  Test MAE: {xgb_metrics.get('test_mae', 'N/A'):.4f}")
            print(f"  Test MSE: {xgb_metrics.get('test_mse', 'N/A'):.4f}")
        else:
            print("  Not trained")

        print("\n" + "="*70 + "\n")

    def train_all(self) -> bool:
        """
        Complete training pipeline.

        Returns:
            True if all models trained successfully
        """
        try:
            # Load data
            if not self.load_data():
                return False

            # Prepare data
            X, y = self.prepare_data()
            if X is None:
                return False

            # Split data
            if not self.split_data(X, y):
                return False

            # Train neural network (if TensorFlow is available)
            if TF_AVAILABLE:
                logger.info("\n" + "="*70)
                logger.info("TRAINING NEURAL NETWORK")
                logger.info("="*70)
                nn_model = self.build_neural_network()
                self.train_neural_network(nn_model)
            else:
                logger.warning("\n" + "="*70)
                logger.warning("SKIPPING NEURAL NETWORK (TensorFlow not available)")
                logger.warning("="*70)

            # Train XGBoost
            logger.info("\n" + "="*70)
            logger.info("TRAINING XGBOOST")
            logger.info("="*70)
            self.train_xgboost()

            # Save models
            self.save_models()

            # Print summary
            self.print_summary()

            logger.info("[OK] All available models trained successfully!")
            return True

        except Exception as e:
            logger.error(f"Error in training pipeline: {str(e)}")
            return False


def main():
    """Main training function."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Use absolute path
    script_dir = Path(__file__).parent
    csv_file = script_dir / 'training_data.csv'

    trainer = KundaliMLTrainer(csv_file=str(csv_file))
    success = trainer.train_all()

    if success:
        print("\n[OK] Training complete! Models saved to 'trained_models/' directory")
    else:
        print("\n[WARNING] Training failed. Check logs for details.")


if __name__ == "__main__":
    main()