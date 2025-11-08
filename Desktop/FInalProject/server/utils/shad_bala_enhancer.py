"""
Enhanced Shad Bala Service
Calculates yoga information and house lord strengths to complement base Shad Bala.
"""

import logging
from typing import Dict, List, Any, Tuple
from server.pydantic_schemas.kundali_schema import YogaInfo, YogaAnalysis, HouseLordStrength
from server.utils.astro_utils import get_zodiac_sign, get_ruling_planet

logger = logging.getLogger(__name__)


class EnhancedShadBalaCalculator:
    """
    Calculates yoga analysis and house lord strengths to enhance base Shad Bala.
    """

    # House lords based on ascendant sign
    HOUSE_LORDS = {
        1: "Ascendant",  # 1st house lord is always the ascendant sign lord
        2: "2nd House", 3: "3rd House", 4: "4th House", 5: "5th House", 6: "6th House",
        7: "7th House", 8: "8th House", 9: "9th House", 10: "10th House", 11: "11th House",
        12: "12th House"
    }

    def __init__(self, ascendant_degree: float, planet_positions: Dict[str, float],
                 house_assignments: Dict[int, List[str]]):
        """
        Initialize with chart data.

        Args:
            ascendant_degree: Ascendant degree (0-360)
            planet_positions: Dict of planet longitudes
            house_assignments: Dict of planets in each house
        """
        self.ascendant_degree = ascendant_degree
        self.planet_positions = planet_positions
        self.house_assignments = house_assignments
        self.asc_sign = get_zodiac_sign(ascendant_degree)

    def calculate_house_lord_strengths(self, planetary_strengths: Dict[str, Dict]) -> Dict[int, HouseLordStrength]:
        """
        Calculate strength of each house lord.

        Args:
            planetary_strengths: Dict with strength data for each planet

        Returns:
            Dict mapping house number to HouseLordStrength
        """
        house_lord_strengths = {}

        try:
            for house_num in range(1, 13):
                # Calculate house sign
                house_sign_num = ((int(self.ascendant_degree / 30)) + house_num - 1) % 12
                house_sign_names = [
                    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
                ]
                house_sign = house_sign_names[house_sign_num]

                # Get house lord
                house_lord = get_ruling_planet(house_sign)

                # Get house lord's strength
                strength_data = planetary_strengths.get(house_lord, {})
                strength_percentage = strength_data.get('strength_percentage', 50.0)

                # Determine status
                if strength_percentage >= 70:
                    status = "Strong"
                elif strength_percentage >= 45:
                    status = "Moderate"
                else:
                    status = "Weak"

                house_lord_strengths[house_num] = HouseLordStrength(
                    house=house_num,
                    lord=house_lord,
                    strength_percentage=float(strength_percentage),
                    status=status
                )

        except Exception as e:
            logger.warning(f"Error calculating house lord strengths: {str(e)}")

        return house_lord_strengths

    def calculate_yogas(self, planetary_strengths: Dict[str, Dict]) -> YogaInfo:
        """
        Identify important yogas in the chart.

        Args:
            planetary_strengths: Dict with strength data for each planet

        Returns:
            YogaInfo with yoga counts
        """
        yogas_list = []
        benefic_count = 0
        malefic_count = 0
        neutral_count = 0

        try:
            # Common yogas to check
            yoga_rules = [
                self._check_raj_yoga,
                self._check_dhana_yoga,
                self._check_parivartana_yoga,
                self._check_gajakesari_yoga,
                self._check_neecha_bhanga_yoga
            ]

            for yoga_checker in yoga_rules:
                yoga_result = yoga_checker(planetary_strengths)
                if yoga_result:
                    yoga_name, is_benefic, planets = yoga_result
                    yogas_list.append(YogaAnalysis(
                        yoga_name=yoga_name,
                        planets=planets,
                        strength=75.0,  # Simplified strength
                        benefic=is_benefic
                    ))

                    if is_benefic:
                        benefic_count += 1
                    else:
                        neutral_count += 1

        except Exception as e:
            logger.warning(f"Error identifying yogas: {str(e)}")

        total_count = benefic_count + malefic_count + neutral_count

        return YogaInfo(
            total_yoga_count=total_count,
            benefic_yoga_count=benefic_count,
            malefic_yoga_count=malefic_count,
            neutral_yoga_count=neutral_count,
            yogas=yogas_list if yogas_list else None
        )

    def _check_raj_yoga(self, planetary_strengths: Dict[str, Dict]) -> Tuple[str, bool, List[str]]:
        """Check for Raj Yoga (lords of kendra and trikona in good relationship)."""
        # Simplified check - just see if Jupiter and Saturn are both strong
        jupiter_strength = planetary_strengths.get('Jupiter', {}).get('strength_percentage', 0)
        sun_strength = planetary_strengths.get('Sun', {}).get('strength_percentage', 0)

        if jupiter_strength > 60 and sun_strength > 60:
            return ("Raj Yoga", True, ["Jupiter", "Sun"])
        return None

    def _check_dhana_yoga(self, planetary_strengths: Dict[str, Dict]) -> Tuple[str, bool, List[str]]:
        """Check for Dhana Yoga (lords of 2nd and 11th in good condition)."""
        venus_strength = planetary_strengths.get('Venus', {}).get('strength_percentage', 0)
        mercury_strength = planetary_strengths.get('Mercury', {}).get('strength_percentage', 0)

        if venus_strength > 65 and mercury_strength > 65:
            return ("Dhana Yoga", True, ["Venus", "Mercury"])
        return None

    def _check_parivartana_yoga(self, planetary_strengths: Dict[str, Dict]) -> Tuple[str, bool, List[str]]:
        """Check for Parivartana Yoga (mutual exchange of houses)."""
        # Simplified - just check if two benefics are in good condition
        venus_strength = planetary_strengths.get('Venus', {}).get('strength_percentage', 0)
        jupiter_strength = planetary_strengths.get('Jupiter', {}).get('strength_percentage', 0)

        if venus_strength > 70 and jupiter_strength > 70:
            return ("Parivartana Yoga", True, ["Venus", "Jupiter"])
        return None

    def _check_gajakesari_yoga(self, planetary_strengths: Dict[str, Dict]) -> Tuple[str, bool, List[str]]:
        """Check for Gaja Kesari Yoga (Jupiter and Moon)."""
        jupiter_strength = planetary_strengths.get('Jupiter', {}).get('strength_percentage', 0)
        moon_strength = planetary_strengths.get('Moon', {}).get('strength_percentage', 0)

        if jupiter_strength > 65 and moon_strength > 65:
            return ("Gaja Kesari Yoga", True, ["Jupiter", "Moon"])
        return None

    def _check_neecha_bhanga_yoga(self, planetary_strengths: Dict[str, Dict]) -> Tuple[str, bool, List[str]]:
        """Check for Neecha Bhanga Yoga (Cancellation of debilitation)."""
        # If a weak planet gets support from strong planets
        weak_planets = [p for p, d in planetary_strengths.items() if d.get('strength_percentage', 0) < 35]

        if len(weak_planets) > 0:
            strong_support = [p for p, d in planetary_strengths.items() if d.get('strength_percentage', 0) > 75]
            if len(strong_support) >= 2:
                return ("Neecha Bhanga Yoga", True, strong_support[:2])

        return None

    def calculate_aspect_strengths(self) -> Dict[int, float]:
        """
        Calculate aspect strengths between planets.

        Returns:
            Dict with aspect strength values
        """
        aspect_strengths = {}

        try:
            positions = self.planet_positions
            planets = list(positions.keys())
            aspect_count = 0

            # Major aspects: 0°, 60°, 90°, 120°, 180°
            aspect_degrees = [0, 60, 90, 120, 180]
            orb = 8

            for i in range(len(planets)):
                for j in range(i + 1, len(planets)):
                    pos1 = positions[planets[i]]
                    pos2 = positions[planets[j]]

                    # Calculate angular distance
                    diff = abs(pos1 - pos2)
                    if diff > 180:
                        diff = 360 - diff

                    # Check for aspects
                    for aspect_deg in aspect_degrees:
                        if abs(diff - aspect_deg) <= orb:
                            strength = max(0, 100 * (1 - abs(diff - aspect_deg) / orb))
                            aspect_count += 1
                            aspect_strengths[aspect_count] = strength
                            break

            # Pad with zeros if needed
            while len(aspect_strengths) < 6:
                aspect_strengths[len(aspect_strengths) + 1] = 0.0

        except Exception as e:
            logger.warning(f"Error calculating aspect strengths: {str(e)}")
            aspect_strengths = {i: 0.0 for i in range(1, 7)}

        return aspect_strengths