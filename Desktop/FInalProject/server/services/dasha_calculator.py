"""
Dasha Calculator Module
Implements Vimshottari Dasha system for astrological life period calculations.

The Dasha system is based on a 120-year cycle divided among 9 planets,
starting from the planet that rules the Moon's natal nakshatra (lunar mansion).

Author: Astrology Backend
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DashaCalculator:
    """
    Calculates Vimshottari Dasha periods and sub-periods based on Moon's nakshatra.

    Dasha Periods (in years):
    - Ketu: 7, Venus: 20, Sun: 6, Moon: 10, Mars: 7, Rahu: 18, Jupiter: 16, Saturn: 19, Mercury: 17
    Total: 120 years
    """

    # Dasha duration in years for each planet
    DASHA_DURATIONS = {
        'Ketu': 7,
        'Venus': 20,
        'Sun': 6,
        'Moon': 10,
        'Mars': 7,
        'Rahu': 18,
        'Jupiter': 16,
        'Saturn': 19,
        'Mercury': 17
    }

    # Order of Dasha periods in 120-year cycle
    DASHA_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

    # Nakshatras and their ruling planets (0-27 degrees mapped to 27 nakshatras)
    NAKSHATRA_LORDS = {
        0: 'Ketu',      # Ashwini (0-3:20)
        1: 'Venus',     # Bharani (3:20-6:40)
        2: 'Sun',       # Krittika (6:40-10:00)
        3: 'Moon',      # Rohini (10:00-13:20)
        4: 'Mars',      # Mrigashira (13:20-16:40)
        5: 'Rahu',      # Ardra (16:40-20:00)
        6: 'Jupiter',   # Punarvasu (20:00-23:20)
        7: 'Saturn',    # Pushya (23:20-26:40)
        8: 'Mercury',   # Ashlesha (26:40-30:00)
    }

    def __init__(self, birth_date: datetime, birth_time: str, moon_longitude: float):
        """
        Initialize Dasha Calculator.

        Args:
            birth_date: Birth date as datetime object
            birth_time: Birth time as string (HH:MM format)
            moon_longitude: Moon's longitude in degrees (0-360)
        """
        self.birth_date = birth_date
        self.birth_time = birth_time
        self.moon_longitude = moon_longitude

    def get_nakshatra_from_longitude(self, longitude: float) -> Tuple[int, str]:
        """
        Get nakshatra number and name from longitude.

        Args:
            longitude: Celestial longitude (0-360 degrees)

        Returns:
            Tuple of (nakshatra_number: 0-26, nakshatra_name: str)
        """
        # Normalize longitude to 0-360
        longitude = longitude % 360

        # Each nakshatra spans 360/27 = 13.333 degrees
        nakshatra_num = int(longitude / (360 / 27))

        # Ensure nakshatra_num is within 0-26
        nakshatra_num = min(nakshatra_num, 26)

        nakshatra_names = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira',
            'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha',
            'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra',
            'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula',
            'Purva Ashadha', 'Uttara Ashadha', 'Abhijit', 'Shravana',
            'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada'
        ]

        return nakshatra_num, nakshatra_names[nakshatra_num]

    def get_dasha_lord_from_nakshatra(self, nakshatra_num: int) -> str:
        """
        Get the Dasha lord (ruling planet) for a given nakshatra.

        Args:
            nakshatra_num: Nakshatra number (0-26)

        Returns:
            Planet name that rules this nakshatra
        """
        # Each set of 3 nakshatras (0-2, 3-5, 6-8...) is ruled by a planet
        # This maps to the order: Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury
        lord_index = (nakshatra_num // 3) % 9
        return self.DASHA_ORDER[lord_index]

    def calculate_dasha_balance(self) -> Tuple[str, float, float]:
        """
        Calculate the current Dasha lord and remaining days in current Dasha.

        Returns:
            Tuple of (current_dasha_lord, remaining_years, remaining_months)
        """
        # Get Moon's nakshatra
        nakshatra_num, nakshatra_name = self.get_nakshatra_from_longitude(self.moon_longitude)
        starting_dasha_lord = self.get_dasha_lord_from_nakshatra(nakshatra_num)

        # Calculate Moon's position within its nakshatra (0-1, where 1 = complete)
        nakshatra_start = nakshatra_num * (360 / 27)
        nakshatra_end = (nakshatra_num + 1) * (360 / 27)
        moon_position_in_nakshatra = (self.moon_longitude - nakshatra_start) / (nakshatra_end - nakshatra_start)
        moon_position_in_nakshatra = max(0, min(1, moon_position_in_nakshatra))

        # Get duration of starting dasha
        starting_dasha_duration = self.DASHA_DURATIONS[starting_dasha_lord]

        # Calculate remaining years in starting dasha
        remaining_years = starting_dasha_duration * (1 - moon_position_in_nakshatra)
        remaining_months = remaining_years * 12

        return starting_dasha_lord, remaining_years, remaining_months

    def calculate_maha_dasha_timeline(self) -> List[Dict]:
        """
        Calculate complete 120-year Maha Dasha (major period) timeline.

        Returns:
            List of dicts with Dasha information:
            [{
                'planet': str,
                'duration': int,
                'start_year': int,
                'end_year': int,
                'is_current': bool
            }]
        """
        current_dasha_lord, remaining_years, remaining_months = self.calculate_dasha_balance()
        current_age_in_dasha = self.DASHA_DURATIONS[current_dasha_lord] - remaining_years

        timeline = []
        cumulative_years = -current_age_in_dasha

        # Find starting index in dasha order
        starting_index = self.DASHA_ORDER.index(current_dasha_lord)

        # Generate complete 120-year cycle
        for i in range(9):
            dasha_index = (starting_index + i) % 9
            planet = self.DASHA_ORDER[dasha_index]
            duration = self.DASHA_DURATIONS[planet]

            start_year = int(cumulative_years)
            end_year = start_year + duration

            is_current = (i == 0)

            timeline.append({
                'planet': planet,
                'duration': duration,
                'start_year': start_year,
                'end_year': end_year,
                'is_current': is_current,
                'remaining_years': remaining_years if is_current else None
            })

            cumulative_years += duration

        return timeline

    def calculate_antar_dasha(self, maha_dasha_lord: Optional[str] = None) -> List[Dict]:
        """
        Calculate Antar Dasha (sub-periods) within a Maha Dasha.

        Each Antar Dasha = (Maha Dasha Duration × Antar Lord Duration) / 120

        Args:
            maha_dasha_lord: Planet name for which to calculate Antar Dasha.
                           If None, uses current Dasha lord.

        Returns:
            List of dicts with Antar Dasha information:
            [{
                'planet': str,
                'duration_years': float,
                'duration_months': int,
                'duration_days': int,
                'is_current': bool
            }]
        """
        if maha_dasha_lord is None:
            maha_dasha_lord, _, _ = self.calculate_dasha_balance()

        maha_duration = self.DASHA_DURATIONS[maha_dasha_lord]
        antar_dasha_list = []

        for planet in self.DASHA_ORDER:
            planet_duration = self.DASHA_DURATIONS[planet]

            # Antar Dasha duration in years
            antar_duration_years = (maha_duration * planet_duration) / 120.0

            # Convert to months and days
            total_days = antar_duration_years * 365.25
            total_months = antar_duration_years * 12
            days = int((antar_duration_years % 1) * 365.25)
            months = int(total_months % 12)

            antar_dasha_list.append({
                'planet': planet,
                'duration_years': round(antar_duration_years, 2),
                'duration_months': int(total_months),
                'duration_days': int(total_days),
                'is_current': False  # Will be marked by calling function
            })

        return antar_dasha_list

    def calculate_complete_dasha_info(self) -> Dict:
        """
        Calculate complete Dasha information including Maha and Antar periods.

        Returns:
            Comprehensive dasha dictionary with all information
        """
        try:
            # Get current Dasha info
            current_dasha_lord, remaining_years, remaining_months = self.calculate_dasha_balance()

            # Get nakshatra info
            nakshatra_num, nakshatra_name = self.get_nakshatra_from_longitude(self.moon_longitude)

            # Get Maha Dasha timeline
            maha_timeline = self.calculate_maha_dasha_timeline()

            # Get Antar Dasha for current Maha Dasha
            antar_timeline = self.calculate_antar_dasha(current_dasha_lord)

            # Calculate birth date from age
            dasha_duration = self.DASHA_DURATIONS[current_dasha_lord]
            dasha_start_date = self.birth_date + timedelta(days=-remaining_years * 365.25)
            dasha_end_date = dasha_start_date + timedelta(days=dasha_duration * 365.25)

            return {
                'moon_nakshatra': nakshatra_name,
                'moon_nakshatra_number': nakshatra_num,
                'current_maha_dasha': current_dasha_lord,
                'maha_dasha_start_date': dasha_start_date.strftime('%Y-%m-%d'),
                'maha_dasha_end_date': dasha_end_date.strftime('%Y-%m-%d'),
                'maha_dasha_duration_years': dasha_duration,
                'remaining_maha_dasha_years': round(remaining_years, 2),
                'remaining_maha_dasha_months': round(remaining_months, 1),
                'completed_maha_dasha_years': round(dasha_duration - remaining_years, 2),
                'current_antar_dasha': antar_timeline[0]['planet'] if antar_timeline else None,
                'current_antar_dasha_duration_days': antar_timeline[0]['duration_days'] if antar_timeline else None,
                'maha_dasha_timeline': maha_timeline,
                'antar_dasha_timeline': antar_timeline,
                'next_dasha_lord': maha_timeline[1]['planet'] if len(maha_timeline) > 1 else None
            }

        except Exception as e:
            logger.error(f"Error calculating Dasha information: {str(e)}", exc_info=True)
            return {
                'error': str(e),
                'current_maha_dasha': None,
                'maha_dasha_timeline': [],
                'antar_dasha_timeline': []
            }

    def get_dasha_characteristics(self, planet: str) -> Dict[str, str]:
        """
        Get characteristics and interpretations of a Dasha period.

        Args:
            planet: Planet name

        Returns:
            Dictionary with interpretations and characteristics
        """
        characteristics = {
            'Sun': {
                'duration': '6 years',
                'signification': 'Self, father, government, authority, power',
                'positive_effects': 'Gain in power, status, authority; achievement; recognition',
                'negative_effects': 'Ego issues; health problems; conflicts with authority',
                'best_for': 'Government jobs, leadership, political success',
                'challenges': 'Arrogance, pride, health issues'
            },
            'Moon': {
                'duration': '10 years',
                'signification': 'Mind, emotions, mother, comfort, public acceptance',
                'positive_effects': 'Emotional stability; gains through mother; public favor; travel',
                'negative_effects': 'Emotional turbulence; depression; health issues; rumors',
                'best_for': 'Emotional healing, travel, public work, family matters',
                'challenges': 'Mood swings, anxiety, instability'
            },
            'Mars': {
                'duration': '7 years',
                'signification': 'Energy, courage, conflict, surgery, siblings, property',
                'positive_effects': 'Courage; success in competition; property gains; surgery benefits',
                'negative_effects': 'Accidents; conflicts; diseases; financial losses',
                'best_for': 'Military, sports, competitive endeavors, property matters',
                'challenges': 'Accidents, surgeries, conflicts, aggression'
            },
            'Mercury': {
                'duration': '17 years',
                'signification': 'Communication, intelligence, business, commerce, education',
                'positive_effects': 'Communication success; business growth; education; intellectual development',
                'negative_effects': 'Confusion; business losses; communication failures',
                'best_for': 'Business, teaching, writing, trade, contracts',
                'challenges': 'Nervousness, confusion, misunderstandings'
            },
            'Jupiter': {
                'duration': '16 years',
                'signification': 'Wisdom, children, prosperity, luck, dharma, higher learning',
                'positive_effects': 'Expansion; prosperity; children; religious inclination; wisdom',
                'negative_effects': 'Over-expansion; legal issues; weight gain',
                'best_for': 'Higher education, spirituality, children, wealth accumulation',
                'challenges': 'Overindulgence, excessive spending'
            },
            'Venus': {
                'duration': '20 years',
                'signification': 'Love, marriage, beauty, arts, vehicles, comforts, enjoyment',
                'positive_effects': 'Marriage; love relationships; artistic gains; vehicles; comforts',
                'negative_effects': 'Relationship issues; excess indulgence; health problems',
                'best_for': 'Marriage, arts, entertainment, luxury business',
                'challenges': 'Relationship complications, excess, sensuality'
            },
            'Saturn': {
                'duration': '19 years',
                'signification': 'Discipline, karma, delays, longevity, service, hard work',
                'positive_effects': 'Spiritual growth; discipline; building solid foundation; longevity',
                'negative_effects': 'Delays; difficulties; health issues; loss; hardships',
                'best_for': 'Spiritual practice, discipline, building lasting structures',
                'challenges': 'Delays, hardships, health issues, depression'
            },
            'Rahu': {
                'duration': '18 years',
                'signification': 'Illusion, obsession, foreign matters, technology, unconventional success',
                'positive_effects': 'Unexpected gains; foreign travel; technology success; fame',
                'negative_effects': 'Illusion; obsession; addictions; accidents; losses',
                'best_for': 'Technology, foreign business, unconventional ventures',
                'challenges': 'Illusions, addictions, unexpected difficulties'
            },
            'Ketu': {
                'duration': '7 years',
                'signification': 'Spiritual growth, detachment, liberation, mysteries, occult',
                'positive_effects': 'Spiritual advancement; detachment; mystical understanding; liberation',
                'negative_effects': 'Health issues; confusion; isolation; losses',
                'best_for': 'Spiritual practice, meditation, occult studies',
                'challenges': 'Isolation, health problems, confusion'
            }
        }

        return characteristics.get(planet, {
            'duration': 'Unknown',
            'signification': 'Unknown',
            'positive_effects': 'Unknown',
            'negative_effects': 'Unknown',
            'best_for': 'Unknown',
            'challenges': 'Unknown'
        })
