"""
Enhanced House Analysis
Provides detailed analysis of astrological houses.

Each house represents different life areas and significators.

Author: Astrology Backend
"""

import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class HouseAnalyzer:
    """
    Analyze astrological houses in detail.

    Houses represent 12 life areas, each with ruling planets and significators.
    """

    # House significators (Karakas) - Natural significators for each house
    HOUSE_SIGNIFICATORS = {
        1: {'name': 'Self', 'karakas': ['Sun'], 'areas': ['Personality', 'Health', 'Appearance']},
        2: {'name': 'Wealth', 'karakas': ['Jupiter', 'Venus'], 'areas': ['Money', 'Family', 'Speech']},
        3: {'name': 'Siblings', 'karakas': ['Mercury', 'Mars'], 'areas': ['Siblings', 'Communication', 'Courage']},
        4: {'name': 'Home', 'karakas': ['Moon', 'Venus'], 'areas': ['Mother', 'Home', 'Land', 'Property']},
        5: {'name': 'Children', 'karakas': ['Jupiter', 'Sun'], 'areas': ['Children', 'Creativity', 'Romance']},
        6: {'name': 'Health', 'karakas': ['Mars', 'Saturn'], 'areas': ['Disease', 'Enemies', 'Debt', 'Service']},
        7: {'name': 'Marriage', 'karakas': ['Venus'], 'areas': ['Partnership', 'Marriage', 'Spouse', 'Public']},
        8: {'name': 'Longevity', 'karakas': ['Saturn', 'Ketu'], 'areas': ['Death', 'Inheritance', 'Longevity', 'Occult']},
        9: {'name': 'Luck', 'karakas': ['Jupiter', 'Sun'], 'areas': ['Father', 'Luck', 'Dharma', 'Religion', 'Travel']},
        10: {'name': 'Career', 'karakas': ['Saturn', 'Sun'], 'areas': ['Career', 'Public', 'Authority', 'Honor']},
        11: {'name': 'Gains', 'karakas': ['Jupiter', 'Mercury'], 'areas': ['Income', 'Friends', 'Wishes', 'Groups']},
        12: {'name': 'Losses', 'karakas': ['Saturn', 'Ketu'], 'areas': ['Losses', 'Spirituality', 'Seclusion', 'Foreign']}
    }

    # House friends and enemies
    PLANET_HOUSE_STRENGTH = {
        'Sun': [1, 5, 9, 10],          # Strong in these houses
        'Moon': [1, 4, 7, 10],
        'Mars': [1, 3, 6, 8, 10, 11],
        'Mercury': [1, 2, 6, 8],
        'Jupiter': [1, 2, 5, 9, 10, 11],
        'Venus': [2, 4, 7, 12],
        'Saturn': [1, 6, 8, 10, 11, 12],
        'Rahu': [3, 6, 8, 9, 11, 12],
        'Ketu': [3, 6, 8, 9, 11, 12]
    }

    def __init__(self, planets_info: Dict, houses: Dict, ascendant_sign: str):
        """
        Initialize House Analyzer.

        Args:
            planets_info: Planet positions and details
            houses: House information with signs and planets
            ascendant_sign: Ascendant zodiac sign
        """
        self.planets_info = planets_info
        self.houses = houses
        self.ascendant_sign = ascendant_sign

    def analyze_all_houses(self) -> Dict:
        """
        Analyze all 12 houses.

        Returns:
            Dictionary with detailed analysis for each house
        """
        try:
            house_analysis = {}

            for house_num in range(1, 13):
                house_analysis[house_num] = self.analyze_single_house(house_num)

            return house_analysis

        except Exception as e:
            logger.error(f"Error analyzing all houses: {str(e)}")
            return {}

    def analyze_single_house(self, house_num: int) -> Dict:
        """
        Analyze a single house.

        Args:
            house_num: House number (1-12)

        Returns:
            Dictionary with house analysis
        """
        try:
            if house_num < 1 or house_num > 12:
                return {}

            house_data = self.houses.get(house_num, {})
            significator_info = self.HOUSE_SIGNIFICATORS.get(house_num, {})
            house_sign = house_data.get('sign', '') if isinstance(house_data, dict) else ''
            planets_in_house = house_data.get('planets', []) if isinstance(house_data, dict) else []

            analysis = {
                'house_number': house_num,
                'house_name': significator_info.get('name', ''),
                'sign': house_sign,
                'areas': significator_info.get('areas', []),
                'significators': significator_info.get('karakas', []),
                'planets': planets_in_house,
                'strength': self._calculate_house_strength(house_num, planets_in_house),
                'lord': self._get_house_lord(house_num, house_sign),
                'lord_strength': self._get_house_lord_strength(house_num, house_sign),
                'interpretation': self._get_house_interpretation(
                    house_num, house_sign, planets_in_house
                ),
                'quality': self._determine_house_quality(house_num, planets_in_house),
                'remedies': self._get_house_remedies(house_num, planets_in_house)
            }

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing house {house_num}: {str(e)}")
            return {}

    def _get_house_lord(self, house_num: int, sign: str) -> str:
        """
        Get the lord (ruler) of a house based on its sign.

        Args:
            house_num: House number
            sign: Zodiac sign in that house

        Returns:
            Planet name that rules this sign
        """
        sign_rulers = {
            'Aries': 'Mars',
            'Taurus': 'Venus',
            'Gemini': 'Mercury',
            'Cancer': 'Moon',
            'Leo': 'Sun',
            'Virgo': 'Mercury',
            'Libra': 'Venus',
            'Scorpio': 'Mars',
            'Sagittarius': 'Jupiter',
            'Capricorn': 'Saturn',
            'Aquarius': 'Saturn',
            'Pisces': 'Jupiter'
        }
        return sign_rulers.get(sign, 'Unknown')

    def _get_house_lord_strength(self, house_num: int, sign: str) -> str:
        """
        Get the strength of the house lord.

        Args:
            house_num: House number
            sign: Sign in that house

        Returns:
            Strength assessment string
        """
        lord = self._get_house_lord(house_num, sign)

        if lord in self.planets_info:
            planet_data = self.planets_info[lord]
            if isinstance(planet_data, dict):
                # Check if lord is in strong position
                planet_house = planet_data.get('house', 0)
                planet_sign = planet_data.get('sign', '')

                # Lord in own sign or exalted sign = very strong
                if self._is_lord_in_own_sign(lord, planet_sign):
                    return 'Very Strong'
                elif self._is_lord_in_exalted_sign(lord, planet_sign):
                    return 'Very Strong'
                # Lord in strong house
                elif planet_house in self.PLANET_HOUSE_STRENGTH.get(lord, []):
                    return 'Strong'
                else:
                    return 'Moderate'

        return 'Unknown'

    def _is_lord_in_own_sign(self, planet: str, sign: str) -> bool:
        """Check if planet is in its own sign."""
        own_signs = {
            'Sun': 'Leo',
            'Moon': 'Cancer',
            'Mars': ['Aries', 'Scorpio'],
            'Mercury': ['Gemini', 'Virgo'],
            'Jupiter': ['Sagittarius', 'Pisces'],
            'Venus': ['Taurus', 'Libra'],
            'Saturn': ['Capricorn', 'Aquarius'],
        }

        own = own_signs.get(planet, [])
        if isinstance(own, list):
            return sign in own
        else:
            return sign == own

    def _is_lord_in_exalted_sign(self, planet: str, sign: str) -> bool:
        """Check if planet is in its exalted sign."""
        exalted_signs = {
            'Sun': 'Aries',
            'Moon': 'Taurus',
            'Mars': 'Capricorn',
            'Mercury': 'Virgo',
            'Jupiter': 'Cancer',
            'Venus': 'Pisces',
            'Saturn': 'Libra',
            'Rahu': 'Gemini',
            'Ketu': 'Sagittarius'
        }

        return exalted_signs.get(planet) == sign

    def _calculate_house_strength(self, house_num: int, planets_in_house: List[str]) -> str:
        """
        Calculate overall house strength.

        Args:
            house_num: House number
            planets_in_house: List of planets in this house

        Returns:
            Strength assessment
        """
        if not planets_in_house:
            return 'Weak (No planets)'

        # Count strong planets in this house
        strong_count = 0
        for planet in planets_in_house:
            if self._is_planet_strong_in_house(planet, house_num):
                strong_count += 1

        if strong_count >= 2:
            return 'Very Strong'
        elif strong_count == 1:
            return 'Strong'
        elif len(planets_in_house) > 0:
            return 'Moderate'
        else:
            return 'Weak'

    def _is_planet_strong_in_house(self, planet: str, house_num: int) -> bool:
        """Check if a planet is strong in a given house."""
        return house_num in self.PLANET_HOUSE_STRENGTH.get(planet, [])

    def _get_house_interpretation(self, house_num: int, sign: str,
                                  planets_in_house: List[str]) -> str:
        """
        Get interpretation for a house.

        Args:
            house_num: House number
            sign: Sign in house
            planets_in_house: List of planets in house

        Returns:
            Interpretation string
        """
        significator = self.HOUSE_SIGNIFICATORS.get(house_num, {})
        house_name = significator.get('name', '')
        areas = ', '.join(significator.get('areas', []))

        interpretation = f"House {house_num} ({house_name}) is in {sign} sign. "
        interpretation += f"It rules: {areas}. "

        if planets_in_house:
            interpretation += f"Planets in this house: {', '.join(planets_in_house)}. "
            interpretation += "This strengthens the matters of this house."
        else:
            interpretation += "No planets in this house - rely on house lord strength."

        return interpretation

    def _determine_house_quality(self, house_num: int, planets_in_house: List[str]) -> str:
        """
        Determine overall quality (benefic/malefic) of a house.

        Args:
            house_num: House number
            planets_in_house: List of planets

        Returns:
            Quality assessment
        """
        benefic_planets = ['Sun', 'Moon', 'Jupiter', 'Venus', 'Mercury']
        malefic_planets = ['Mars', 'Saturn', 'Rahu', 'Ketu']

        benefic_count = sum(1 for p in planets_in_house if p in benefic_planets)
        malefic_count = sum(1 for p in planets_in_house if p in malefic_planets)

        if benefic_count > malefic_count:
            return 'Benefic (Favorable)'
        elif malefic_count > benefic_count:
            return 'Malefic (Challenging)'
        else:
            return 'Neutral (Balanced)'

    def _get_house_remedies(self, house_num: int, planets_in_house: List[str]) -> List[str]:
        """
        Get remedies for house issues.

        Args:
            house_num: House number
            planets_in_house: Planets in house

        Returns:
            List of remedy suggestions
        """
        remedies = []
        significator = self.HOUSE_SIGNIFICATORS.get(house_num, {})
        house_name = significator.get('name', '')

        if not planets_in_house:
            remedies.append(f"Strengthen {house_name} house by worshipping its significator")

        # Specific remedies by house
        house_remedies = {
            1: "Practice self-improvement and build confidence",
            2: "Develop financial discipline and generosity",
            3: "Improve communication and build relationships with siblings",
            4: "Strengthen home and family bonds",
            5: "Engage in creative pursuits and fertility remedies if needed",
            6: "Focus on health and avoiding enemies",
            7: "Nurture relationships and partnerships",
            8: "Engage in spiritual practices for longevity",
            9: "Study and travel for luck and dharma",
            10: "Build career and professional reputation",
            11: "Network and pursue financial gains",
            12: "Engage in charity and spiritual practices"
        }

        if house_num in house_remedies:
            remedies.append(house_remedies[house_num])

        return remedies

    def get_house_lords_analysis(self) -> Dict:
        """
        Get comprehensive analysis of all house lords.

        Returns:
            Dictionary with house lord analysis
        """
        try:
            lords_analysis = {}

            for house_num in range(1, 13):
                house_data = self.houses.get(house_num, {})
                house_sign = house_data.get('sign', '') if isinstance(house_data, dict) else ''
                lord = self._get_house_lord(house_num, house_sign)

                lords_analysis[house_num] = {
                    'house': house_num,
                    'lord': lord,
                    'sign_in_house': house_sign,
                    'lord_position': self._get_planet_position(lord),
                    'strength': self._get_house_lord_strength(house_num, house_sign),
                    'aspects': self._get_lord_aspects(lord),
                    'conjunction': self._get_lord_conjunctions(lord)
                }

            return lords_analysis

        except Exception as e:
            logger.error(f"Error analyzing house lords: {str(e)}")
            return {}

    def _get_planet_position(self, planet: str) -> str:
        """Get position of a planet."""
        if planet in self.planets_info:
            planet_data = self.planets_info[planet]
            if isinstance(planet_data, dict):
                sign = planet_data.get('sign', 'Unknown')
                house = planet_data.get('house', 0)
                return f"{sign} in House {house}"

        return "Unknown"

    def _get_lord_aspects(self, planet: str) -> List[str]:
        """Get aspects of a house lord."""
        aspects = []
        # This would be filled in by the aspects calculator
        return aspects

    def _get_lord_conjunctions(self, planet: str) -> List[str]:
        """Get conjunctions of a house lord."""
        conjunctions = []
        # This would be filled in with actual planet positions
        return conjunctions

    def get_house_strength_summary(self) -> Dict:
        """
        Get summary of overall house strength.

        Returns:
            Summary dictionary
        """
        try:
            all_houses = self.analyze_all_houses()

            strong_houses = [h for h in range(1, 13)
                           if all_houses.get(h, {}).get('strength', '').startswith('Strong')]
            weak_houses = [h for h in range(1, 13)
                         if all_houses.get(h, {}).get('strength', '').startswith('Weak')]

            return {
                'strong_houses': strong_houses,
                'weak_houses': weak_houses,
                'total_houses': 12,
                'summary': f"{len(strong_houses)} strong houses, {len(weak_houses)} weak houses",
                'overall_assessment': self._get_overall_house_assessment(strong_houses, weak_houses)
            }

        except Exception as e:
            logger.error(f"Error getting house strength summary: {str(e)}")
            return {}

    def _get_overall_house_assessment(self, strong: List[int], weak: List[int]) -> str:
        """Get overall assessment of house strength."""
        if len(strong) > 8:
            return "Very Strong Chart - Most life areas well-supported"
        elif len(strong) > 6:
            return "Strong Chart - Good support in major life areas"
        elif len(strong) > 4:
            return "Moderate Chart - Mixed support across life areas"
        else:
            return "Weak Chart - Focus on remedies for weak areas"
