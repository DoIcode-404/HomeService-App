"""
Vedic Aspects Calculator Module
Implements Vedic astrology aspects (Graha Drishti) - different from Western aspects.

In Vedic astrology:
- All planets aspect the 7th house
- Some planets have special aspects (Mars, Jupiter, Saturn)
- Aspects are based on house positions, not degrees

Author: Astrology Backend
"""

from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class VedicAspectsCalculator:
    """
    Calculate Vedic planetary aspects (Graha Drishti).

    Standard Aspect:
    - All planets aspect the 7th house from their position

    Special Aspects:
    - Mars: aspects 4th, 8th, and 7th houses
    - Jupiter: aspects 5th, 9th, and 7th houses
    - Saturn: aspects 3rd, 10th, and 7th houses
    """

    # Planet special aspect configurations
    SPECIAL_ASPECTS = {
        'Mars': {
            'aspects': [4, 8, 7],
            'description': 'Mars has special aspects to 4th, 8th, and 7th houses'
        },
        'Jupiter': {
            'aspects': [5, 9, 7],
            'description': 'Jupiter has special aspects to 5th, 9th, and 7th houses'
        },
        'Saturn': {
            'aspects': [3, 10, 7],
            'description': 'Saturn has special aspects to 3rd, 10th, and 7th houses'
        }
    }

    def __init__(self, planets_info: Dict[str, Dict], ascendant_degree: float):
        """
        Initialize Vedic Aspects Calculator.

        Args:
            planets_info: Dictionary with planet details including house positions
            ascendant_degree: Ascendant degree for house calculations
        """
        self.planets_info = planets_info
        self.ascendant_degree = ascendant_degree

    def get_standard_aspects(self, planet: str) -> List[int]:
        """
        Get standard aspect houses for a planet (7th house aspect).

        Args:
            planet: Planet name

        Returns:
            List of houses this planet aspects
        """
        # All planets aspect the 7th house
        planet_house = self.planets_info.get(planet, {}).get('house', 1)
        seventh_aspect = ((planet_house - 1 + 6) % 12) + 1  # 7th house from planet
        return [seventh_aspect]

    def get_special_aspects(self, planet: str) -> List[int]:
        """
        Get special aspect houses for specific planets.

        Args:
            planet: Planet name

        Returns:
            List of special aspect houses (or empty if no special aspects)
        """
        if planet in self.SPECIAL_ASPECTS:
            planet_house = self.planets_info.get(planet, {}).get('house', 1)
            special_config = self.SPECIAL_ASPECTS[planet]
            special_aspects = special_config['aspects']

            # Convert relative aspects to actual houses
            return [(planet_house - 1 + aspect) % 12 + 1 for aspect in special_aspects]

        return []

    def get_all_aspects_for_planet(self, planet: str) -> Dict[str, List[int]]:
        """
        Get all aspects (standard and special) for a planet.

        Args:
            planet: Planet name

        Returns:
            Dictionary with 'standard' and 'special' aspect houses
        """
        return {
            'standard': self.get_standard_aspects(planet),
            'special': self.get_special_aspects(planet)
        }

    def calculate_aspect_relationships(self) -> Dict[str, List[Dict]]:
        """
        Calculate all aspect relationships between planets and houses.

        Returns:
            Dictionary with relationship types and details:
            {
                'conjunctions': [...],  # Planets in same house
                'oppositions': [...],   # 7 houses apart
                'trines': [...],        # 5/9 houses apart
                'squares': [...],       # 4/8 houses apart
                'sextiles': [...]       # 2/10 houses apart
            }
        """
        relationships = {
            'conjunctions': [],
            'oppositions': [],
            'trines': [],
            'squares': [],
            'sextiles': [],
            'vedic_aspects': []
        }

        try:
            planets_list = list(self.planets_info.keys())

            # Calculate conjunction and other relationships
            for i, planet1 in enumerate(planets_list):
                house1 = self.planets_info[planet1].get('house', 1)

                for planet2 in planets_list[i + 1:]:
                    house2 = self.planets_info[planet2].get('house', 1)
                    house_diff = abs(house2 - house1)

                    # Normalize difference (min distance)
                    if house_diff > 6:
                        house_diff = 12 - house_diff

                    relationship = {
                        'planet1': planet1,
                        'planet2': planet2,
                        'house1': house1,
                        'house2': house2,
                        'house_difference': house_diff
                    }

                    if house_diff == 0:
                        relationships['conjunctions'].append(relationship)
                    elif house_diff == 6:
                        relationships['oppositions'].append(relationship)
                    elif house_diff in [3, 9]:
                        relationships['trines'].append(relationship)
                    elif house_diff in [4, 8]:
                        relationships['squares'].append(relationship)
                    elif house_diff in [2, 10]:
                        relationships['sextiles'].append(relationship)

            # Calculate Vedic aspects
            vedic_aspects = self._calculate_vedic_aspect_matrix()
            relationships['vedic_aspects'] = vedic_aspects

        except Exception as e:
            logger.error(f"Error calculating aspect relationships: {str(e)}", exc_info=True)

        return relationships

    def _calculate_vedic_aspect_matrix(self) -> List[Dict]:
        """
        Create a matrix of Vedic aspects between planets and houses.

        Returns:
            List of aspect dictionaries
        """
        vedic_aspects = []

        try:
            for planet in self.planets_info.keys():
                standard_aspects = self.get_standard_aspects(planet)
                special_aspects = self.get_special_aspects(planet)

                aspect_entry = {
                    'planet': planet,
                    'houses_aspected': {
                        'standard': standard_aspects,
                        'special': special_aspects
                    },
                    'total_houses_aspected': len(set(standard_aspects + special_aspects)),
                    'aspect_strength': 'strong' if special_aspects else 'normal'
                }

                vedic_aspects.append(aspect_entry)

        except Exception as e:
            logger.error(f"Error calculating Vedic aspect matrix: {str(e)}", exc_info=True)

        return vedic_aspects

    def get_aspects_to_house(self, house: int) -> List[Dict]:
        """
        Get all planets that aspect a specific house.

        Args:
            house: House number (1-12)

        Returns:
            List of planets aspecting this house with aspect details
        """
        aspects_to_house = []

        try:
            for planet in self.planets_info.keys():
                standard_aspects = self.get_standard_aspects(planet)
                special_aspects = self.get_special_aspects(planet)
                all_aspects = standard_aspects + special_aspects

                if house in all_aspects:
                    aspect_type = 'special' if house in special_aspects else 'standard'
                    aspects_to_house.append({
                        'planet': planet,
                        'aspect_type': aspect_type,
                        'description': self.SPECIAL_ASPECTS.get(
                            planet, {}
                        ).get('description', f'{planet} aspects house {house}')
                    })

        except Exception as e:
            logger.error(f"Error getting aspects to house {house}: {str(e)}", exc_info=True)

        return aspects_to_house

    def get_benefic_aspects(self) -> List[Dict]:
        """
        Identify benefic planetary aspects.

        Returns:
            List of benefic aspect configurations
        """
        benefic_planets = ['Sun', 'Moon', 'Jupiter', 'Venus', 'Mercury']
        benefic_aspects = []

        try:
            for planet in benefic_planets:
                if planet in self.planets_info:
                    standard_aspects = self.get_standard_aspects(planet)
                    special_aspects = self.get_special_aspects(planet)

                    benefic_aspects.append({
                        'planet': planet,
                        'aspect_type': 'benefic',
                        'aspected_houses': standard_aspects + special_aspects,
                        'benefit': f'Positive influence from {planet}'
                    })

        except Exception as e:
            logger.error(f"Error calculating benefic aspects: {str(e)}", exc_info=True)

        return benefic_aspects

    def get_malefic_aspects(self) -> List[Dict]:
        """
        Identify malefic planetary aspects.

        Returns:
            List of malefic aspect configurations
        """
        malefic_planets = ['Mars', 'Saturn', 'Rahu', 'Ketu']
        malefic_aspects = []

        try:
            for planet in malefic_planets:
                if planet in self.planets_info:
                    standard_aspects = self.get_standard_aspects(planet)
                    special_aspects = self.get_special_aspects(planet)

                    malefic_aspects.append({
                        'planet': planet,
                        'aspect_type': 'malefic',
                        'aspected_houses': standard_aspects + special_aspects,
                        'challenge': f'Challenging influence from {planet}'
                    })

        except Exception as e:
            logger.error(f"Error calculating malefic aspects: {str(e)}", exc_info=True)

        return malefic_aspects

    def get_strongest_aspects(self) -> List[Dict]:
        """
        Get the most significant aspects in the chart.

        Returns:
            List of strongest aspects sorted by significance
        """
        strongest = []

        try:
            # Planets with special aspects are strongest
            for planet, config in self.SPECIAL_ASPECTS.items():
                if planet in self.planets_info:
                    house = self.planets_info[planet].get('house', 1)
                    strongest.append({
                        'planet': planet,
                        'aspect_count': len(config['aspects']),
                        'special_aspects': config['aspects'],
                        'significance': 'very strong',
                        'description': config['description']
                    })

            # Sort by aspect count (descending)
            strongest.sort(key=lambda x: x['aspect_count'], reverse=True)

        except Exception as e:
            logger.error(f"Error getting strongest aspects: {str(e)}", exc_info=True)

        return strongest

    def get_complete_aspect_analysis(self) -> Dict:
        """
        Get comprehensive aspect analysis.

        Returns:
            Complete dictionary with all aspect information
        """
        try:
            return {
                'vedic_aspect_matrix': self._calculate_vedic_aspect_matrix(),
                'planet_relationships': self.calculate_aspect_relationships(),
                'benefic_aspects': self.get_benefic_aspects(),
                'malefic_aspects': self.get_malefic_aspects(),
                'strongest_aspects': self.get_strongest_aspects(),
                'house_aspects': {
                    i: self.get_aspects_to_house(i) for i in range(1, 13)
                }
            }
        except Exception as e:
            logger.error(f"Error in complete aspect analysis: {str(e)}", exc_info=True)
            return {}
