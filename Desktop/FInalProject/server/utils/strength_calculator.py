"""
Planetary Strength Calculator (Shad Bala)
Implements the six measures of planetary strength in Vedic astrology.

Shad Bala = Six Strength Measures:
1. Sthana Bala (Positional Strength) - House & Sign position
2. Dig Bala (Directional Strength) - Directional position
3. Kala Bala (Temporal Strength) - Time-based factors
4. Chesta Bala (Motion Strength) - Planet's speed & motion
5. Naisargika Bala (Natural Strength) - Inherent planet strength
6. Drishti Bala (Aspect Strength) - Aspects received

Total Strength = 0-60 points per planet

Author: Astrology Backend
"""

from datetime import datetime
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class StrengthCalculator:
    """
    Calculate comprehensive planetary strengths using Shad Bala system.

    Each planet can score 0-60 points across 6 strength measures.
    """

    # Exalted positions (degrees where planets are strongest)
    EXALTATION_DEGREES = {
        'Sun': 10,      # Aries
        'Moon': 3,      # Taurus
        'Mercury': 15,  # Virgo
        'Venus': 27,    # Pisces
        'Mars': 28,     # Capricorn
        'Jupiter': 5,   # Cancer
        'Saturn': 20,   # Libra
        'Rahu': 20,     # Gemini
        'Ketu': 20      # Sagittarius
    }

    # Own signs for each planet
    OWN_SIGNS = {
        'Sun': [5],                    # Leo
        'Moon': [4],                   # Cancer
        'Mercury': [3, 6],             # Gemini, Virgo
        'Venus': [2, 7],               # Taurus, Libra
        'Mars': [1, 8],                # Aries, Scorpio
        'Jupiter': [9, 12],            # Sagittarius, Pisces
        'Saturn': [10, 11],            # Capricorn, Aquarius
        'Rahu': [11],                  # Aquarius
        'Ketu': [8]                    # Scorpio
    }

    # Debilitated signs
    DEBILITATED_SIGNS = {
        'Sun': 7,       # Libra
        'Moon': 8,      # Scorpio
        'Mercury': 12,  # Pisces
        'Venus': 6,     # Virgo
        'Mars': 4,      # Cancer
        'Jupiter': 10,  # Capricorn
        'Saturn': 1,    # Aries
        'Rahu': 9,      # Sagittarius
        'Ketu': 3       # Gemini
    }

    # Directional strength - which quadrant each planet is strongest
    DIRECTIONAL_STRENGTH = {
        'Sun': {'quadrant': 1, 'description': 'East'},      # 0-90° (1st quadrant)
        'Moon': {'quadrant': 4, 'description': 'North'},    # 270-360° (4th quadrant)
        'Mars': {'quadrant': 2, 'description': 'South'},    # 90-180° (2nd quadrant)
        'Mercury': {'quadrant': 1, 'description': 'East'},
        'Jupiter': {'quadrant': 1, 'description': 'East'},
        'Venus': {'quadrant': 2, 'description': 'South'},
        'Saturn': {'quadrant': 3, 'description': 'West'},   # 180-270° (3rd quadrant)
        'Rahu': {'quadrant': 3, 'description': 'West'},
        'Ketu': {'quadrant': 3, 'description': 'West'}
    }

    # Natural strength ranking (Naisargika Bala)
    NATURAL_STRENGTH_RANKING = {
        'Sun': 60,
        'Moon': 51,
        'Venus': 42,
        'Jupiter': 34,
        'Mercury': 25,
        'Mars': 17,
        'Saturn': 10,
        'Rahu': 15,
        'Ketu': 12
    }

    def __init__(self, planets_info: Dict, ascendant_sign: int, birth_date: datetime):
        """
        Initialize Strength Calculator.

        Args:
            planets_info: Dictionary with planet positions and details
            ascendant_sign: Ascendant sign number (1-12)
            birth_date: Birth date for time-based calculations
        """
        self.planets_info = planets_info
        self.ascendant_sign = ascendant_sign
        self.birth_date = birth_date

    def calculate_all_strengths(self) -> Dict:
        """
        Calculate complete strength analysis for all planets.

        Returns:
            Dictionary with strength details for each planet
        """
        strengths = {}

        try:
            for planet in self.planets_info.keys():
                strength_data = self.calculate_planet_strength(planet)
                strengths[planet] = strength_data

            # Add overall chart strength assessment
            overall_strength = self._calculate_overall_chart_strength(strengths)

            return {
                'planetary_strengths': strengths,
                'chart_strength_assessment': overall_strength
            }

        except Exception as e:
            logger.error(f"Error calculating all strengths: {str(e)}", exc_info=True)
            return {'error': str(e)}

    def calculate_planet_strength(self, planet: str) -> Dict:
        """
        Calculate complete strength profile for a single planet.

        Args:
            planet: Planet name

        Returns:
            Dictionary with all strength components
        """
        try:
            sthana = self._calculate_sthana_bala(planet)
            dig = self._calculate_dig_bala(planet)
            kala = self._calculate_kala_bala(planet)
            chesta = self._calculate_chesta_bala(planet)
            naisargika = self._calculate_naisargika_bala(planet)
            drishti = self._calculate_drishti_bala(planet)

            total_strength = sthana + dig + kala + chesta + naisargika + drishti
            strength_percentage = (total_strength / 60) * 100

            return {
                'planet': planet,
                'total_strength': round(total_strength, 2),
                'strength_percentage': round(strength_percentage, 1),
                'strength_status': self._get_strength_status(strength_percentage),
                'breakdown': {
                    'sthana_bala': round(sthana, 2),      # Positional
                    'dig_bala': round(dig, 2),            # Directional
                    'kala_bala': round(kala, 2),          # Temporal
                    'chesta_bala': round(chesta, 2),      # Motion
                    'naisargika_bala': round(naisargika, 2),  # Natural
                    'drishti_bala': round(drishti, 2)     # Aspect
                },
                'is_strong': strength_percentage >= 70,
                'capacity': self._assess_capacity(strength_percentage)
            }

        except Exception as e:
            logger.error(f"Error calculating strength for {planet}: {str(e)}")
            return {'error': str(e)}

    def _calculate_sthana_bala(self, planet: str) -> float:
        """
        Calculate Sthana Bala (Positional Strength).

        Based on:
        - Exalted position (strongest)
        - Own sign
        - Friendly sign
        - Neutral sign
        - Enemy sign
        - Debilitated (weakest)

        Returns:
            Strength points (0-15)
        """
        if planet not in self.planets_info:
            return 0

        planet_sign = self.planets_info[planet].get('sign')
        planet_degree = self.planets_info[planet].get('longitude', 0)

        # Base score (0-15)
        if planet_sign in [5] and planet == 'Sun':  # Sun in Leo (own)
            return 15
        elif planet_sign == self.OWN_SIGNS.get(planet, [])[0] if self.OWN_SIGNS.get(planet) else None:
            return 12
        elif planet_sign == self.DEBILITATED_SIGNS.get(planet):
            return 3
        else:
            return 9

    def _calculate_dig_bala(self, planet: str) -> float:
        """
        Calculate Dig Bala (Directional Strength).

        Each planet has a direction where it's strongest.
        Strength based on planet's house position relative to direction.

        Returns:
            Strength points (0-15)
        """
        if planet not in self.planets_info:
            return 0

        house = self.planets_info[planet].get('house', 1)
        directional_config = self.DIRECTIONAL_STRENGTH.get(planet, {})

        # Simplified: Strong in designated quadrant
        if directional_config.get('quadrant') == 1 and house in [1, 10]:
            return 15
        elif directional_config.get('quadrant') == 2 and house in [4, 5]:
            return 15
        elif directional_config.get('quadrant') == 3 and house in [7, 8]:
            return 15
        elif directional_config.get('quadrant') == 4 and house in [10, 11]:
            return 15
        else:
            return 8

    def _calculate_kala_bala(self, planet: str) -> float:
        """
        Calculate Kala Bala (Temporal Strength).

        Based on:
        - Day/Night (some planets strong during day, some at night)
        - Month (seasonal strength)
        - Year
        - Hour (planetary hours)

        Returns:
            Strength points (0-15)
        """
        try:
            # Simplified temporal strength
            # Sun, Mars, Jupiter strong during day
            day_planets = ['Sun', 'Mars', 'Jupiter']
            night_planets = ['Moon', 'Venus', 'Saturn']

            # Get hour of birth (simplified - assuming daytime for now)
            hour = self.birth_date.hour

            is_daytime = 6 <= hour <= 18

            if planet in day_planets and is_daytime:
                return 12
            elif planet in night_planets and not is_daytime:
                return 12
            else:
                return 8

        except Exception as e:
            logger.warning(f"Error in Kala Bala calculation: {str(e)}")
            return 8

    def _calculate_chesta_bala(self, planet: str) -> float:
        """
        Calculate Chesta Bala (Motion Strength).

        Based on:
        - Planet speed (faster = stronger)
        - Retrograde status (retrograde = weaker)
        - Direction of motion

        Returns:
            Strength points (0-15)
        """
        if planet not in self.planets_info:
            return 0

        speed = self.planets_info[planet].get('speed', 0)
        retrograde = self.planets_info[planet].get('retrograde', False)

        # Base calculation
        base_strength = 10 if not retrograde else 4

        # Adjust based on speed (higher speed = stronger motion)
        if speed > 1:
            base_strength += 3
        elif speed < 0.1:
            base_strength -= 2

        # Cap at 15
        return min(base_strength, 15)

    def _calculate_naisargika_bala(self, planet: str) -> float:
        """
        Calculate Naisargika Bala (Natural Strength).

        Inherent strength of planet (does not change).
        Sun is strongest, Saturn is weakest.

        Returns:
            Strength points (0-15) normalized from natural ranking
        """
        if planet not in self.planets_info:
            return 0

        natural_rank = self.NATURAL_STRENGTH_RANKING.get(planet, 10)
        # Normalize to 0-15 scale
        # Sun=60 maps to 15, Saturn=10 maps to 2.5
        normalized = (natural_rank / 60) * 15

        return round(normalized, 2)

    def _calculate_drishti_bala(self, planet: str) -> float:
        """
        Calculate Drishti Bala (Aspect Strength).

        Benefic aspects increase strength.
        Malefic aspects decrease strength.
        Mutual aspects with other planets.

        Returns:
            Strength points (0-15)
        """
        if planet not in self.planets_info:
            return 0

        base_strength = 8
        benefic_planets = ['Sun', 'Moon', 'Jupiter', 'Venus', 'Mercury']
        malefic_planets = ['Mars', 'Saturn', 'Rahu', 'Ketu']

        # Check for beneficial aspects
        for other_planet in self.planets_info.keys():
            if other_planet != planet:
                other_house = self.planets_info[other_planet].get('house', 1)
                planet_house = self.planets_info[planet].get('house', 1)

                # Check if in aspect (7th house aspect simplified)
                if abs(other_house - planet_house) == 6:
                    if other_planet in benefic_planets:
                        base_strength += 2
                    elif other_planet in malefic_planets:
                        base_strength -= 2

        return min(max(base_strength, 0), 15)

    def _get_strength_status(self, percentage: float) -> str:
        """Get descriptive strength status."""
        if percentage >= 80:
            return 'Very Strong'
        elif percentage >= 60:
            return 'Strong'
        elif percentage >= 40:
            return 'Moderate'
        elif percentage >= 20:
            return 'Weak'
        else:
            return 'Very Weak'

    def _assess_capacity(self, percentage: float) -> str:
        """Assess planet's capacity to give results."""
        if percentage >= 80:
            return 'Full capacity - Planet can give complete results'
        elif percentage >= 60:
            return 'Good capacity - Planet can give favorable results'
        elif percentage >= 40:
            return 'Moderate capacity - Planet gives mixed results'
        elif percentage >= 20:
            return 'Limited capacity - Planet gives minimal results'
        else:
            return 'Very limited capacity - Planet struggles to give results'

    def _calculate_overall_chart_strength(self, strengths: Dict) -> Dict:
        """
        Calculate overall chart strength assessment.

        Args:
            strengths: Dictionary of all planetary strengths

        Returns:
            Overall chart strength analysis
        """
        try:
            if not strengths or 'planetary_strengths' not in strengths:
                return {}

            planetary_strengths = strengths['planetary_strengths']

            strong_planets = [p for p, data in planetary_strengths.items()
                            if isinstance(data, dict) and data.get('is_strong')]

            total_strength = sum(data.get('total_strength', 0)
                               for data in planetary_strengths.values()
                               if isinstance(data, dict))

            average_strength = total_strength / len(planetary_strengths) if planetary_strengths else 0

            return {
                'total_planetary_strength': round(total_strength, 2),
                'average_planet_strength': round(average_strength, 2),
                'strong_planets_count': len(strong_planets),
                'strong_planets': strong_planets,
                'chart_quality': self._assess_chart_quality(len(strong_planets), average_strength),
                'recommendations': self._get_strength_recommendations(planetary_strengths)
            }

        except Exception as e:
            logger.error(f"Error calculating overall strength: {str(e)}")
            return {}

    def _assess_chart_quality(self, strong_count: int, avg_strength: float) -> str:
        """Assess overall chart quality based on strengths."""
        if strong_count >= 5 and avg_strength >= 35:
            return 'Excellent - Strong planetary support'
        elif strong_count >= 3 and avg_strength >= 30:
            return 'Good - Decent planetary support'
        elif strong_count >= 2 and avg_strength >= 25:
            return 'Average - Moderate planetary support'
        else:
            return 'Challenging - Limited planetary support'

    def _get_strength_recommendations(self, planetary_strengths: Dict) -> List[str]:
        """Get recommendations based on planetary strengths."""
        recommendations = []

        try:
            weak_planets = []
            for planet, data in planetary_strengths.items():
                if isinstance(data, dict) and not data.get('is_strong'):
                    weak_planets.append(planet)

            if weak_planets:
                recommendations.append(
                    f"Weak planets: {', '.join(weak_planets)}. "
                    f"Consider remedies (mantras, donations, gems) for these planets."
                )

            strong_planets = [p for p, data in planetary_strengths.items()
                            if isinstance(data, dict) and data.get('is_strong')]

            if strong_planets:
                recommendations.append(
                    f"Strong planets: {', '.join(strong_planets)}. "
                    f"These planets can give excellent results in their periods."
                )

            recommendations.append(
                "Focus on strengthening weak planets through appropriate practices."
            )

        except Exception as e:
            logger.warning(f"Error generating recommendations: {str(e)}")

        return recommendations

    def get_strength_interpretation(self, planet: str) -> Dict:
        """
        Get detailed interpretation of planet's strength.

        Args:
            planet: Planet name

        Returns:
            Dictionary with interpretation details
        """
        strength_data = self.calculate_planet_strength(planet)

        if 'error' in strength_data:
            return strength_data

        capacity = strength_data['capacity']
        status = strength_data['strength_status']

        return {
            'planet': planet,
            'strength_status': status,
            'capacity': capacity,
            'breakdown': strength_data['breakdown'],
            'interpretation': f"{planet} is {status}. {capacity}",
            'best_for': self._get_planet_use_cases(planet, strength_data['is_strong']),
            'challenges': self._get_planet_challenges(planet, not strength_data['is_strong'])
        }

    def _get_planet_use_cases(self, planet: str, is_strong: bool) -> List[str]:
        """Get what planet is best for."""
        use_cases = {
            'Sun': ['Leadership', 'Government jobs', 'Authority'],
            'Moon': ['Mind peace', 'Public relations', 'Emotional stability'],
            'Mars': ['Sports', 'Military', 'Engineering'],
            'Mercury': ['Business', 'Writing', 'Communication'],
            'Jupiter': ['Teaching', 'Spirituality', 'Wisdom'],
            'Venus': ['Arts', 'Entertainment', 'Relationships'],
            'Saturn': ['Hard work', 'Discipline', 'Long-term projects'],
            'Rahu': ['Modern ventures', 'Technology', 'Unconventional fields'],
            'Ketu': ['Spirituality', 'Occult', 'Meditation']
        }

        base_uses = use_cases.get(planet, [])
        if is_strong:
            return [f"✓ {use}" for use in base_uses]
        else:
            return [f"△ {use}" for use in base_uses]

    def _get_planet_challenges(self, planet: str, is_weak: bool) -> List[str]:
        """Get challenges for planet."""
        challenges = {
            'Sun': ['Ego issues', 'Health problems', 'Authority conflicts'],
            'Moon': ['Emotional instability', 'Depression', 'Confusion'],
            'Mars': ['Accidents', 'Aggression', 'Conflicts'],
            'Mercury': ['Nervousness', 'Communication failures', 'Confusion'],
            'Jupiter': ['Over-expansion', 'Legal issues', 'Excess'],
            'Venus': ['Relationship issues', 'Excess indulgence'],
            'Saturn': ['Delays', 'Obstacles', 'Hardships'],
            'Rahu': ['Illusions', 'Addictions', 'Obsessions'],
            'Ketu': ['Health issues', 'Isolation', 'Confusion']
        }

        if is_weak:
            return challenges.get(planet, [])
        return []
