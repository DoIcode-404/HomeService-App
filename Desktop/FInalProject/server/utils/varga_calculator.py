"""
Divisional Charts (Vargas) Calculator
Implements divisional charts for deeper astrological analysis.

Vargas are different divisions of the zodiac that show specific life areas.

Key Divisions:
- D1 (Rasi): Basic birth chart
- D2 (Hora): Wealth and finance (2 parts)
- D3 (Drekkana): Siblings, courage (3 parts)
- D7 (Saptamsha): Children, progeny (7 parts)
- D9 (Navamsha): Marriage, hidden nature (9 parts) - MOST IMPORTANT
- D12 (Dwadashamsha): Parents, inheritance (12 parts)
- D20 (Vimsamsha): Spiritual strength (20 parts)

Author: Astrology Backend
"""

import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class VargaCalculator:
    """
    Calculate divisional charts (vargas).

    Each varga divides the zodiac into equal parts and shows specific life areas.
    """

    # Zodiac signs for reference
    SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]

    def __init__(self, planets_info: Dict[str, Dict], ascendant_degree: float):
        """
        Initialize Varga Calculator.

        Args:
            planets_info: Dictionary with planet positions
            ascendant_degree: Ascendant degree (0-360)
        """
        self.planets_info = planets_info
        self.ascendant_degree = ascendant_degree

    def calculate_all_vargas(self) -> Dict:
        """
        Calculate all important divisional charts.

        Returns:
            Dictionary with D1, D2, D7, D9 charts
        """
        try:
            return {
                'D1_Rasi': self._get_rasi_chart(),
                'D2_Hora': self.calculate_hora_chart(),
                'D7_Saptamsha': self.calculate_saptamsha_chart(),
                'D9_Navamsha': self.calculate_navamsha_chart()
            }
        except Exception as e:
            logger.error(f"Error calculating vargas: {str(e)}", exc_info=True)
            return {'error': str(e)}

    def _get_rasi_chart(self) -> Dict:
        """Get the birth chart (D1) - basic info."""
        try:
            return {
                'name': 'Rasi Chart (D1)',
                'description': 'Basic birth chart',
                'significance': 'Overall life, personality, general events',
                'planets': self.planets_info,
                'ascendant_degree': self.ascendant_degree
            }
        except Exception as e:
            logger.error(f"Error getting Rasi chart: {str(e)}")
            return {}

    def calculate_hora_chart(self) -> Dict:
        """
        Calculate Hora Chart (D2).

        Hora = 2 equal parts = 15° each
        Used for: Wealth, financial success, money matters

        Each sign has 2 horas:
        - Even signs: First half is Sun's hora, Second half is Moon's hora
        - Odd signs: First half is Moon's hora, Second half is Sun's hora
        """
        try:
            hora_chart = {
                'name': 'Hora Chart (D2)',
                'description': 'Finance and Wealth Division',
                'significance': 'Financial success, money, wealth accumulation',
                'division': 2,
                'part_size': 15,  # degrees
                'planets': {}
            }

            for planet, planet_data in self.planets_info.items():
                if not isinstance(planet_data, dict):
                    continue

                degree = planet_data.get('longitude', 0)
                sign = planet_data.get('sign')

                # Calculate hora
                hora_number, hora_lord = self._calculate_hora(degree, sign)

                hora_chart['planets'][planet] = {
                    'original_degree': degree,
                    'original_sign': sign,
                    'hora_sign': hora_lord,
                    'hora_number': hora_number,
                    'hour': hora_lord
                }

            hora_chart['ascendant'] = self._calculate_varga_ascendant(
                self.ascendant_degree, 2
            )

            return hora_chart

        except Exception as e:
            logger.error(f"Error calculating Hora chart: {str(e)}")
            return {}

    def _calculate_hora(self, degree: float, sign: Optional[str]) -> Tuple[int, str]:
        """
        Calculate Hora for a given degree.

        Args:
            degree: Longitude in degrees (0-360)
            sign: Zodiac sign

        Returns:
            Tuple of (hora_number: 1-2, hora_sign: lord name)
        """
        degree = degree % 360
        sign_number = int(degree / 30)  # 0-11

        # Position within the sign (0-30)
        position_in_sign = degree % 30

        # Each sign is divided into 2 horas (15° each)
        if position_in_sign < 15:
            hora_num = 1
        else:
            hora_num = 2

        # Hora lords (Sun for even horas starting first, Moon alternating)
        # Simplified: 1st hora of each sign has a lord
        if sign_number % 2 == 0:  # Even signs (Aries, Gemini, etc.)
            hora_lord = 'Sun' if hora_num == 1 else 'Moon'
        else:  # Odd signs
            hora_lord = 'Moon' if hora_num == 1 else 'Sun'

        return hora_num, hora_lord

    def calculate_saptamsha_chart(self) -> Dict:
        """
        Calculate Saptamsha Chart (D7).

        Saptamsha = 7 equal parts = 4.286° each
        Used for: Children, progeny, fertility, offspring

        Provides insights into:
        - Number and nature of children
        - Fertility and reproductive capacity
        - Character development of children
        """
        try:
            saptamsha_chart = {
                'name': 'Saptamsha Chart (D7)',
                'description': 'Children and Progeny Division',
                'significance': 'Children, progeny, fertility, reproductive health',
                'division': 7,
                'part_size': 30 / 7,  # ~4.286 degrees
                'planets': {}
            }

            for planet, planet_data in self.planets_info.items():
                if not isinstance(planet_data, dict):
                    continue

                degree = planet_data.get('longitude', 0)
                sign = planet_data.get('sign')

                # Calculate which saptamsha this planet falls into
                saptamsha_num = self._calculate_saptamsha_number(degree)
                saptamsha_sign = self._calculate_saptamsha_sign(degree, sign)

                saptamsha_chart['planets'][planet] = {
                    'original_degree': degree,
                    'original_sign': sign,
                    'saptamsha_number': saptamsha_num,
                    'saptamsha_sign': saptamsha_sign,
                    'interpretation': self._get_saptamsha_interpretation(saptamsha_num)
                }

            saptamsha_chart['ascendant'] = self._calculate_varga_ascendant(
                self.ascendant_degree, 7
            )

            saptamsha_chart['fertility_analysis'] = self._analyze_saptamsha_fertility()

            return saptamsha_chart

        except Exception as e:
            logger.error(f"Error calculating Saptamsha chart: {str(e)}")
            return {}

    def _calculate_saptamsha_number(self, degree: float) -> int:
        """Calculate which saptamsha a degree falls into (0-6)."""
        degree = degree % 360
        saptamsha_size = 360 / 7  # ~51.43°
        return int(degree / saptamsha_size)

    def _calculate_saptamsha_sign(self, degree: float, sign: Optional[str]) -> str:
        """Calculate saptamsha sign."""
        degree = degree % 30  # Position in sign
        saptamsha_in_sign = int((degree / 30) * 7)
        sign_num = int(degree / 30)

        # Map to sign
        return self.SIGNS[sign_num % 12]

    def _get_saptamsha_interpretation(self, saptamsha_num: int) -> str:
        """Get interpretation for saptamsha position."""
        interpretations = [
            "Weak children - needs special care",
            "Average children - moderate support needed",
            "Good children - positive influence",
            "Excellent children - very favorable",
            "Very strong progeny - highly beneficial",
            "Extraordinary children - exceptional benefits",
            "Highly auspicious for children"
        ]
        return interpretations[saptamsha_num % 7]

    def calculate_navamsha_chart(self) -> Dict:
        """
        Calculate Navamsha Chart (D9).

        Navamsha = 9 equal parts = 3.333° each
        Used for: Marriage, partnerships, hidden qualities, marital life

        Most important divisional chart:
        - Shows marriage and partnership potential
        - Reveals hidden strengths and weaknesses
        - Indicates spiritual development
        - Marriage compatibility matching
        """
        try:
            navamsha_chart = {
                'name': 'Navamsha Chart (D9)',
                'description': 'Marriage and Hidden Nature Division',
                'significance': 'Marriage, partnerships, hidden strengths, spiritual nature',
                'division': 9,
                'part_size': 30 / 9,  # 3.333 degrees
                'planets': {}
            }

            for planet, planet_data in self.planets_info.items():
                if not isinstance(planet_data, dict):
                    continue

                degree = planet_data.get('longitude', 0)
                sign = planet_data.get('sign')

                # Calculate navamsha
                navamsha_num, navamsha_sign = self._calculate_navamsha(degree, sign)

                navamsha_chart['planets'][planet] = {
                    'original_degree': degree,
                    'original_sign': sign,
                    'navamsha_number': navamsha_num,
                    'navamsha_sign': navamsha_sign,
                    'pada': self._get_navamsha_pada(navamsha_num),
                    'significance': self._get_navamsha_significance(navamsha_num)
                }

            navamsha_chart['ascendant'] = self._calculate_varga_ascendant(
                self.ascendant_degree, 9
            )

            navamsha_chart['marriage_analysis'] = self._analyze_navamsha_marriage()
            navamsha_chart['hidden_strengths'] = self._analyze_hidden_strengths()

            return navamsha_chart

        except Exception as e:
            logger.error(f"Error calculating Navamsha chart: {str(e)}")
            return {}

    def _calculate_navamsha(self, degree: float, sign: Optional[str]) -> Tuple[int, str]:
        """
        Calculate Navamsha position.

        Each rasi is divided into 9 equal parts = 3.333° per navamsha
        Each navamsha corresponds to a sign

        Args:
            degree: Longitude (0-360)
            sign: Zodiac sign

        Returns:
            Tuple of (navamsha_number: 0-8, navamsha_sign: sign name)
        """
        degree = degree % 360
        sign_num = int(degree / 30)  # 0-11
        position_in_sign = degree % 30  # 0-30

        # Each sign divided into 9 navaamsas
        navamsha_in_sign = int((position_in_sign / 30) * 9)  # 0-8

        # Navamsha signs follow a specific pattern
        # Starting from Aries for the first navamsha of Aries
        navamsha_absolute = (sign_num * 9) + navamsha_in_sign  # 0-107
        navamsha_sign_num = (navamsha_absolute) % 12

        return navamsha_in_sign, self.SIGNS[navamsha_sign_num]

    def _get_navamsha_pada(self, navamsha_num: int) -> int:
        """Get pada (quarter) of navamsha."""
        return (navamsha_num % 9) // 3 + 1

    def _get_navamsha_significance(self, navamsha_num: int) -> str:
        """Get significance of navamsha position."""
        significances = [
            "Strong marriage potential - very auspicious",
            "Good partnerships - favorable for alliances",
            "Moderate marriage stability - needs care",
            "Blessed in relationships - harmony expected",
            "Excellent marital life - highly favored",
            "Strong partnership bonds - deep commitment",
            "Spiritual partnership - soulmate potential",
            "Harmonious relationships - mutual understanding",
            "Transformed through partnerships - growth"
        ]
        return significances[navamsha_num % 9]

    def _calculate_varga_ascendant(self, ascendant_degree: float, division: int) -> str:
        """
        Calculate divisional chart ascendant.

        Args:
            ascendant_degree: Original ascendant degree
            division: Varga division (2, 7, 9, etc.)

        Returns:
            Divisional chart ascendant sign
        """
        varga_ascendant = ascendant_degree * division
        varga_ascendant = varga_ascendant % 360

        sign_num = int(varga_ascendant / 30)
        return self.SIGNS[sign_num % 12]

    def _analyze_navamsha_marriage(self) -> Dict:
        """Analyze marriage potential from Navamsha."""
        venus_nav = self.planets_info.get('Venus', {})
        moon_nav = self.planets_info.get('Moon', {})

        return {
            'venus_position': venus_nav.get('navamsha_sign') if isinstance(venus_nav, dict) else None,
            'moon_position': moon_nav.get('navamsha_sign') if isinstance(moon_nav, dict) else None,
            'marriage_timing': self._predict_marriage_timing(),
            'partnership_quality': self._assess_partnership_quality()
        }

    def _analyze_hidden_strengths(self) -> List[str]:
        """Analyze hidden strengths from Navamsha."""
        strengths = [
            "Navamsha reveals hidden talents and abilities",
            "Shows spiritual nature and inner character",
            "Indicates potential in relationships",
            "Reveals life purpose at deeper level"
        ]
        return strengths

    def _analyze_saptamsha_fertility(self) -> Dict:
        """Analyze fertility from Saptamsha."""
        return {
            'fertility_indicators': 'Based on Jupiter and Moon positions in Saptamsha',
            'progeny_count': 'Indicated by strength of 5th lord',
            'child_welfare': 'Based on benefic placements in D7'
        }

    def _predict_marriage_timing(self) -> str:
        """Predict marriage timing from chart analysis."""
        return "Timing indicated by Dasha periods and transit of Jupiter"

    def _assess_partnership_quality(self) -> str:
        """Assess quality of partnerships."""
        return "Quality determined by benefic planet positions in Navamsha"

    def get_varga_summary(self) -> Dict:
        """
        Get summary of all vargas.

        Returns:
            Summary of key varga indicators
        """
        try:
            all_vargas = self.calculate_all_vargas()

            summary = {
                'total_vargas': len(all_vargas),
                'important_vargas': {
                    'D1': 'Overall life - primary indicator',
                    'D2': 'Wealth and finance',
                    'D7': 'Children and progeny',
                    'D9': 'Marriage and hidden nature'
                },
                'd9_importance': 'Navamsha is the most important divisional chart for marriage analysis',
                'vargas': all_vargas
            }

            return summary

        except Exception as e:
            logger.error(f"Error getting varga summary: {str(e)}")
            return {}

    def compare_d1_d9_alignment(self) -> Dict:
        """
        Compare D1 (Rasi) and D9 (Navamsha) alignment.

        Strong D1 D9 alignment indicates stability.

        Returns:
            Alignment analysis
        """
        try:
            d1_chart = self._get_rasi_chart()
            d9_chart = self.calculate_navamsha_chart()

            alignment_score = 0
            details = []

            # Compare planet positions
            for planet in self.planets_info.keys():
                d1_sign = self.planets_info[planet].get('sign')
                d9_sign = d9_chart['planets'].get(planet, {}).get('navamsha_sign')

                if d1_sign and d9_sign:
                    if d1_sign == d9_sign:
                        alignment_score += 10
                        details.append(f"{planet} in same sign in D1 and D9 - Strong alignment")
                    else:
                        details.append(f"{planet} in different signs - Check compatibility")

            return {
                'alignment_score': alignment_score,
                'max_score': 90,
                'alignment_percentage': (alignment_score / 90) * 100,
                'details': details,
                'interpretation': self._interpret_alignment(alignment_score)
            }

        except Exception as e:
            logger.error(f"Error comparing D1 D9: {str(e)}")
            return {}

    def _interpret_alignment(self, score: int) -> str:
        """Interpret D1 D9 alignment score."""
        if score >= 60:
            return "Excellent alignment - Life is well-supported by hidden nature"
        elif score >= 40:
            return "Good alignment - Generally harmonious development"
        elif score >= 20:
            return "Moderate alignment - Some adjustments needed"
        else:
            return "Weak alignment - Significant differences between apparent and true nature"
