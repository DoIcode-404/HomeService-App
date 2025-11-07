"""
Synthetic Kundali Dataset Generator
Generates synthetic Kundali records using the backend API for ML training.

This generator creates training-ready datasets by:
1. Generating random but valid birth parameters
2. Calling the backend Kundali API
3. Extracting features from the response
4. Generating labels based on Vedic astrology rules
5. Validating and saving data to CSV

Author: ML Pipeline
"""

import requests
import random
import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SyntheticKundaliGenerator:
    """Generate synthetic Kundali records for ML training."""

    # Major world cities with coordinates and timezone
    MAJOR_CITIES = [
        {'name': 'Delhi', 'latitude': 28.6139, 'longitude': 77.2090, 'timezone': 'Asia/Kolkata'},
        {'name': 'Mumbai', 'latitude': 19.0760, 'longitude': 72.8777, 'timezone': 'Asia/Kolkata'},
        {'name': 'Bangalore', 'latitude': 12.9716, 'longitude': 77.5946, 'timezone': 'Asia/Kolkata'},
        {'name': 'Chennai', 'latitude': 13.0827, 'longitude': 80.2707, 'timezone': 'Asia/Kolkata'},
        {'name': 'Kolkata', 'latitude': 22.5726, 'longitude': 88.3639, 'timezone': 'Asia/Kolkata'},
        {'name': 'Pune', 'latitude': 18.5204, 'longitude': 73.8567, 'timezone': 'Asia/Kolkata'},
        {'name': 'New York', 'latitude': 40.7128, 'longitude': -74.0060, 'timezone': 'America/New_York'},
        {'name': 'London', 'latitude': 51.5074, 'longitude': -0.1278, 'timezone': 'Europe/London'},
        {'name': 'Tokyo', 'latitude': 35.6762, 'longitude': 139.6503, 'timezone': 'Asia/Tokyo'},
        {'name': 'Sydney', 'latitude': -33.8688, 'longitude': 151.2093, 'timezone': 'Australia/Sydney'},
        {'name': 'Los Angeles', 'latitude': 34.0522, 'longitude': -118.2437, 'timezone': 'America/Los_Angeles'},
        {'name': 'Paris', 'latitude': 48.8566, 'longitude': 2.3522, 'timezone': 'Europe/Paris'},
    ]

    # Vedic time periods for predictions
    DASHA_DURATIONS = {
        'Sun': 6,
        'Moon': 10,
        'Mars': 7,
        'Mercury': 17,
        'Jupiter': 16,
        'Venus': 20,
        'Saturn': 19,
        'Rahu': 18,
        'Ketu': 7
    }

    def __init__(self, api_url: str = "http://localhost:8000", batch_size: int = 10):
        """
        Initialize the synthetic data generator.

        Args:
            api_url: URL of the backend API
            batch_size: Number of records to generate before saving
        """
        self.api_url = api_url
        self.batch_size = batch_size
        self.session = requests.Session()
        self.generated_count = 0
        self.error_count = 0

    def generate_random_birth_date(self) -> Tuple[str, str]:
        """
        Generate random birth date and time.

        Returns:
            Tuple of (date_str, time_str)
        """
        # Random date between 1950 and 2020
        start_date = datetime(1950, 1, 1)
        end_date = datetime(2020, 12, 31)
        random_days = random.randint(0, (end_date - start_date).days)
        birth_datetime = start_date + timedelta(days=random_days)

        # Random time
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)

        date_str = birth_datetime.strftime('%Y-%m-%d')
        time_str = f"{hour:02d}:{minute:02d}"

        return date_str, time_str

    def generate_random_location(self) -> Dict:
        """
        Generate random location from major cities.

        Returns:
            Dictionary with location details
        """
        city = random.choice(self.MAJOR_CITIES)
        return city

    def generate_birth_parameters(self) -> Dict:
        """
        Generate complete random birth parameters.

        Returns:
            Dictionary with valid birth parameters
        """
        birth_date, birth_time = self.generate_random_birth_date()
        location = self.generate_random_location()

        return {
            'birthDate': birth_date,
            'birthTime': birth_time,
            'latitude': location['latitude'],
            'longitude': location['longitude'],
            'timezone': location['timezone'],
            'location': location['name']
        }

    def call_api(self, birth_params: Dict) -> Dict:
        """
        Call the backend API to generate Kundali.

        Args:
            birth_params: Birth parameters

        Returns:
            Kundali data from API
        """
        try:
            response = self.session.post(
                f"{self.api_url}/kundali/generate_kundali",
                json=birth_params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if data['success']:
                return data['data']
            else:
                logger.error(f"API returned error: {data['message']}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return None

    def extract_features(self, kundali_data: Dict) -> Dict:
        """
        Extract ML features from Kundali data.

        Args:
            kundali_data: Kundali response from API

        Returns:
            Dictionary of extracted features
        """
        if not kundali_data:
            return {}

        features = {}

        try:
            # Planet position features (0-360)
            planets_list = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']

            for planet in planets_list:
                planet_data = kundali_data['planets'].get(planet, {})
                if isinstance(planet_data, dict):
                    features[f'{planet.lower()}_degree'] = planet_data.get('longitude', 0)
                    features[f'{planet.lower()}_house'] = planet_data.get('house', 0)
                    features[f'{planet.lower()}_sign_encoded'] = self._encode_sign(planet_data.get('sign', 'Aries'))

            # House features
            for house_num in range(1, 13):
                house_data = kundali_data['houses'].get(house_num, {})
                if isinstance(house_data, dict):
                    features[f'planets_in_house_{house_num}'] = len(house_data.get('planets', []))
                    features[f'house_{house_num}_lord_strength'] = house_data.get('lord_strength', 0)

            # Strength features (Shad Bala)
            shad_bala = kundali_data.get('shad_bala', {})
            strengths = shad_bala.get('planetary_strengths', {})

            for planet in planets_list:
                if planet in strengths:
                    planet_strength = strengths[planet]
                    features[f'{planet.lower()}_strength'] = planet_strength.get('strength_percentage', 0)
                    breakdown = planet_strength.get('breakdown', {})
                    features[f'{planet.lower()}_sthana_bala'] = breakdown.get('sthana_bala', 0)
                    features[f'{planet.lower()}_dig_bala'] = breakdown.get('dig_bala', 0)
                    features[f'{planet.lower()}_kala_bala'] = breakdown.get('kala_bala', 0)
                    features[f'{planet.lower()}_chesta_bala'] = breakdown.get('chesta_bala', 0)
                    features[f'{planet.lower()}_naisargika_bala'] = breakdown.get('naisargika_bala', 0)
                    features[f'{planet.lower()}_drishti_bala'] = breakdown.get('drishti_bala', 0)

            # Yoga features
            yogas = kundali_data.get('yogas', {})
            benefic_yogas = yogas.get('benefic_yogas', [])
            malefic_yogas = yogas.get('malefic_yogas', [])

            features['total_yoga_count'] = len(benefic_yogas) + len(malefic_yogas)
            features['benefic_yoga_count'] = len(benefic_yogas)
            features['malefic_yoga_count'] = len(malefic_yogas)

            # Yoga names
            yoga_names = [y.get('name', '') for y in benefic_yogas] + [y.get('name', '') for y in malefic_yogas]
            features['raj_yoga_present'] = 1 if 'Raj Yoga' in yoga_names else 0
            features['parivartana_yoga_present'] = 1 if 'Parivartana Yoga' in yoga_names else 0
            features['gaj_kesari_yoga_present'] = 1 if 'Gaj Kesari Yoga' in yoga_names else 0

            # Dasha features
            dasha = kundali_data.get('dasha', {})
            features['current_dasha_remaining_years'] = dasha.get('remaining_maha_dasha_years', 0)

            # Divisional charts alignment
            div_charts = kundali_data.get('divisional_charts', {})
            alignment = div_charts.get('alignment_analysis', {})
            features['d1_d9_alignment'] = alignment.get('alignment_percentage', 50)

            # Ascendant and signs
            ascendant = kundali_data.get('ascendant', {})
            features['ascendant_sign_encoded'] = self._encode_sign(ascendant.get('sign', 'Aries'))
            features['moon_sign_encoded'] = self._encode_sign(kundali_data.get('zodiac_sign', 'Aries'))

            # Count retrograde planets
            retrograde_count = 0
            for planet in planets_list:
                planet_data = kundali_data['planets'].get(planet, {})
                if isinstance(planet_data, dict) and planet_data.get('retrograde', False):
                    retrograde_count += 1
            features['retrograde_planet_count'] = retrograde_count

            # Overall metrics
            features['chart_quality_score'] = sum(strengths.get(p, {}).get('strength_percentage', 0)
                                                   for p in planets_list) / len(planets_list)

        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")

        return features

    def _encode_sign(self, sign: str) -> int:
        """Encode zodiac sign to number 0-11."""
        signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        return signs.index(sign) if sign in signs else 0

    def generate_labels(self, kundali_data: Dict) -> Dict:
        """
        Generate target labels based on Vedic astrology rules.

        Args:
            kundali_data: Kundali response

        Returns:
            Dictionary of target labels
        """
        if not kundali_data:
            return {}

        labels = {}

        try:
            # Extract key information
            strengths = kundali_data.get('shad_bala', {}).get('planetary_strengths', {})
            yogas = kundali_data.get('yogas', {})
            dasha = kundali_data.get('dasha', {})
            houses = kundali_data.get('houses', {})

            # Career Potential (based on 10th house, Saturn, Sun)
            career_score = 50.0
            house_10 = houses.get(10, {})
            career_score += len(house_10.get('planets', [])) * 5
            career_score += (house_10.get('lord_strength', 50) / 100) * 20
            career_score += (strengths.get('Saturn', {}).get('strength_percentage', 50) / 100) * 15
            career_score += (strengths.get('Sun', {}).get('strength_percentage', 50) / 100) * 10
            labels['career_potential'] = min(100, max(0, career_score))

            # Wealth Potential (based on 2nd, 11th house, Jupiter, Venus)
            wealth_score = 50.0
            house_2 = houses.get(2, {})
            house_11 = houses.get(11, {})
            wealth_score += len(house_2.get('planets', [])) * 5 + len(house_11.get('planets', [])) * 5
            wealth_score += (house_2.get('lord_strength', 50) / 100) * 15
            wealth_score += (strengths.get('Jupiter', {}).get('strength_percentage', 50) / 100) * 15
            wealth_score += (strengths.get('Venus', {}).get('strength_percentage', 50) / 100) * 10
            labels['wealth_potential'] = min(100, max(0, wealth_score))

            # Marriage Happiness (based on 7th house, Venus, D9 alignment)
            marriage_score = 50.0
            house_7 = houses.get(7, {})
            div_alignment = kundali_data.get('divisional_charts', {}).get('alignment_analysis', {}).get('alignment_percentage', 50)
            marriage_score += len(house_7.get('planets', [])) * 5
            marriage_score += (house_7.get('lord_strength', 50) / 100) * 20
            marriage_score += (strengths.get('Venus', {}).get('strength_percentage', 50) / 100) * 15
            marriage_score += (div_alignment / 100) * 20
            labels['marriage_happiness'] = min(100, max(0, marriage_score))

            # Children Prospects (based on 5th house, Jupiter, D7)
            children_score = 50.0
            house_5 = houses.get(5, {})
            children_score += len(house_5.get('planets', [])) * 8
            children_score += (house_5.get('lord_strength', 50) / 100) * 20
            children_score += (strengths.get('Jupiter', {}).get('strength_percentage', 50) / 100) * 15
            labels['children_prospects'] = min(100, max(0, children_score))

            # Health Status (based on 6th house strength and Mars/Saturn weakness)
            health_score = 100.0
            house_6 = houses.get(6, {})
            health_score -= len(house_6.get('planets', [])) * 10  # Fewer planets better
            health_score -= (houses.get(6, {}).get('lord_strength', 50) / 100) * 20
            health_score -= (100 - strengths.get('Mars', {}).get('strength_percentage', 50)) * 0.2
            labels['health_status'] = min(100, max(0, health_score))

            # Spiritual Inclination (based on 12th house, Ketu, Saturn)
            spiritual_score = 50.0
            house_12 = houses.get(12, {})
            spiritual_score += len(house_12.get('planets', [])) * 8
            spiritual_score += (strengths.get('Saturn', {}).get('strength_percentage', 50) / 100) * 15
            labels['spiritual_inclination'] = min(100, max(0, spiritual_score))

            # Chart Strength (average of all planets)
            avg_strength = sum(p.get('strength_percentage', 50) for p in strengths.values()) / max(len(strengths), 1)
            labels['chart_strength'] = min(100, max(0, avg_strength))

            # Life Ease Score (based on yoga count, retrograde, strength)
            life_ease = 50.0
            benefic_yogas = len(yogas.get('benefic_yogas', []))
            malefic_yogas = len(yogas.get('malefic_yogas', []))
            life_ease += benefic_yogas * 5
            life_ease -= malefic_yogas * 5
            life_ease += (avg_strength - 50) * 0.5
            labels['life_ease_score'] = min(100, max(0, life_ease))

        except Exception as e:
            logger.error(f"Error generating labels: {str(e)}")

        return labels

    def generate_dataset(self, num_records: int = 1000, output_file: str = 'training_data.csv') -> List[Dict]:
        """
        Generate complete synthetic dataset.

        Args:
            num_records: Number of records to generate
            output_file: Output CSV file path

        Returns:
            List of generated records
        """
        dataset = []
        output_path = Path(output_file)

        logger.info(f"Starting generation of {num_records} synthetic records...")

        for i in range(num_records):
            try:
                # Generate birth parameters
                birth_params = self.generate_birth_parameters()

                # Call API
                kundali_data = self.call_api(birth_params)

                if kundali_data:
                    # Extract features and generate labels
                    features = self.extract_features(kundali_data)
                    labels = self.generate_labels(kundali_data)

                    # Combine all data
                    record = {
                        'id': i + 1,
                        'birth_date': birth_params['birthDate'],
                        'birth_time': birth_params['birthTime'],
                        'location': birth_params['location'],
                        'is_synthetic': True,
                        **features,
                        **labels
                    }

                    dataset.append(record)
                    self.generated_count += 1

                    if (i + 1) % 100 == 0:
                        logger.info(f"Generated {i + 1}/{num_records} records")

                    # Save periodically
                    if self.generated_count % self.batch_size == 0:
                        self._save_batch_to_csv(dataset, output_path)

                else:
                    self.error_count += 1
                    logger.warning(f"Failed to generate record {i + 1}")

            except Exception as e:
                self.error_count += 1
                logger.error(f"Error in record {i + 1}: {str(e)}")
                continue

        # Final save
        self._save_batch_to_csv(dataset, output_path)

        logger.info(f"Dataset generation complete!")
        logger.info(f"Successfully generated: {self.generated_count} records")
        logger.info(f"Errors: {self.error_count}")
        logger.info(f"Saved to: {output_path}")

        return dataset

    def _save_batch_to_csv(self, dataset: List[Dict], output_path: Path):
        """Save batch of records to CSV."""
        if not dataset:
            return

        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=dataset[0].keys())
                writer.writeheader()
                writer.writerows(dataset)
            logger.info(f"Saved {len(dataset)} records to {output_path}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")


def main():
    """Main function to generate synthetic dataset."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    generator = SyntheticKundaliGenerator(
        api_url="http://localhost:8000",
        batch_size=100
    )

    # Generate 10,000 synthetic records
    dataset = generator.generate_dataset(
        num_records=10000,
        output_file='server/ml/training_data.csv'
    )

    print(f"\n✓ Generated {len(dataset)} records")
    print(f"✓ Dataset saved to server/ml/training_data.csv")


if __name__ == "__main__":
    main()
