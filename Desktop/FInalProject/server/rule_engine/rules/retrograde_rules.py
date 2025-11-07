"""
Retrograde Planet Analysis Rules
Provides interpretations for retrograde planets in the birth chart.

In Vedic astrology, retrograde planets have different effects than in Western astrology.

Author: Astrology Backend
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class RetrogradRules:
    """Generate interpretations for retrograde planets."""

    # Retrograde effects by planet
    RETROGRADE_EFFECTS = {
        'Sun': 'Rare and inauspicious; affects authority and self-expression',
        'Moon': 'Very rare; affects emotional stability',
        'Mars': 'Affects courage and action; can create internal conflict',
        'Mercury': 'Affects communication and intellect; creates delays',
        'Jupiter': 'Affects expansion and wisdom; inward spiritual growth',
        'Venus': 'Affects relationships and values; relationship lessons',
        'Saturn': 'Affects discipline; can create introspection and maturity',
        'Rahu': 'Uncommon; affects obsessions and ambitions',
        'Ketu': 'Uncommon; affects spirituality and detachment'
    }

    @staticmethod
    def interpret_retrograde_planet(planet: str, retrograde_status: bool,
                                    planet_data: Dict) -> List[str]:
        """
        Generate interpretation for a retrograde planet.

        Args:
            planet: Planet name
            retrograde_status: Whether planet is retrograde
            planet_data: Complete planet data

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            if not retrograde_status:
                return [f"{planet}: Direct motion - normal expression"]

            interpretations.append(f"✓ {planet} RETROGRADE")
            interpretations.append("=" * 50)

            # General effect
            if planet in RetrogradRules.RETROGRADE_EFFECTS:
                interpretations.append(
                    f"General Effect: {RetrogradRules.RETROGRADE_EFFECTS[planet]}"
                )

            # Specific interpretations
            specific = RetrogradRules._get_specific_retrograde_interpretation(planet)
            interpretations.extend(specific)

            # House analysis
            house = planet_data.get('house', 0)
            if house:
                interpretations.append(
                    f"\nIn House {house}: Effects are modified by house placement"
                )

            # Sign analysis
            sign = planet_data.get('sign', '')
            if sign:
                interpretations.extend(
                    RetrogradRules._get_retrograde_sign_analysis(planet, sign)
                )

        except Exception as e:
            logger.error(f"Error interpreting retrograde {planet}: {str(e)}")

        return interpretations

    @staticmethod
    def _get_specific_retrograde_interpretation(planet: str) -> List[str]:
        """Get specific interpretation for retrograde planet."""

        interpretations = {
            'Sun': [
                "Affects self-expression and personal power",
                "May struggle with authority and leadership",
                "Need for introspection and self-discovery",
                "Karmic lessons regarding pride and ego"
            ],
            'Moon': [
                "Affects emotional expression and intuition",
                "Tendency towards emotional introversion",
                "Past-life emotional patterns need resolution",
                "Deep introspection and psychological work beneficial"
            ],
            'Mercury': [
                "Communication may be internal rather than external",
                "Tendency to overthink and analyze",
                "May experience delays in communication",
                "Good for writing, research, and deep thinking",
                "Misunderstandings possible in relationships"
            ],
            'Venus': [
                "Relationship patterns from past lives present",
                "May withdraw from social life",
                "Need for self-love and inner values",
                "Love comes through introspection and wisdom",
                "Karmic relationship lessons to learn"
            ],
            'Mars': [
                "Aggression is internalized rather than expressed",
                "May feel lack of courage or assertiveness",
                "Indirect approach to conflicts",
                "Need to develop internal strength",
                "Transform anger into spiritual power"
            ],
            'Jupiter': [
                "Luck is internal spiritual growth, not external expansion",
                "Wisdom comes through suffering and lessons",
                "Spiritual guru or teacher within",
                "Expansion comes through introspection",
                "Great opportunity for spiritual development"
            ],
            'Saturn': [
                "Delays and obstacles serve as lessons",
                "Develop patience, discipline, and perseverance",
                "Maturity comes through facing challenges",
                "Past-life karmic debts working out",
                "Introspection leads to lasting results"
            ],
            'Rahu': [
                "Unusual or unconventional path in life",
                "Obsessions need to be internalized",
                "Growth through non-traditional means",
                "Psychic or intuitive abilities may develop"
            ],
            'Ketu': [
                "Spiritual wisdom from past lives",
                "Detachment from worldly matters",
                "Mystical or occult interests",
                "Natural spiritual abilities present"
            ]
        }

        return interpretations.get(planet, ["Retrograde effects present"])

    @staticmethod
    def _get_retrograde_sign_analysis(planet: str, sign: str) -> List[str]:
        """Get retrograde analysis based on sign placement."""
        analysis = []

        try:
            analysis.append(f"\nRetrograde {planet} in {sign}:")

            # Element analysis
            fire_signs = ['Aries', 'Leo', 'Sagittarius']
            earth_signs = ['Taurus', 'Virgo', 'Capricorn']
            air_signs = ['Gemini', 'Libra', 'Aquarius']
            water_signs = ['Cancer', 'Scorpio', 'Pisces']

            if sign in fire_signs:
                analysis.append(f"In fire sign {sign}: Introspect on your passion and courage")
            elif sign in earth_signs:
                analysis.append(f"In earth sign {sign}: Focus on practical, grounded approach")
            elif sign in air_signs:
                analysis.append(f"In air sign {sign}: Mental analysis and communication reflection")
            elif sign in water_signs:
                analysis.append(f"In water sign {sign}: Emotional depth and intuitive understanding")

        except Exception as e:
            logger.error(f"Error analyzing retrograde sign: {str(e)}")

        return analysis

    @staticmethod
    def get_retrograde_summary(birth_chart: Dict) -> Dict:
        """
        Get summary of all retrograde planets.

        Args:
            birth_chart: Birth chart data

        Returns:
            Summary dictionary
        """
        try:
            planets_info = birth_chart.get('planets', {})
            retrograde_planets = []

            for planet, data in planets_info.items():
                if isinstance(data, dict):
                    # Assuming retrograde status is in the data
                    # This would need to be populated from ephemeris calculation
                    retrograde_status = data.get('retrograde', False)

                    if retrograde_status:
                        retrograde_planets.append({
                            'planet': planet,
                            'sign': data.get('sign', ''),
                            'house': data.get('house', 0)
                        })

            return {
                'total_retrograde': len(retrograde_planets),
                'retrograde_planets': retrograde_planets,
                'has_retrograde': len(retrograde_planets) > 0,
                'interpretation': RetrogradRules._get_retrograde_chart_interpretation(
                    len(retrograde_planets)
                )
            }

        except Exception as e:
            logger.error(f"Error getting retrograde summary: {str(e)}")
            return {'total_retrograde': 0, 'retrograde_planets': []}

    @staticmethod
    def _get_retrograde_chart_interpretation(retrograde_count: int) -> str:
        """Get interpretation for number of retrograde planets."""
        if retrograde_count == 0:
            return "No retrograde planets - Direct manifestation of planets"
        elif retrograde_count == 1:
            return "One retrograde planet - Specific area needs introspection"
        elif retrograde_count <= 3:
            return "Multiple retrograde planets - Deep introspection and spiritual growth needed"
        else:
            return "Many retrograde planets - Significant karmic lessons, spiritual evolution focus"

    @staticmethod
    def get_retrograde_remedies(planet: str) -> List[str]:
        """
        Get remedies for retrograde planets.

        Args:
            planet: Retrograde planet name

        Returns:
            List of remedy suggestions
        """
        remedies = {
            'Sun': [
                "Practice humility and service to others",
                "Regular meditation on self",
                "Spend time in sunlight",
                "Develop your core identity and self-worth"
            ],
            'Moon': [
                "Emotional healing work and counseling",
                "Journal your feelings regularly",
                "Meditation to calm the mind",
                "Moon fasting on Mondays beneficial"
            ],
            'Mercury': [
                "Double-check all communications",
                "Study and learning important",
                "Journal your thoughts",
                "Practice clear thinking and logic"
            ],
            'Venus': [
                "Develop self-love and inner values",
                "Artistic pursuits and creativity",
                "Nurture important relationships",
                "Financial management and budgeting"
            ],
            'Mars': [
                "Channel energy into productive work",
                "Martial arts or physical activity",
                "Develop courage and assertiveness",
                "Handle conflicts diplomatically"
            ],
            'Jupiter': [
                "Spiritual studies and philosophy",
                "Teaching and sharing wisdom",
                "Charitable work and service",
                "Guru meditation and mentoring"
            ],
            'Saturn': [
                "Accept limitations and work within them",
                "Long-term planning and discipline",
                "Serve the elderly or disadvantaged",
                "Patience and perseverance practice"
            ],
            'Rahu': [
                "Ground yourself through yoga",
                "Avoid addictions and obsessions",
                "Spiritual practices and meditation",
                "Channel ambitions into constructive goals"
            ],
            'Ketu': [
                "Meditation and spiritual practices",
                "Study occult and metaphysics",
                "Accept losses gracefully",
                "Develop detachment from material"
            ]
        }

        return remedies.get(planet, [
            "Practice meditation and yoga",
            "Engage in spiritual studies",
            "Perform charitable deeds",
            "Introspection and self-reflection"
        ])

    @staticmethod
    def analyze_retrograde_dasha_conjunction(planet: str, in_retrograde: bool,
                                              current_dasha: str) -> List[str]:
        """
        Analyze retrograde planet in current dasha.

        Args:
            planet: Planet name
            in_retrograde: Is it retrograde
            current_dasha: Current dasha planet

        Returns:
            Analysis strings
        """
        analysis = []

        try:
            if not in_retrograde:
                return [f"{planet}: Direct motion during {current_dasha} dasha - normal results"]

            analysis.append(
                f"RETROGRADE {planet.upper()} IN {current_dasha.upper()} DASHA"
            )
            analysis.append("=" * 50)

            if planet == current_dasha:
                analysis.append(
                    f"The dasha lord {planet} is retrograde - Unique influence"
                )
                analysis.append(
                    "Results are delayed but work intensely when they come"
                )
                analysis.append(
                    "Introspection and inner work will be beneficial"
                )
            else:
                analysis.append(
                    f"{planet} retrograde during {current_dasha} dasha"
                )
                analysis.append(
                    "Conflicting influences - need to balance action with reflection"
                )

        except Exception as e:
            logger.error(f"Error analyzing retrograde dasha: {str(e)}")

        return analysis
