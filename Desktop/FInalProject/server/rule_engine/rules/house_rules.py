"""
House Interpretation Rules
Provides meaningful interpretations for house analysis.

Each house represents specific life areas and shows how they are affected
by planetary placements and house lord strength.

Author: Astrology Backend
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class HouseRules:
    """Generate interpretations for house analysis."""

    # Detailed interpretations for each house
    HOUSE_DESCRIPTIONS = {
        1: "House of Self - Personality, appearance, health, and personal identity",
        2: "House of Wealth - Money, family, speech, and material possessions",
        3: "House of Siblings - Siblings, communication, courage, and short journeys",
        4: "House of Home - Mother, home, property, land, and domestic happiness",
        5: "House of Children - Children, creativity, romance, and intellect",
        6: "House of Health - Enemies, disease, service, and debts",
        7: "House of Marriage - Partnerships, marriage, spouse, and public relations",
        8: "House of Longevity - Death, inheritance, occult, and hidden matters",
        9: "House of Luck - Father, luck, dharma, religion, and long journeys",
        10: "House of Career - Career, public image, authority, and honor",
        11: "House of Gains - Income, friends, wishes, and social groups",
        12: "House of Losses - Spirituality, losses, seclusion, and foreign lands"
    }

    @staticmethod
    def interpret_house(house_analysis: Dict) -> List[str]:
        """
        Generate comprehensive interpretation for a house.

        Args:
            house_analysis: Complete house analysis data

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            house_num = house_analysis.get('house_number', 0)
            house_name = house_analysis.get('house_name', '')
            sign = house_analysis.get('sign', '')
            strength = house_analysis.get('strength', '')
            planets = house_analysis.get('planets', [])
            lord = house_analysis.get('lord', '')
            lord_strength = house_analysis.get('lord_strength', '')

            # Header
            interpretations.append(f"HOUSE {house_num} ({house_name})")
            interpretations.append("=" * 60)

            # House description
            if house_num in HouseRules.HOUSE_DESCRIPTIONS:
                interpretations.append(HouseRules.HOUSE_DESCRIPTIONS[house_num])

            # Sign and planets
            interpretations.append(f"\nSign: {sign}")

            if planets:
                interpretations.append(f"Planets: {', '.join(planets)}")
                interpretations.append(
                    "Presence of planets in this house strengthens its matters"
                )
            else:
                interpretations.append(
                    "No planets in this house - see house lord for strength"
                )

            # House lord analysis
            interpretations.append(f"\nHouse Lord: {lord} ({lord_strength})")
            interpretations.append(
                f"The strength of {lord} determines the outcome of {house_name} matters"
            )

            # Specific interpretations by house
            specific = HouseRules._get_specific_interpretation(house_num, sign, planets, lord)
            interpretations.extend(specific)

            # Strength assessment
            interpretations.append(f"\nOverall Strength: {strength}")

            return interpretations

        except Exception as e:
            logger.error(f"Error interpreting house: {str(e)}")
            return ["Unable to generate house interpretation"]

    @staticmethod
    def _get_specific_interpretation(house_num: int, sign: str, planets: List[str],
                                      lord: str) -> List[str]:
        """
        Get specific interpretation based on house number.

        Args:
            house_num: House number
            sign: Sign in house
            planets: Planets in house
            lord: House lord

        Returns:
            List of specific interpretations
        """
        interpretations = []

        try:
            if house_num == 1:
                interpretations.extend(HouseRules._interpret_house_1(sign, planets, lord))
            elif house_num == 2:
                interpretations.extend(HouseRules._interpret_house_2(sign, planets, lord))
            elif house_num == 3:
                interpretations.extend(HouseRules._interpret_house_3(sign, planets, lord))
            elif house_num == 4:
                interpretations.extend(HouseRules._interpret_house_4(sign, planets, lord))
            elif house_num == 5:
                interpretations.extend(HouseRules._interpret_house_5(sign, planets, lord))
            elif house_num == 6:
                interpretations.extend(HouseRules._interpret_house_6(sign, planets, lord))
            elif house_num == 7:
                interpretations.extend(HouseRules._interpret_house_7(sign, planets, lord))
            elif house_num == 8:
                interpretations.extend(HouseRules._interpret_house_8(sign, planets, lord))
            elif house_num == 9:
                interpretations.extend(HouseRules._interpret_house_9(sign, planets, lord))
            elif house_num == 10:
                interpretations.extend(HouseRules._interpret_house_10(sign, planets, lord))
            elif house_num == 11:
                interpretations.extend(HouseRules._interpret_house_11(sign, planets, lord))
            elif house_num == 12:
                interpretations.extend(HouseRules._interpret_house_12(sign, planets, lord))

        except Exception as e:
            logger.error(f"Error getting specific house interpretation: {str(e)}")

        return interpretations

    @staticmethod
    def _interpret_house_1(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 1: Self and Personality"""
        interpretations = ["\nHOUSE 1 ANALYSIS:"]
        interpretations.append(
            f"Your natural personality and appearance are influenced by {sign}"
        )
        if 'Sun' in planets:
            interpretations.append("✓ Sun in 1st: Strong personality, natural leader")
        if 'Moon' in planets:
            interpretations.append("✓ Moon in 1st: Emotional, responsive, intuitive personality")
        if 'Mars' in planets:
            interpretations.append("⚠ Mars in 1st: Aggressive, courageous but can be temperamental")
        interpretations.append(
            f"Your {lord} as house lord determines your overall health and vitality"
        )
        return interpretations

    @staticmethod
    def _interpret_house_2(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 2: Wealth and Family"""
        interpretations = ["\nHOUSE 2 ANALYSIS:"]
        interpretations.append(
            f"Financial prospects indicated by {sign} and {lord}"
        )
        if 'Jupiter' in planets:
            interpretations.append("✓ Jupiter in 2nd: Strong financial gains, wealth accumulation")
        if 'Venus' in planets:
            interpretations.append("✓ Venus in 2nd: Luxury, comfort, and material prosperity")
        if 'Saturn' in planets:
            interpretations.append("⚠ Saturn in 2nd: Delays in wealth, need for hard work")
        interpretations.append(
            "Invest in education and skill development for long-term financial growth"
        )
        return interpretations

    @staticmethod
    def _interpret_house_3(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 3: Siblings and Communication"""
        interpretations = ["\nHOUSE 3 ANALYSIS:"]
        interpretations.append(
            f"Relationship with siblings: {sign} temperament, {lord} influence"
        )
        if 'Mercury' in planets:
            interpretations.append("✓ Mercury in 3rd: Excellent communication skills")
        if 'Mars' in planets:
            interpretations.append("⚠ Mars in 3rd: Conflict with siblings possible, be tactful")
        interpretations.append(
            "Develop your communication abilities - they are your greatest asset"
        )
        return interpretations

    @staticmethod
    def _interpret_house_4(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 4: Home and Mother"""
        interpretations = ["\nHOUSE 4 ANALYSIS:"]
        interpretations.append(
            f"Domestic happiness and mother's well-being: {sign}, with {lord} influence"
        )
        if 'Moon' in planets:
            interpretations.append("✓ Moon in 4th: Very favorable for home and mother")
        if 'Venus' in planets:
            interpretations.append("✓ Venus in 4th: Beautiful home, material comforts")
        if 'Mars' in planets:
            interpretations.append("⚠ Mars in 4th: Disputes at home, need for harmony")
        interpretations.append(
            "Focus on home renovation and family relationships for happiness"
        )
        return interpretations

    @staticmethod
    def _interpret_house_5(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 5: Children and Creativity"""
        interpretations = ["\nHOUSE 5 ANALYSIS:"]
        interpretations.append(
            f"Children and creativity indicated by {sign}, strengthened by {lord}"
        )
        if 'Jupiter' in planets:
            interpretations.append("✓ Jupiter in 5th: Blessings of children, great creativity")
        if 'Sun' in planets:
            interpretations.append("✓ Sun in 5th: Strong children, creative talents")
        if 'Saturn' in planets:
            interpretations.append("⚠ Saturn in 5th: Delays in children, need patience")
        interpretations.append(
            "Engage in creative pursuits and invest in children's education"
        )
        return interpretations

    @staticmethod
    def _interpret_house_6(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 6: Health and Enemies"""
        interpretations = ["\nHOUSE 6 ANALYSIS:"]
        interpretations.append(
            f"Health and enemies: {sign} sign, with {lord} protection"
        )
        if 'Mars' in planets:
            interpretations.append("⚠ Mars in 6th: Accidents possible, maintain caution")
        if 'Saturn' in planets:
            interpretations.append("⚠ Saturn in 6th: Chronic health issues, preventive care needed")
        interpretations.append(
            "Focus on preventive healthcare and avoid enemies through good conduct"
        )
        return interpretations

    @staticmethod
    def _interpret_house_7(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 7: Marriage and Partnership"""
        interpretations = ["\nHOUSE 7 ANALYSIS:"]
        interpretations.append(
            f"Marriage and partnerships: {sign} sign, {lord} as significator"
        )
        if 'Venus' in planets:
            interpretations.append("✓ Venus in 7th: Happy marriage, loving spouse")
        if 'Mars' in planets:
            interpretations.append("⚠ Mars in 7th: Marital conflicts possible, need patience")
        if 'Saturn' in planets:
            interpretations.append("⚠ Saturn in 7th: Delayed marriage, older spouse likely")
        interpretations.append(
            "Study your spouse's chart (D9 Navamsha) for compatibility"
        )
        return interpretations

    @staticmethod
    def _interpret_house_8(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 8: Longevity and Inheritance"""
        interpretations = ["\nHOUSE 8 ANALYSIS:"]
        interpretations.append(
            f"Longevity and inheritance: {sign}, with {lord} influence on lifespan"
        )
        if planets:
            interpretations.append(
                "Planets here indicate inheritance and unexpected gains"
            )
        interpretations.append(
            "Study occult sciences and spirituality for transformation"
        )
        return interpretations

    @staticmethod
    def _interpret_house_9(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 9: Luck and Dharma"""
        interpretations = ["\nHOUSE 9 ANALYSIS:"]
        interpretations.append(
            f"Luck and spiritual path: {sign}, with {lord} determining fortune"
        )
        if 'Jupiter' in planets:
            interpretations.append("✓ Jupiter in 9th: Excellent luck, spiritual growth")
        if 'Sun' in planets:
            interpretations.append("✓ Sun in 9th: Fame and recognition, righteous path")
        interpretations.append(
            "Engage in spiritual practices and study for enhanced wisdom"
        )
        return interpretations

    @staticmethod
    def _interpret_house_10(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 10: Career and Status"""
        interpretations = ["\nHOUSE 10 ANALYSIS:"]
        interpretations.append(
            f"Career and public image: {sign}, with {lord} determining success"
        )
        if 'Sun' in planets:
            interpretations.append("✓ Sun in 10th: Leadership, high status, recognition")
        if 'Saturn' in planets:
            interpretations.append("✓ Saturn in 10th: Long-term career success through hard work")
        if 'Mars' in planets:
            interpretations.append("✓ Mars in 10th: Aggressive career growth, competitive drive")
        interpretations.append(
            "Build professional reputation and work towards long-term career goals"
        )
        return interpretations

    @staticmethod
    def _interpret_house_11(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 11: Gains and Friendships"""
        interpretations = ["\nHOUSE 11 ANALYSIS:"]
        interpretations.append(
            f"Financial gains and friends: {sign}, with {lord} bringing opportunities"
        )
        if 'Jupiter' in planets:
            interpretations.append("✓ Jupiter in 11th: Income gains, beneficial groups")
        if 'Mercury' in planets:
            interpretations.append("✓ Mercury in 11th: Business success, many friends")
        interpretations.append(
            "Network with beneficial people and pursue collective goals"
        )
        return interpretations

    @staticmethod
    def _interpret_house_12(sign: str, planets: List[str], lord: str) -> List[str]:
        """House 12: Spirituality and Losses"""
        interpretations = ["\nHOUSE 12 ANALYSIS:"]
        interpretations.append(
            f"Spirituality and losses: {sign}, with {lord} influence on seclusion"
        )
        if 'Ketu' in planets:
            interpretations.append("✓ Ketu in 12th: Strong spirituality, mystical experiences")
        if 'Saturn' in planets:
            interpretations.append("✓ Saturn in 12th: Spiritual discipline, meditation beneficial")
        interpretations.append(
            "Engage in charitable work and spiritual practices for evolution"
        )
        return interpretations

    @staticmethod
    def get_house_recommendations(all_houses: Dict) -> List[str]:
        """
        Get general recommendations based on house analysis.

        Args:
            all_houses: Complete house analysis

        Returns:
            List of recommendations
        """
        recommendations = []

        try:
            # Find strongest house
            strongest = None
            strongest_strength = 0
            for house_num, analysis in all_houses.items():
                strength_val = 0
                if 'Strong' in analysis.get('strength', ''):
                    strength_val = 2
                elif 'Moderate' in analysis.get('strength', ''):
                    strength_val = 1

                if strength_val > strongest_strength:
                    strongest_strength = strength_val
                    strongest = (house_num, analysis)

            # Find weakest house
            weakest = None
            weakest_strength = 999
            for house_num, analysis in all_houses.items():
                strength_val = 999
                if 'Strong' in analysis.get('strength', ''):
                    strength_val = 2
                elif 'Moderate' in analysis.get('strength', ''):
                    strength_val = 1
                else:
                    strength_val = 0

                if strength_val < weakest_strength:
                    weakest_strength = strength_val
                    weakest = (house_num, analysis)

            if strongest:
                recommendations.append(
                    f"Leverage strength of House {strongest[0]} ({strongest[1].get('house_name')})"
                )
                recommendations.append(
                    "This is your area of natural strength and talent"
                )

            if weakest:
                recommendations.append(
                    f"Address weakness in House {weakest[0]} ({weakest[1].get('house_name')})"
                )
                recommendations.append(
                    "Apply remedies to strengthen this house"
                )

            recommendations.append(
                "Use transit and dasha timings to initiate important activities"
            )
            recommendations.append(
                "Regularly review and strengthen weaker houses through practices"
            )

        except Exception as e:
            logger.error(f"Error generating house recommendations: {str(e)}")

        return recommendations
