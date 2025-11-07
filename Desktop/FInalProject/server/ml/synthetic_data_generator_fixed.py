"""
Fixed Synthetic Data Generator for Kundali Analysis
Generates realistic synthetic training data with proper variance in targets.

This version DOES NOT rely on the broken backend API.
Instead, it generates:
1. Realistic astrological features (planetary positions, house placements)
2. Realistic target variables with actual variance
3. Proper data validation and quality checks
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Dict, List
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FixedSyntheticKundaliGenerator:
    """Generate realistic synthetic Kundali data with proper feature/target variance."""

    def __init__(self, seed=42):
        self.seed = seed
        np.random.seed(seed)

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

    def generate_features(self, num_records: int) -> pd.DataFrame:
        """
        Generate 62 realistic astrological features with VARIANCE.

        Features include:
        - Planetary positions (zodiac degrees): 10 planets x 1 = 10
        - House placements: 12 houses x 2 (planet count, lord strength) = 24
        - Planetary strengths: 10 planets = 10
        - Yogas: 6 yoga counts = 6
        - Aspect strengths: 6 aspect types = 6
        """
        logger.info(f"Generating {num_records} feature records...")

        features = {}

        # 1. Planetary positions (0-360 degrees, realistic variation)
        planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu', 'Ascendant']
        for planet in planets:
            features[f'{planet.lower()}_degree'] = np.random.uniform(0, 360, num_records)

        # 2. House placements (0-12 planets per house, lord strength 0-100)
        for house_num in range(1, 13):
            features[f'house_{house_num}_planets'] = np.random.randint(0, 4, num_records)
            features[f'house_{house_num}_lord_strength'] = np.random.uniform(20, 100, num_records)

        # 3. Planetary strengths (0-100 scale)
        for planet in planets[:-1]:  # Exclude Ascendant
            features[f'{planet.lower()}_strength'] = np.random.uniform(20, 100, num_records)

        # 4. Yoga counts
        features['total_yoga_count'] = np.random.randint(0, 8, num_records)
        features['benefic_yoga_count'] = np.random.randint(0, 6, num_records)
        features['malefic_yoga_count'] = np.random.randint(0, 4, num_records)
        features['neutral_yoga_count'] = np.random.randint(0, 3, num_records)

        # 5. Aspect strengths (0-100)
        for i in range(1, 7):
            features[f'aspect_strength_{i}'] = np.random.uniform(0, 100, num_records)

        df = pd.DataFrame(features)
        logger.info(f"  Generated features shape: {df.shape}")
        logger.info(f"  Features: {list(df.columns)[:5]}... (showing first 5)")

        # Validate no constant features
        for col in df.columns:
            std = df[col].std()
            if std < 0.1:
                logger.warning(f"  WARNING: Feature {col} has very low variance (std={std:.4f})")

        return df

    def generate_targets(self, features: pd.DataFrame) -> pd.DataFrame:
        """
        Generate realistic target variables based on features.
        Targets have REAL VARIANCE and meaningful relationships to features.
        """
        logger.info(f"Generating targets with meaningful relationships to features...")

        targets = {}
        num_records = len(features)

        # 1. Career Potential (depends on House 10, Saturn, Sun strength)
        base = 50
        career_potential = base + \
            (features['house_10_lord_strength'] / 100) * 30 + \
            (features['saturn_strength'] / 100) * 15 + \
            (features['sun_strength'] / 100) * 5 + \
            np.random.normal(0, 5, num_records)  # Add realistic noise
        targets['career_potential'] = np.clip(career_potential, 0, 100)

        # 2. Wealth Potential (depends on House 2, Jupiter, Venus strength)
        base = 50
        wealth_potential = base + \
            (features['house_2_lord_strength'] / 100) * 25 + \
            (features['jupiter_strength'] / 100) * 20 + \
            (features['venus_strength'] / 100) * 10 + \
            np.random.normal(0, 6, num_records)
        targets['wealth_potential'] = np.clip(wealth_potential, 0, 100)

        # 3. Marriage Happiness (depends on House 7, Venus, Mars, D9 compatibility)
        base = 55
        marriage_happiness = base + \
            (features['house_7_lord_strength'] / 100) * 30 + \
            (features['venus_strength'] / 100) * 15 - \
            (features['mars_strength'] / 100) * 5 + \
            np.random.normal(0, 7, num_records)
        targets['marriage_happiness'] = np.clip(marriage_happiness, 0, 100)

        # 4. Children Prospects (depends on House 5, Jupiter, Moon strength)
        base = 60
        children_prospects = base + \
            (features['house_5_lord_strength'] / 100) * 25 + \
            (features['jupiter_strength'] / 100) * 15 + \
            np.random.normal(0, 5, num_records)
        targets['children_prospects'] = np.clip(children_prospects, 0, 100)

        # 5. Health Status (depends on House 6, Saturn, Mars, Moon strength)
        base = 65
        health_status = base + \
            (100 - features['mars_strength']) / 100 * 20 + \
            (100 - features['saturn_strength']) / 100 * 10 + \
            (features['moon_strength'] / 100) * 15 + \
            np.random.normal(0, 6, num_records)
        targets['health_status'] = np.clip(health_status, 0, 100)

        # 6. Spiritual Inclination (depends on 12H, Saturn, Rahu, yoga count)
        base = 45
        spiritual_inclination = base + \
            (features['house_12_lord_strength'] / 100) * 25 + \
            (features['saturn_strength'] / 100) * 10 + \
            (features['total_yoga_count'] / 8) * 20 + \
            np.random.normal(0, 8, num_records)
        targets['spiritual_inclination'] = np.clip(spiritual_inclination, 0, 100)

        # 7. Chart Strength (overall average of all strengths + yoga boost)
        chart_strength = \
            (features['sun_strength'] + features['moon_strength'] + features['jupiter_strength']) / 3 * 0.6 + \
            (features['total_yoga_count'] / 8) * 30 + \
            np.random.normal(0, 5, num_records)
        targets['chart_strength'] = np.clip(chart_strength, 0, 100)

        # 8. Life Ease Score (overall well-being, combines all factors)
        base = 50
        life_ease_score = base + \
            (features['house_1_lord_strength'] / 100) * 15 + \
            (features['benefic_yoga_count'] / 6) * 30 - \
            (features['malefic_yoga_count'] / 4) * 10 + \
            np.random.normal(0, 8, num_records)
        targets['life_ease_score'] = np.clip(life_ease_score, 0, 100)

        df = pd.DataFrame(targets)
        logger.info(f"  Generated targets shape: {df.shape}")

        # Validate variance
        print("\n[Target Variable Statistics]")
        for col in df.columns:
            print(f"  {col}:")
            print(f"    Mean: {df[col].mean():.2f}, Std: {df[col].std():.2f}")
            print(f"    Min: {df[col].min():.2f}, Max: {df[col].max():.2f}")
            print(f"    Unique values: {df[col].nunique()}")

        return df

    def generate_dataset(self, num_records: int = 10000, output_file: str = None) -> Dict:
        """
        Generate complete synthetic Kundali dataset.
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"GENERATING SYNTHETIC KUNDALI DATASET")
        logger.info(f"{'='*70}\n")

        # Generate features and targets
        features_df = self.generate_features(num_records)
        targets_df = self.generate_targets(features_df)

        # Combine
        dataset_df = pd.concat([features_df, targets_df], axis=1)

        logger.info(f"\nCombined dataset shape: {dataset_df.shape}")
        logger.info(f"Total columns: {dataset_df.shape[1]}")

        # Verify no data quality issues
        logger.info(f"\n[Data Quality Checks]")

        # Check for NaN values
        nan_count = dataset_df.isna().sum().sum()
        if nan_count > 0:
            logger.error(f"  ERROR: {nan_count} NaN values found!")
        else:
            logger.info(f"  [OK] No NaN values")

        # Check target variance
        logger.info(f"\n[Target Variable Variance Check]")
        all_have_variance = True
        for col in self.target_cols:
            std = dataset_df[col].std()
            if std < 5:
                logger.error(f"  ERROR: {col} has very low variance (std={std:.4f})")
                all_have_variance = False
            else:
                logger.info(f"  [OK] {col} has good variance (std={std:.4f})")

        if not all_have_variance:
            raise ValueError("Target variables have insufficient variance!")

        # Save to CSV
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            dataset_df.to_csv(output_path, index=False)
            logger.info(f"\n[OK] Dataset saved to {output_path}")
            logger.info(f"  File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

        logger.info(f"\n{'='*70}")
        logger.info(f"DATASET GENERATION COMPLETE")
        logger.info(f"  Total records: {num_records}")
        logger.info(f"  Total features: {len(features_df.columns)}")
        logger.info(f"  Total targets: {len(targets_df.columns)}")
        logger.info(f"{'='*70}\n")

        return dataset_df.to_dict()


def main():
    """Main function to generate fixed synthetic dataset."""
    logger.info("="*70)
    logger.info("FIXED SYNTHETIC DATA GENERATOR")
    logger.info("No dependency on broken backend API")
    logger.info("="*70 + "\n")

    script_dir = Path(__file__).parent
    output_file = script_dir / 'training_data_fixed.csv'

    generator = FixedSyntheticKundaliGenerator(seed=42)
    dataset = generator.generate_dataset(
        num_records=10000,
        output_file=str(output_file)
    )

    print(f"\n[SUCCESS] Fixed training data generated!")
    print(f"  File: {output_file}")
    print(f"  Records: 10,000")
    print(f"\nNext steps:")
    print(f"  1. Delete old broken data: rm training_data.csv")
    print(f"  2. Rename fixed file: mv training_data_fixed.csv training_data.csv")
    print(f"  3. Delete old models: rm -rf trained_models/")
    print(f"  4. Retrain models: python train_models.py")


if __name__ == "__main__":
    main()