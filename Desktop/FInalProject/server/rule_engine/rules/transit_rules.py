"""
Transit Interpretation Rules
Provides meaningful interpretations for current planetary transits.

Transits show current planetary influences and timing of life events.

Author: Astrology Backend
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class TransitRules:
    """Generate interpretations for planetary transits."""

    @staticmethod
    def interpret_sun_transit(transit_data: Dict) -> List[str]:
        """
        Interpret Sun transit effects.

        Sun transit through a sign affects general vitality and focus.

        Args:
            transit_data: Sun transit information

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            current_sign = transit_data.get('current_sign', '')
            birth_sign = transit_data.get('birth_sign', '')

            interpretations.append("SUN TRANSIT")
            interpretations.append("=" * 50)
            interpretations.append(f"Sun is currently in {current_sign}")
            interpretations.append("Sun's 30-day transit brings focus to matters ruled by this sign")

            if current_sign == birth_sign:
                interpretations.append(
                    "✓ Sun on birth position: Your natural vitality is heightened"
                )
                interpretations.append(
                    "This is a time of increased confidence, energy, and personal power"
                )
            else:
                interpretations.append(
                    f"Focus is on {current_sign} affairs during this transit period"
                )

            interpretations.append(
                "Sun transit activates the house it passes through in your birth chart"
            )

        except Exception as e:
            logger.error(f"Error interpreting Sun transit: {str(e)}")

        return interpretations

    @staticmethod
    def interpret_moon_transit(transit_data: Dict) -> List[str]:
        """
        Interpret Moon transit effects.

        Moon transit affects emotions, daily mood, and immediate events.

        Args:
            transit_data: Moon transit information

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            current_sign = transit_data.get('current_sign', '')
            birth_sign = transit_data.get('birth_sign', '')

            interpretations.append("MOON TRANSIT - Daily Emotional Influence")
            interpretations.append("=" * 50)
            interpretations.append(f"Moon is currently in {current_sign}")
            interpretations.append("Moon's 2-day transit through each sign affects emotions and daily mood")

            if current_sign == birth_sign:
                interpretations.append(
                    "✓ Moon on birth position (Chandra Grahan): Very important day"
                )
                interpretations.append(
                    "Strong emotional and intuitive powers activated today"
                )
                interpretations.append(
                    "Good time for decisions related to emotions, home, and family"
                )
            else:
                interpretations.append(
                    f"Your emotional nature is tuned to {current_sign} qualities"
                )

            interpretations.append(
                "Moon transit affects: emotions, mood, intuition, domestic matters"
            )

        except Exception as e:
            logger.error(f"Error interpreting Moon transit: {str(e)}")

        return interpretations

    @staticmethod
    def interpret_mars_transit(transit_data: Dict) -> List[str]:
        """
        Interpret Mars transit effects.

        Mars transit brings energy, action, courage, or conflicts.

        Args:
            transit_data: Mars transit information

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            current_sign = transit_data.get('current_sign', '')
            transit_quality = transit_data.get('transit_quality', '')

            interpretations.append("MARS TRANSIT - Energy & Action")
            interpretations.append("=" * 50)
            interpretations.append(f"Mars is currently in {current_sign}")
            interpretations.append("Mars transits take ~45 days per sign")

            if transit_quality == 'Benefic':
                interpretations.append(
                    f"✓ Mars in {current_sign}: Strong period for action and initiative"
                )
                interpretations.append(
                    "Good for starting projects, physical activities, and competitive ventures"
                )
            else:
                interpretations.append(
                    f"⚠ Mars in {current_sign}: Prone to conflicts and arguments"
                )
                interpretations.append(
                    "Exercise caution in aggressive actions and maintain patience"
                )

            interpretations.append(
                "Mars transit affects: courage, energy, conflicts, physical strength"
            )
            interpretations.append(
                "Avoid impulsive decisions during Mars transit in challenging positions"
            )

        except Exception as e:
            logger.error(f"Error interpreting Mars transit: {str(e)}")

        return interpretations

    @staticmethod
    def interpret_mercury_transit(transit_data: Dict) -> List[str]:
        """
        Interpret Mercury transit effects.

        Mercury transit affects communication, thinking, and travel.

        Args:
            transit_data: Mercury transit information

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            current_sign = transit_data.get('current_sign', '')

            interpretations.append("MERCURY TRANSIT - Communication & Intellect")
            interpretations.append("=" * 50)
            interpretations.append(f"Mercury is currently in {current_sign}")
            interpretations.append("Mercury transits take 14-30 days per sign")

            interpretations.append(
                f"Mercury in {current_sign} affects: communication style, thinking process, travel"
            )
            interpretations.append(
                "Good period for: writing, speaking, negotiations, short journeys"
            )
            interpretations.append(
                "Caution: Mercury can cause confusion and communication delays"
            )
            interpretations.append(
                "Pay attention to contracts, agreements, and important communications"
            )

        except Exception as e:
            logger.error(f"Error interpreting Mercury transit: {str(e)}")

        return interpretations

    @staticmethod
    def interpret_venus_transit(transit_data: Dict) -> List[str]:
        """
        Interpret Venus transit effects.

        Venus transit brings harmony, relationships, and financial benefits.

        Args:
            transit_data: Venus transit information

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            current_sign = transit_data.get('current_sign', '')

            interpretations.append("VENUS TRANSIT - Love, Relationships & Finance")
            interpretations.append("=" * 50)
            interpretations.append(f"Venus is currently in {current_sign}")
            interpretations.append("Venus transits take ~28 days per sign")

            interpretations.append(
                f"Venus in {current_sign}: Favorable for relationships and finances"
            )
            interpretations.append(
                "Good for: romance, marriage talks, financial agreements, artistic pursuits"
            )
            interpretations.append(
                "Venus brings harmony and pleasure during its transit through your chart"
            )
            interpretations.append(
                "Invest in relationships, beauty, and comfort during this period"
            )

        except Exception as e:
            logger.error(f"Error interpreting Venus transit: {str(e)}")

        return interpretations

    @staticmethod
    def interpret_jupiter_transit(transit_data: Dict) -> List[str]:
        """
        Interpret Jupiter transit effects.

        Jupiter brings expansion, luck, and growth.

        Args:
            transit_data: Jupiter transit information

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            current_sign = transit_data.get('current_sign', '')

            interpretations.append("JUPITER TRANSIT - Expansion & Good Fortune")
            interpretations.append("=" * 50)
            interpretations.append(f"Jupiter is currently in {current_sign}")
            interpretations.append("Jupiter transits take ~1 year per sign (12-13 months)")

            interpretations.append(
                f"✓ Jupiter in {current_sign}: Very favorable period for growth"
            )
            interpretations.append(
                "Opportunities for expansion in {0} matters".format(current_sign.lower())
            )
            interpretations.append(
                "Good for: education, travel, business expansion, spiritual growth"
            )
            interpretations.append(
                "Jupiter is the great benefic - take advantage of opportunities presented"
            )
            interpretations.append(
                "This 12-month period brings luck and positive developments"
            )

        except Exception as e:
            logger.error(f"Error interpreting Jupiter transit: {str(e)}")

        return interpretations

    @staticmethod
    def interpret_saturn_transit(transit_data: Dict) -> List[str]:
        """
        Interpret Saturn transit effects.

        Saturn brings lessons, restrictions, and long-term growth.

        Args:
            transit_data: Saturn transit information

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            current_sign = transit_data.get('current_sign', '')

            interpretations.append("SATURN TRANSIT - Lessons & Long-term Growth")
            interpretations.append("=" * 50)
            interpretations.append(f"Saturn is currently in {current_sign}")
            interpretations.append("Saturn transits take ~2.5 years per sign (important life periods)")

            interpretations.append(
                "⚠ Saturn Transit: This is a testing and maturation period"
            )
            interpretations.append(
                f"Saturn in {current_sign} brings lessons and restrictions to that area"
            )
            interpretations.append(
                "Challenges: obstacles, delays, hard work required"
            )
            interpretations.append(
                "Opportunities: building foundations, discipline, lasting results"
            )
            interpretations.append(
                "Saturn's 2.5-year transit builds character and long-term success"
            )
            interpretations.append(
                "Use this period to work hard, accept responsibilities, and grow"
            )

        except Exception as e:
            logger.error(f"Error interpreting Saturn transit: {str(e)}")

        return interpretations

    @staticmethod
    def interpret_rahu_transit(transit_data: Dict) -> List[str]:
        """
        Interpret Rahu transit effects.

        Rahu brings obsessions, growth, and new ventures.

        Args:
            transit_data: Rahu transit information

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            current_sign = transit_data.get('current_sign', '')

            interpretations.append("RAHU TRANSIT - New Growth & Obsessions")
            interpretations.append("=" * 50)
            interpretations.append(f"Rahu is currently in {current_sign}")
            interpretations.append("Rahu transits take ~1.5 years per sign (major life transitions)")

            interpretations.append(
                f"Rahu in {current_sign}: Brings new opportunities and growth in this area"
            )
            interpretations.append(
                "Rahu effect: strong desires, new ventures, unconventional paths"
            )
            interpretations.append(
                "Potential: growth, expansion, success in new fields"
            )
            interpretations.append(
                "Caution: obsessions, illusions, and deceptive situations possible"
            )
            interpretations.append(
                "Use Rahu's transit to pursue new ventures and unconventional goals"
            )

        except Exception as e:
            logger.error(f"Error interpreting Rahu transit: {str(e)}")

        return interpretations

    @staticmethod
    def interpret_ketu_transit(transit_data: Dict) -> List[str]:
        """
        Interpret Ketu transit effects.

        Ketu brings spiritual lessons and release.

        Args:
            transit_data: Ketu transit information

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            current_sign = transit_data.get('current_sign', '')

            interpretations.append("KETU TRANSIT - Spiritual Lessons & Release")
            interpretations.append("=" * 50)
            interpretations.append(f"Ketu is currently in {current_sign}")
            interpretations.append("Ketu transits take ~1.5 years per sign (spiritual transformation)")

            interpretations.append(
                f"Ketu in {current_sign}: Brings spiritual lessons and detachment from worldly matters"
            )
            interpretations.append(
                "Ketu effect: lessons from past, letting go, spiritual growth"
            )
            interpretations.append(
                "Potential: spiritual development, past karma working out, mystical experiences"
            )
            interpretations.append(
                "Caution: confusion, losses in worldly matters possible"
            )
            interpretations.append(
                "Use Ketu's transit for spiritual practices and introspection"
            )

        except Exception as e:
            logger.error(f"Error interpreting Ketu transit: {str(e)}")

        return interpretations

    @staticmethod
    def get_transit_remedies(planet: str, current_sign: str) -> List[str]:
        """
        Get remedies for challenging transits.

        Args:
            planet: Transiting planet
            current_sign: Current sign of transit

        Returns:
            List of remedy suggestions
        """
        remedies = {
            'Sun': [
                "Engage in activities that boost confidence",
                "Take leadership roles",
                "Spend time outdoors in sunlight",
                "Practice charity and generosity"
            ],
            'Moon': [
                "Maintain emotional balance",
                "Spend time with family",
                "Meditate to calm the mind",
                "Avoid major decisions on emotional days"
            ],
            'Mars': [
                "Channel energy into productive work",
                "Exercise and physical activity",
                "Practice patience and non-violence",
                "Avoid confrontations"
            ],
            'Mercury': [
                "Double-check all communications",
                "Be clear in writing and speaking",
                "Travel safely",
                "Keep important documents organized"
            ],
            'Venus': [
                "Nurture relationships",
                "Engage in artistic pursuits",
                "Practice gratitude for comforts",
                "Support others with love"
            ],
            'Jupiter': [
                "Pursue expansion and growth",
                "Study and gain knowledge",
                "Support education and learning",
                "Practice generosity and charity"
            ],
            'Saturn': [
                "Accept responsibilities with discipline",
                "Work on long-term projects",
                "Practice patience and perseverance",
                "Serve those less fortunate"
            ],
            'Rahu': [
                "Channel desires into productive goals",
                "Pursue unconventional opportunities",
                "Practice meditation and grounding",
                "Avoid obsessions and addictions"
            ],
            'Ketu': [
                "Engage in spiritual practices",
                "Meditate regularly",
                "Study metaphysics and spirituality",
                "Accept losses with grace"
            ]
        }

        return remedies.get(planet, [
            "Practice meditation and yoga",
            "Perform charitable deeds",
            "Maintain positive mindset",
            "Accept planetary influences with grace"
        ])

    @staticmethod
    def analyze_transit_house_passage(current_sign: str, birth_chart: Dict) -> List[str]:
        """
        Analyze which house the transiting planet is passing through.

        Args:
            current_sign: Current sign of transit
            birth_chart: Birth chart information

        Returns:
            List of house passage interpretations
        """
        try:
            analysis = []
            houses = birth_chart.get('houses', {})

            analysis.append("HOUSE PASSAGE ANALYSIS")
            analysis.append("=" * 50)

            # Find which house this sign corresponds to
            analysis.append(f"Transiting planet in {current_sign}")
            analysis.append(
                "The house it passes through is activated and receives focus"
            )
            analysis.append(
                "Transit effects manifest in matters ruled by this house"
            )

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing house passage: {str(e)}")
            return []
