"""
Transit Calculator (Gochara)
Calculates current planetary transits and their effects on birth chart.

Transits show how current planets are moving through the birth chart,
indicating current influences and timing of life events.

Author: Astrology Backend
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from server.utils.astro_utils import calculate_planet_positions, get_zodiac_sign, get_nakshatra

logger = logging.getLogger(__name__)


class TransitCalculator:
    """
    Calculate current planetary transits and their effects.

    Transits are real-time planetary movements compared to birth chart positions.
    Each planet's transit has different significance and duration.
    """

    # Transit durations (approximate, in days)
    TRANSIT_DURATIONS = {
        'Sun': 30,           # 30 days per sign
        'Moon': 2.25,        # 2.25 days per sign
        'Mercury': 14,       # 14-30 days per sign (variable)
        'Venus': 28,         # 28 days per sign (variable)
        'Mars': 45,          # 45 days per sign
        'Jupiter': 360,      # ~1 year per sign
        'Saturn': 900,       # ~2.5 years per sign
        'Rahu': 540,         # ~1.5 years per sign
        'Ketu': 540          # ~1.5 years per sign
    }

    # Significance of transits
    TRANSIT_SIGNIFICANCE = {
        'Sun': 'General life influence',
        'Moon': 'Emotional and daily mood',
        'Mercury': 'Communication and thinking',
        'Venus': 'Relationships and finances',
        'Mars': 'Energy, courage, conflicts',
        'Jupiter': 'Expansion, luck, growth',
        'Saturn': 'Restrictions, lessons, responsibilities',
        'Rahu': 'Obsessions, new ventures, growth',
        'Ketu': 'Release, spirituality, past karma'
    }

    def __init__(self, birth_chart: Dict, transit_date: Optional[datetime] = None):
        """
        Initialize Transit Calculator.

        Args:
            birth_chart: Birth chart with planet positions and houses
            transit_date: Date to calculate transits for (default: today)
        """
        self.birth_chart = birth_chart
        self.transit_date = transit_date or datetime.now()
        self.birth_planets = birth_chart.get('planets', {})
        self.birth_houses = birth_chart.get('houses', {})

    def calculate_current_transits(self) -> Dict:
        """
        Calculate all current planetary transits.

        Returns:
            Dictionary with transit information for all planets
        """
        try:
            # Get current planet positions
            from server.utils.astro_utils import get_julian_day_from_date
            jd = get_julian_day_from_date(self.transit_date)
            current_positions = calculate_planet_positions(jd)

            transits = {}

            for planet, current_pos in current_positions.items():
                if planet not in self.birth_planets:
                    continue

                birth_pos = self.birth_planets[planet].get('longitude', 0) if isinstance(
                    self.birth_planets[planet], dict
                ) else 0

                current_sign = get_zodiac_sign(current_pos)
                birth_sign = self.birth_planets[planet].get('sign') if isinstance(
                    self.birth_planets[planet], dict
                ) else None

                transit_info = {
                    'planet': planet,
                    'current_degree': round(current_pos, 2),
                    'current_sign': current_sign,
                    'birth_degree': round(birth_pos, 2),
                    'birth_sign': birth_sign,
                    'sign_change': current_sign != birth_sign if birth_sign else False,
                    'significance': self.TRANSIT_SIGNIFICANCE.get(planet, 'Life influence'),
                    'duration_in_sign_days': self.TRANSIT_DURATIONS.get(planet, 30)
                }

                # Calculate aspects to birth planets
                transit_info['aspects_to_birth'] = self._calculate_transit_aspects(
                    planet, current_pos
                )

                # Determine transit status (benefic/malefic)
                transit_info['transit_quality'] = self._determine_transit_quality(
                    planet, current_sign, birth_sign
                )

                # Generate interpretation
                transit_info['interpretation'] = self._get_transit_interpretation(
                    planet, current_sign, birth_sign
                )

                transits[planet] = transit_info

            return transits

        except Exception as e:
            logger.error(f"Error calculating current transits: {str(e)}")
            return {}

    def _calculate_transit_aspects(self, planet: str, current_degree: float) -> List[Dict]:
        """
        Calculate aspects from transiting planet to birth planets.

        Args:
            planet: Transiting planet
            current_degree: Current position in degrees

        Returns:
            List of aspect information
        """
        aspects = []
        aspect_orbs = {
            'Conjunction': 6,    # 0° ± 6°
            'Sextile': 4,        # 60° ± 4°
            'Square': 6,         # 90° ± 6°
            'Trine': 6,          # 120° ± 6°
            'Opposition': 6      # 180° ± 6°
        }

        for birth_planet, birth_data in self.birth_planets.items():
            if isinstance(birth_data, dict):
                birth_degree = birth_data.get('longitude', 0)
            else:
                continue

            # Calculate angle between planets
            angle = self._calculate_angle(current_degree, birth_degree)

            # Check for aspects
            for aspect_name, orb in aspect_orbs.items():
                aspect_angle = self._get_aspect_angle(aspect_name)

                if abs(angle - aspect_angle) <= orb:
                    aspects.append({
                        'planet': birth_planet,
                        'aspect': aspect_name,
                        'angle': round(angle, 2),
                        'orb': round(abs(angle - aspect_angle), 2),
                        'applying': angle < aspect_angle,
                        'strength': 'Strong' if abs(angle - aspect_angle) < 2 else 'Moderate'
                    })

        return aspects

    def _calculate_angle(self, degree1: float, degree2: float) -> float:
        """
        Calculate angle between two degree positions.

        Args:
            degree1: First position (0-360)
            degree2: Second position (0-360)

        Returns:
            Angle in degrees (0-180)
        """
        diff = abs(degree1 - degree2)
        if diff > 180:
            diff = 360 - diff
        return diff

    def _get_aspect_angle(self, aspect_name: str) -> float:
        """Get the exact angle for an aspect."""
        aspect_angles = {
            'Conjunction': 0,
            'Sextile': 60,
            'Square': 90,
            'Trine': 120,
            'Opposition': 180
        }
        return aspect_angles.get(aspect_name, 0)

    def _determine_transit_quality(self, planet: str, current_sign: str,
                                   birth_sign: Optional[str]) -> str:
        """
        Determine if transit is benefic or malefic.

        Args:
            planet: Planet name
            current_sign: Current zodiac sign
            birth_sign: Birth zodiac sign

        Returns:
            'Benefic', 'Neutral', or 'Malefic'
        """
        # Simple logic: some planets are naturally benefic/malefic
        benefic_planets = ['Sun', 'Moon', 'Jupiter', 'Venus', 'Mercury']
        malefic_planets = ['Mars', 'Saturn', 'Rahu', 'Ketu']
        neutral_planets = []

        if planet in benefic_planets:
            return 'Benefic'
        elif planet in malefic_planets:
            return 'Malefic'
        else:
            return 'Neutral'

    def _get_transit_interpretation(self, planet: str, current_sign: str,
                                    birth_sign: Optional[str]) -> str:
        """
        Get interpretation for transit.

        Args:
            planet: Planet name
            current_sign: Current sign
            birth_sign: Birth sign

        Returns:
            Transit interpretation string
        """
        interpretations = {
            'Sun': f"{planet} transiting {current_sign} brings focus and vitality to areas ruled by {current_sign}",
            'Moon': f"{planet} in {current_sign} creates emotional tendencies and daily influences",
            'Mercury': f"{planet} in {current_sign} affects communication and intellectual matters",
            'Venus': f"{planet} in {current_sign} brings harmony or challenges in relationships and finance",
            'Mars': f"{planet} in {current_sign} energizes or creates conflicts in {current_sign} matters",
            'Jupiter': f"{planet} in {current_sign} expands opportunities and brings good fortune",
            'Saturn': f"{planet} in {current_sign} brings lessons, restrictions, and long-term growth",
            'Rahu': f"{planet} in {current_sign} indicates obsessions and new ventures",
            'Ketu': f"{planet} in {current_sign} brings spiritual lessons and release"
        }

        base_interpretation = interpretations.get(planet, f"{planet} transiting {current_sign}")

        if birth_sign and current_sign == birth_sign:
            base_interpretation += " (Same as birth sign - reinforcing birth chart influence)"
        elif birth_sign:
            houses_apart = self._calculate_houses_apart(current_sign, birth_sign)
            if houses_apart == 7:
                base_interpretation += " (Opposing birth position - significant impact)"
            elif houses_apart == 4 or houses_apart == 8:
                base_interpretation += " (Square to birth position - challenging aspect)"
            elif houses_apart == 5 or houses_apart == 9:
                base_interpretation += " (Trine to birth position - harmonious influence)"

        return base_interpretation

    def _calculate_houses_apart(self, sign1: str, sign2: str) -> int:
        """Calculate houses apart between two signs."""
        signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]

        try:
            idx1 = signs.index(sign1)
            idx2 = signs.index(sign2)
            diff = abs(idx1 - idx2)
            return min(diff, 12 - diff)
        except ValueError:
            return 0

    def get_important_transits(self) -> List[Dict]:
        """
        Get list of currently important transits.

        Important transits are:
        - Saturn transits (major life periods)
        - Jupiter transits (annual good fortune)
        - Lunar Node transits (1.5-year periods)

        Returns:
            List of important transit information
        """
        try:
            current_transits = self.calculate_current_transits()
            important = []

            # Saturn transits are most important
            if 'Saturn' in current_transits:
                saturn = current_transits['Saturn']
                important.append({
                    'planet': 'Saturn',
                    'type': 'Critical Life Period',
                    'duration': '2.5 years per sign',
                    'current': saturn['current_sign'],
                    'significance': 'Tests, lessons, and long-term development',
                    'impact': 'High'
                })

            # Jupiter transits bring yearly opportunities
            if 'Jupiter' in current_transits:
                jupiter = current_transits['Jupiter']
                important.append({
                    'planet': 'Jupiter',
                    'type': 'Expansion Period',
                    'duration': '~13 months per sign',
                    'current': jupiter['current_sign'],
                    'significance': 'Growth, opportunities, and good fortune',
                    'impact': 'High'
                })

            # Lunar Nodes bring major life transitions
            for node in ['Rahu', 'Ketu']:
                if node in current_transits:
                    node_info = current_transits[node]
                    important.append({
                        'planet': node,
                        'type': 'Life Transition Period',
                        'duration': '~1.5 years per sign',
                        'current': node_info['current_sign'],
                        'significance': f"{node} brings fated events and major life changes",
                        'impact': 'Very High'
                    })

            return important

        except Exception as e:
            logger.error(f"Error getting important transits: {str(e)}")
            return []

    def get_upcoming_important_transits(self, days: int = 365) -> List[Dict]:
        """
        Predict upcoming important transits for specified period.

        Args:
            days: Number of days to look ahead (default: 365 for 1 year)

        Returns:
            List of upcoming important transits
        """
        try:
            upcoming = []

            # Check for sign changes in the next specified days
            for i in range(0, days, 30):
                future_date = self.transit_date + timedelta(days=i)
                future_calc = TransitCalculator(self.birth_chart, future_date)
                future_transits = future_calc.calculate_current_transits()

                current_transits = self.calculate_current_transits()

                for planet in ['Saturn', 'Jupiter', 'Rahu', 'Ketu']:
                    if planet in future_transits and planet in current_transits:
                        if (future_transits[planet]['current_sign'] !=
                            current_transits[planet]['current_sign']):
                            upcoming.append({
                                'planet': planet,
                                'date': future_date.strftime('%Y-%m-%d'),
                                'new_sign': future_transits[planet]['current_sign'],
                                'old_sign': current_transits[planet]['current_sign'],
                                'significance': self.TRANSIT_SIGNIFICANCE.get(planet),
                                'days_away': i
                            })

            return sorted(upcoming, key=lambda x: x['days_away'])

        except Exception as e:
            logger.error(f"Error calculating upcoming transits: {str(e)}")
            return []

    def get_transit_predictions(self) -> List[str]:
        """
        Generate predictions based on current transits.

        Returns:
            List of prediction strings
        """
        try:
            predictions = []
            transits = self.calculate_current_transits()

            predictions.append("TRANSIT-BASED PREDICTIONS")
            predictions.append("=" * 50)

            # Saturn predictions
            if 'Saturn' in transits:
                saturn = transits['Saturn']
                if saturn['transit_quality'] == 'Malefic':
                    predictions.append(
                        f"Saturn in {saturn['current_sign']}: "
                        f"This is a testing period. Focus on discipline, hard work, "
                        f"and accepting life's lessons. Results come through perseverance."
                    )
                else:
                    predictions.append(
                        f"Saturn in {saturn['current_sign']}: "
                        f"Long-term success possible through sustained effort. "
                        f"Build strong foundations for future growth."
                    )

            # Jupiter predictions
            if 'Jupiter' in transits:
                jupiter = transits['Jupiter']
                predictions.append(
                    f"Jupiter in {jupiter['current_sign']}: "
                    f"Good fortune and expansion available in {jupiter['current_sign']} areas. "
                    f"Take calculated risks and pursue growth opportunities."
                )

            # Moon predictions
            if 'Moon' in transits:
                moon = transits['Moon']
                predictions.append(
                    f"Moon in {moon['current_sign']}: "
                    f"Your emotional state is currently influenced by {moon['current_sign']} qualities. "
                    f"Good time for emotional matters and family concerns."
                )

            return predictions

        except Exception as e:
            logger.error(f"Error generating transit predictions: {str(e)}")
            return ["Unable to generate transit predictions"]

    def analyze_transit_dasha_conjunction(self, current_dasha: str) -> List[str]:
        """
        Analyze interaction between current transits and dasha periods.

        Args:
            current_dasha: Current dasha planet

        Returns:
            List of conjunction analysis
        """
        try:
            analysis = []
            transits = self.calculate_current_transits()

            if current_dasha in transits:
                dasha_transit = transits[current_dasha]
                analysis.append(
                    f"Current {current_dasha} Dasha is interacting with {current_dasha} Transit"
                )
                analysis.append(
                    f"Transit {current_dasha} in {dasha_transit['current_sign']} "
                    f"strengthens {current_dasha} dasha effects"
                )
                analysis.append(
                    "Combined influence: Results will manifest more strongly and quickly"
                )

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing dasha-transit conjunction: {str(e)}")
            return []
