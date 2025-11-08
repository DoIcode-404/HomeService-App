# from datetime import datetime
# import pytz
# import swisseph
# from server.pydantic_schemas.kundali_schema import KundaliRequest


# def get_julian_day_from_birth_details(birth_details: KundaliRequest) -> float:
#     """
#     Convert birth details to UTC and calculate Julian Day.
#     """
#     dt = datetime.strptime(f"{birth_details.birthDate} {birth_details.birthTime}", "%Y-%m-%d %H:%M")
#     tz = pytz.timezone(birth_details.timezone)
#     dt = tz.localize(dt)
#     utc_time = dt.astimezone(pytz.UTC)

#     return swisseph.julday(
#         utc_time.year,
#         utc_time.month,
#         utc_time.day,
#         utc_time.hour + utc_time.minute / 60.0 + utc_time.second / 3600.0
#     )

# def get_zodiac_sign(longitude):
#     """
#     Determine the zodiac sign based on the sidereal longitude.
#     """
#     # zodiac_signs = [
#     #     "Aries (Mesha)", "Taurus (Vrishabha)", "Gemini (Mithuna)", "Cancer (Karka)",
#     #     "Leo (Simha)", "Virgo (Kanya)", "Libra (Tula)", "Scorpio (Vrishchika)",
#     #     "Sagittarius (Dhanu)", "Capricorn (Makara)", "Aquarius (Kumbha)", "Pisces (Meena)"
#     # ]
#     zodiac_signs = [
#         "Aries", "Taurus", "Gemini ", "Cancer ","Leo", "Virgo", "Libra", "Scorpio",
#         "Sagittarius", "Capricorn", "Aquarius", "Pisces"
#     ]
#     sign_index = int(longitude / 30)
#     return zodiac_signs[sign_index]


# def calculate_planet_positions(jd):
#     """
#     Calculate accurate sidereal positions for all planets, including Rahu and Ketu.
#     """
#     ayanamsa = swisseph.get_ayanamsa(jd)  # Use Lahiri ayanamsa
#     planets = {
#         "Sun": swisseph.SUN,
#         "Moon": swisseph.MOON,
#         "Mars": swisseph.MARS,
#         "Mercury": swisseph.MERCURY,
#         "Jupiter": swisseph.JUPITER,
#         "Venus": swisseph.VENUS,
#         "Saturn": swisseph.SATURN,
#         "Rahu": swisseph.MEAN_NODE,  # Mean node for Rahu
#     }
#     positions = {}

#     for planet_name, planet_id in planets.items():
#         flag = swisseph.FLG_SWIEPH | swisseph.FLG_SPEED  # Use Swiss Ephemeris with speed flag
#         result = swisseph.calc_ut(jd, planet_id, flag)
#         tropical_longitude = result[0][0]  # Get the tropical position
#         sidereal_longitude = (tropical_longitude - ayanamsa) % 360  # Convert to sidereal
#         positions[planet_name] = sidereal_longitude

#     # Ketu is 180° opposite to Rahu
#     positions["Ketu"] = (positions["Rahu"] + 180) % 360
#     return positions


# def calculate_ascendant(jd, lat, lon):
#     """
#     Calculate the sidereal ascendant based on the Julian Day, latitude, and longitude.
#     """
#     houses = swisseph.houses(jd, lat, lon)[0]  # Tropical ascendant
#     ayanamsa = swisseph.get_ayanamsa(jd)
#     ascendant = (houses[0] - ayanamsa) % 360  # Sidereal ascendant
#     return ascendant


# def assign_planets_to_houses(planet_positions, ascendant):
#     """
#     Assign planets to houses based on the Whole Sign House System.
#     """
#     houses = {i: [] for i in range(1, 13)}  # Create empty house mapping
#     asc_sign = int(ascendant / 30) + 1  # Ascendant sign (1-12)

#     for planet, position in planet_positions.items():
#         planet_sign = int(position / 30) + 1  # Planet's sidereal sign (1-12)
#         house = ((planet_sign - asc_sign) % 12) + 1  # House calculation
#         houses[house].append(planet)  # Assign planet to the house

#     return houses


# def get_nakshatra(longitude):
#     nakshatra_names = [
#         'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 
#         'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 
#         'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra', 
#         'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 
#         'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 
#         'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada', 
#         'Uttara Bhadrapada', 'Revati'
#     ]
#     degrees_per_nakshatra = 360 / 27
#     degrees_per_pada = degrees_per_nakshatra / 4

#     nakshatra_index = int(longitude / degrees_per_nakshatra)
#     pada = int((longitude % degrees_per_nakshatra) / degrees_per_pada) + 1

#     nakshatra_name = nakshatra_names[nakshatra_index]
#     # logger.debug(f"Longitude: {longitude}, Nakshatra: {nakshatra_name}, Pada: {pada}")
#     return nakshatra_name, pada

# def get_ruling_planet(moon_sign):
#     """
#     Determine the ruling planet based on the Moon sign according to Vedic astrology.
#     """
#     ruling_planets = {
#         "Aries": "Mars",
#         "Taurus": "Venus",
#         "Gemini": "Mercury",
#         "Cancer": "Moon",
#         "Leo": "Sun",
#         "Virgo": "Mercury",
#         "Libra": "Venus",
#         "Scorpio": "Mars",
#         "Sagittarius": "Jupiter",
#         "Capricorn": "Saturn",
#         "Aquarius": "Saturn",
#         "Pisces": "Jupiter"
#     }
#     return ruling_planets.get(moon_sign, "Unknown")

# from datetime import datetime
# import pytz
# import swisseph
# from server.pydantic_schemas.kundali_schema import KundaliRequest
# import logging

# # Configure logging for debugging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


# def get_julian_day_from_birth_details(birth_details: KundaliRequest) -> float:
#     """
#     Convert birth details to UTC and calculate Julian Day with enhanced precision.
#     """
#     try:
#         # Parse the datetime string with better error handling
#         dt = datetime.strptime(f"{birth_details.birthDate} {birth_details.birthTime}", "%Y-%m-%d %H:%M")
        
#         # Handle timezone more robustly
#         if hasattr(birth_details, 'timezone') and birth_details.timezone:
#             tz = pytz.timezone(birth_details.timezone)
#         else:
#             # Default to UTC if no timezone provided
#             tz = pytz.UTC
#             logger.warning("No timezone provided, defaulting to UTC")
        
#         # Localize and convert to UTC
#         dt = tz.localize(dt)
#         utc_time = dt.astimezone(pytz.UTC)

#         # Calculate Julian Day with full precision
#         jd = swisseph.julday(
#             utc_time.year,
#             utc_time.month,
#             utc_time.day,
#             utc_time.hour + utc_time.minute / 60.0 + utc_time.second / 3600.0
#         )
        
#         logger.debug(f"Calculated JD: {jd} for UTC time: {utc_time}")
#         return jd
        
#     except Exception as e:
#         logger.error(f"Error calculating Julian Day: {e}")
#         raise ValueError(f"Invalid birth details format: {e}")


# def get_zodiac_sign(longitude):
#     """
#     Determine the zodiac sign based on the sidereal longitude with validation.
#     """
#     # Clean zodiac signs array (removed extra spaces)
#     zodiac_signs = [
#         "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
#         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
#     ]
    
#     # Normalize longitude to 0-360 range
#     longitude = longitude % 360
    
#     # Calculate sign index with validation
#     sign_index = int(longitude / 30)
    
#     # Ensure sign_index is within valid range
#     if sign_index < 0 or sign_index > 11:
#         sign_index = 0
#         logger.warning(f"Invalid sign index calculated, defaulting to Aries")
    
#     return zodiac_signs[sign_index]


# def calculate_planet_positions(jd):
#     """
#     Calculate accurate sidereal positions for all planets with enhanced precision and error handling.
#     """
#     try:
#         # Set sidereal mode to Lahiri (most commonly used in Vedic astrology)
#         swisseph.set_sid_mode(swisseph.SIDM_LAHIRI)
#         ayanamsa = swisseph.get_ayanamsa(jd)
        
#         logger.debug(f"Ayanamsa for JD {jd}: {ayanamsa}")
        
#         planets = {
#             "Sun": swisseph.SUN,
#             "Moon": swisseph.MOON,
#             "Mars": swisseph.MARS,
#             "Mercury": swisseph.MERCURY,
#             "Jupiter": swisseph.JUPITER,
#             "Venus": swisseph.VENUS,
#             "Saturn": swisseph.SATURN,
#             "Rahu": swisseph.MEAN_NODE,  # Mean node for Rahu
#         }
#         positions = {}

#         for planet_name, planet_id in planets.items():
#             try:
#                 # Use high precision flags for maximum accuracy
#                 flag = swisseph.FLG_SWIEPH | swisseph.FLG_SPEED | swisseph.FLG_TOPOCTR
#                 result = swisseph.calc_ut(jd, planet_id, flag)
                
#                 # Check for calculation errors
#                 if result[1] != '':
#                     logger.error(f"Swiss Ephemeris error for {planet_name}: {result[1]}")
#                     continue
                
#                 tropical_longitude = result[0][0]
#                 speed = result[0][3]  # Daily motion
                
#                 # Convert to sidereal with proper normalization
#                 sidereal_longitude = (tropical_longitude - ayanamsa) % 360
                
#                 # Store additional data for enhanced accuracy
#                 positions[planet_name] = {
#                     'longitude': sidereal_longitude,
#                     'tropical_longitude': tropical_longitude,
#                     'speed': speed,
#                     'is_retrograde': speed < 0,
#                     'sign': get_zodiac_sign(sidereal_longitude),
#                     'degree_in_sign': sidereal_longitude % 30
#                 }
                
#                 logger.debug(f"{planet_name}: {sidereal_longitude:.6f}° in {get_zodiac_sign(sidereal_longitude)}")
                
#             except Exception as e:
#                 logger.error(f"Error calculating {planet_name}: {e}")
#                 continue

#         # Calculate Ketu as exact opposite of Rahu with enhanced precision
#         if "Rahu" in positions:
#             rahu_longitude = positions["Rahu"]["longitude"]
#             ketu_longitude = (rahu_longitude + 180) % 360
            
#             positions["Ketu"] = {
#                 'longitude': ketu_longitude,
#                 'tropical_longitude': (positions["Rahu"]["tropical_longitude"] + 180) % 360,
#                 'speed': -positions["Rahu"]["speed"],  # Opposite motion
#                 'is_retrograde': positions["Rahu"]["speed"] > 0,  # Opposite of Rahu
#                 'sign': get_zodiac_sign(ketu_longitude),
#                 'degree_in_sign': ketu_longitude % 30
#             }
        
#         # Return just longitudes for backward compatibility, but store full data
#         simple_positions = {}
#         for planet, data in positions.items():
#             simple_positions[planet] = data['longitude']
            
#         return simple_positions
        
#     except Exception as e:
#         logger.error(f"Error in calculate_planet_positions: {e}")
#         raise RuntimeError(f"Failed to calculate planet positions: {e}")


# def calculate_ascendant(jd, lat, lon):
#     """
#     Calculate the sidereal ascendant with enhanced precision and validation.
#     """
#     try:
#         # Validate coordinates
#         if not (-90 <= lat <= 90):
#             raise ValueError(f"Invalid latitude: {lat}. Must be between -90 and 90.")
#         if not (-180 <= lon <= 180):
#             raise ValueError(f"Invalid longitude: {lon}. Must be between -180 and 180.")
        
#         # Set sidereal mode consistently
#         swisseph.set_sid_mode(swisseph.SIDM_LAHIRI)
#         ayanamsa = swisseph.get_ayanamsa(jd)
        
#         # Calculate houses with proper house system (Placidus is default)
#         houses_result = swisseph.houses(jd, lat, lon, b'P')  # 'P' for Placidus
        
#         if not houses_result or len(houses_result) < 2:
#             raise RuntimeError("Failed to calculate houses")
        
#         houses = houses_result[0]  # House cusps
#         ascmc = houses_result[1]   # Ascendant, MC, etc.
        
#         # Get tropical ascendant (first element is ascendant)
#         tropical_ascendant = ascmc[0]
        
#         # Convert to sidereal with proper normalization
#         sidereal_ascendant = (tropical_ascendant - ayanamsa) % 360
        
#         logger.debug(f"Tropical Ascendant: {tropical_ascendant:.6f}°")
#         logger.debug(f"Sidereal Ascendant: {sidereal_ascendant:.6f}° in {get_zodiac_sign(sidereal_ascendant)}")
        
#         return sidereal_ascendant
        
#     except Exception as e:
#         logger.error(f"Error calculating ascendant: {e}")
#         raise RuntimeError(f"Failed to calculate ascendant: {e}")


# def assign_planets_to_houses(planet_positions, ascendant):
#     """
#     Assign planets to houses using Whole Sign House System with enhanced accuracy.
#     """
#     try:
#         houses = {i: [] for i in range(1, 13)}  # Create empty house mapping
        
#         # Normalize ascendant to 0-360 range
#         ascendant = ascendant % 360
#         asc_sign = int(ascendant / 30) + 1  # Ascendant sign (1-12)
        
#         logger.debug(f"Ascendant sign number: {asc_sign}")
        
#         for planet, position in planet_positions.items():
#             # Normalize planet position
#             position = position % 360
#             planet_sign = int(position / 30) + 1  # Planet's sidereal sign (1-12)
            
#             # Calculate house using Whole Sign system
#             # House = (Planet Sign - Ascendant Sign + 12) % 12 + 1
#             house = ((planet_sign - asc_sign + 12) % 12) + 1
            
#             # Ensure house is in valid range
#             if house < 1 or house > 12:
#                 house = 1
#                 logger.warning(f"Invalid house calculated for {planet}, defaulting to house 1")
            
#             houses[house].append(planet)
#             logger.debug(f"{planet} in sign {planet_sign} assigned to house {house}")

#         return houses
        
#     except Exception as e:
#         logger.error(f"Error assigning planets to houses: {e}")
#         raise RuntimeError(f"Failed to assign planets to houses: {e}")


# def get_nakshatra(longitude):
#     """
#     Calculate nakshatra and pada with enhanced precision and validation.
#     """
#     try:
#         nakshatra_names = [
#             'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 
#             'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 
#             'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra', 
#             'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 
#             'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 
#             'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada', 
#             'Uttara Bhadrapada', 'Revati'
#         ]
        
#         # Normalize longitude
#         longitude = longitude % 360
        
#         # Enhanced precision calculations
#         degrees_per_nakshatra = 360.0 / 27.0  # 13.333... degrees
#         degrees_per_pada = degrees_per_nakshatra / 4.0  # 3.333... degrees

#         nakshatra_index = int(longitude / degrees_per_nakshatra)
        
#         # Validate nakshatra index
#         if nakshatra_index < 0 or nakshatra_index >= 27:
#             nakshatra_index = 0
#             logger.warning(f"Invalid nakshatra index calculated, defaulting to Ashwini")
        
#         # Calculate pada with proper rounding
#         pada_position = (longitude % degrees_per_nakshatra) / degrees_per_pada
#         pada = int(pada_position) + 1
        
#         # Ensure pada is within valid range (1-4)
#         if pada < 1 or pada > 4:
#             pada = 1
#             logger.warning(f"Invalid pada calculated, defaulting to pada 1")

#         nakshatra_name = nakshatra_names[nakshatra_index]
        
#         logger.debug(f"Longitude: {longitude:.6f}°, Nakshatra: {nakshatra_name}, Pada: {pada}")
#         return nakshatra_name, pada
        
#     except Exception as e:
#         logger.error(f"Error calculating nakshatra: {e}")
#         return "Ashwini", 1  # Default fallback


# def get_ruling_planet(moon_sign):
#     """
#     Determine the ruling planet based on the Moon sign with validation.
#     """
#     # Clean the moon_sign input
#     if isinstance(moon_sign, str):
#         moon_sign = moon_sign.strip()
    
#     ruling_planets = {
#         "Aries": "Mars",
#         "Taurus": "Venus",
#         "Gemini": "Mercury",
#         "Cancer": "Moon",
#         "Leo": "Sun",
#         "Virgo": "Mercury",
#         "Libra": "Venus",
#         "Scorpio": "Mars",
#         "Sagittarius": "Jupiter",
#         "Capricorn": "Saturn",
#         "Aquarius": "Saturn",
#         "Pisces": "Jupiter"
#     }
    
#     ruling_planet = ruling_planets.get(moon_sign, "Unknown")
    
#     if ruling_planet == "Unknown":
#         logger.warning(f"Unknown moon sign: {moon_sign}")
    
#     return ruling_planet


# def validate_birth_coordinates(lat, lon):
#     """
#     Validate geographical coordinates for accuracy.
#     """
#     if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
#         raise ValueError("Latitude and longitude must be numeric")
    
#     if not (-90 <= lat <= 90):
#         raise ValueError(f"Latitude {lat} is out of range. Must be between -90 and 90 degrees.")
    
#     if not (-180 <= lon <= 180):
#         raise ValueError(f"Longitude {lon} is out of range. Must be between -180 and 180 degrees.")
    
#     return True


# def get_planetary_dignities(planet_positions):
#     """
#     Calculate planetary dignities (Exaltation, Debilitation, Own Sign) for enhanced accuracy.
#     """
#     dignities = {}
    
#     # Exaltation degrees and signs
#     exaltations = {
#         "Sun": {"sign": "Aries", "degree": 10},
#         "Moon": {"sign": "Taurus", "degree": 3},
#         "Mars": {"sign": "Capricorn", "degree": 28},
#         "Mercury": {"sign": "Virgo", "degree": 15},
#         "Jupiter": {"sign": "Cancer", "degree": 5},
#         "Venus": {"sign": "Pisces", "degree": 27},
#         "Saturn": {"sign": "Libra", "degree": 20}
#     }
    
#     # Own signs
#     own_signs = {
#         "Sun": ["Leo"],
#         "Moon": ["Cancer"],
#         "Mars": ["Aries", "Scorpio"],
#         "Mercury": ["Gemini", "Virgo"],
#         "Jupiter": ["Sagittarius", "Pisces"],
#         "Venus": ["Taurus", "Libra"],
#         "Saturn": ["Capricorn", "Aquarius"]
#     }
    
#     for planet, longitude in planet_positions.items():
#         if planet in ["Rahu", "Ketu"]:  # Skip nodes
#             continue
            
#         sign = get_zodiac_sign(longitude)
#         degree = longitude % 30
        
#         dignity = "Neutral"
        
#         # Check for exaltation
#         if planet in exaltations:
#             exalt_info = exaltations[planet]
#             if sign == exalt_info["sign"]:
#                 dignity = "Exalted"
        
#         # Check for own sign
#         if planet in own_signs and sign in own_signs[planet]:
#             dignity = "Own Sign" if dignity == "Neutral" else dignity
        
#         # Check for debilitation (opposite of exaltation)
#         if planet in exaltations:
#             exalt_sign_index = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
#                                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"].index(exaltations[planet]["sign"])
#             debil_sign_index = (exalt_sign_index + 6) % 12
#             debil_sign = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
#                          "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"][debil_sign_index]
            
#             if sign == debil_sign:
#                 dignity = "Debilitated"
        
#         dignities[planet] = dignity
    
#     return dignities


# def cleanup_swiss_ephemeris():
#     """
#     Clean up Swiss Ephemeris resources to prevent memory leaks.
#     """
#     try:
#         swisseph.close()
#         logger.debug("Swiss Ephemeris resources cleaned up")
#     except Exception as e:
#         logger.warning(f"Error cleaning up Swiss Ephemeris: {e}")

from datetime import datetime
import pytz
import swisseph
from server.pydantic_schemas.kundali_schema import KundaliRequest
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_julian_day_from_birth_details(birth_details: KundaliRequest) -> float:
    """
    Convert birth details to UTC and calculate Julian Day with enhanced precision.
    """
    try:
        # Parse the datetime string with better error handling
        dt = datetime.strptime(f"{birth_details.birthDate} {birth_details.birthTime}", "%Y-%m-%d %H:%M")
        
        # Handle timezone more robustly
        if hasattr(birth_details, 'timezone') and birth_details.timezone:
            tz = pytz.timezone(birth_details.timezone)
        else:
            # Default to UTC if no timezone provided
            tz = pytz.UTC
            logger.warning("No timezone provided, defaulting to UTC")
        
        # Localize and convert to UTC
        dt = tz.localize(dt)
        utc_time = dt.astimezone(pytz.UTC)

        # Calculate Julian Day with full precision
        jd = swisseph.julday(
            utc_time.year,
            utc_time.month,
            utc_time.day,
            utc_time.hour + utc_time.minute / 60.0 + utc_time.second / 3600.0
        )
        
        logger.debug(f"Calculated JD: {jd} for UTC time: {utc_time}")
        return jd
        
    except Exception as e:
        logger.error(f"Error calculating Julian Day: {e}")
        raise ValueError(f"Invalid birth details format: {e}")


def get_zodiac_sign(longitude):
    """
    Determine the zodiac sign based on the sidereal longitude with validation.
    """
    # Clean zodiac signs array (removed extra spaces)
    zodiac_signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    
    # Normalize longitude to 0-360 range
    longitude = longitude % 360
    
    # Calculate sign index with validation
    sign_index = int(longitude / 30)
    
    # Ensure sign_index is within valid range
    if sign_index < 0 or sign_index > 11:
        sign_index = 0
        logger.warning(f"Invalid sign index calculated, defaulting to Aries")
    
    return zodiac_signs[sign_index]


def calculate_planet_positions(jd, lat=None, lon=None):
    """
    Calculate accurate sidereal positions for all planets with enhanced precision and error handling.
    """
    try:
        # Set sidereal mode to Lahiri (most commonly used in Vedic astrology)
        swisseph.set_sid_mode(swisseph.SIDM_LAHIRI)
        ayanamsa = swisseph.get_ayanamsa(jd)
        
        logger.debug(f"Ayanamsa for JD {jd}: {ayanamsa}")
        
        # Set geographic position if coordinates are provided (for topocentric calculations)
        if lat is not None and lon is not None:
            swisseph.set_topo(lon, lat, 0)  # longitude, latitude, altitude (0 for sea level)
            logger.debug(f"Geographic position set: lat={lat}, lon={lon}")
        
        planets = {
            "Sun": swisseph.SUN,
            "Moon": swisseph.MOON,
            "Mars": swisseph.MARS,
            "Mercury": swisseph.MERCURY,
            "Jupiter": swisseph.JUPITER,
            "Venus": swisseph.VENUS,
            "Saturn": swisseph.SATURN,
            "Rahu": swisseph.MEAN_NODE,  # Mean node for Rahu
        }
        positions = {}

        for planet_name, planet_id in planets.items():
            try:
                # Use appropriate flags based on whether coordinates are available
                if lat is not None and lon is not None:
                    flag = swisseph.FLG_SWIEPH | swisseph.FLG_SPEED | swisseph.FLG_TOPOCTR
                else:
                    flag = swisseph.FLG_SWIEPH | swisseph.FLG_SPEED
                
                result = swisseph.calc_ut(jd, planet_id, flag)
                
                # Check for calculation errors
                if len(result) > 1 and result[1] != '':
                    logger.error(f"Swiss Ephemeris error for {planet_name}: {result[1]}")
                    # Try without topocentric flag as fallback
                    if flag & swisseph.FLG_TOPOCTR:
                        logger.debug(f"Retrying {planet_name} without topocentric flag")
                        flag = swisseph.FLG_SWIEPH | swisseph.FLG_SPEED
                        result = swisseph.calc_ut(jd, planet_id, flag)
                        if len(result) > 1 and result[1] != '':
                            logger.error(f"Swiss Ephemeris error for {planet_name} (retry): {result[1]}")
                            continue
                
                
                tropical_longitude = result[0][0]
                speed = result[0][3] if len(result[0]) > 3 else 0  # Daily motion
                
                # Convert to sidereal with proper normalization
                sidereal_longitude = (tropical_longitude - ayanamsa) % 360
                
                # Store additional data for enhanced accuracy
                positions[planet_name] = {
                    'longitude': sidereal_longitude,
                    'tropical_longitude': tropical_longitude,
                    'speed': speed,
                    'is_retrograde': speed < 0,
                    'sign': get_zodiac_sign(sidereal_longitude),
                    'degree_in_sign': sidereal_longitude % 30
                }
                
                logger.debug(f"{planet_name}: {sidereal_longitude:.6f}° in {get_zodiac_sign(sidereal_longitude)}")
                
            except Exception as e:
                logger.error(f"Error calculating {planet_name}: {e}")
                # Try with basic flags as final fallback
                try:
                    flag = swisseph.FLG_SWIEPH
                    result = swisseph.calc_ut(jd, planet_id, flag)
                    tropical_longitude = result[0][0]
                    sidereal_longitude = (tropical_longitude - ayanamsa) % 360
                    
                    positions[planet_name] = {
                        'longitude': sidereal_longitude,
                        'tropical_longitude': tropical_longitude,
                        'speed': 0,
                        'is_retrograde': False,
                        'sign': get_zodiac_sign(sidereal_longitude),
                        'degree_in_sign': sidereal_longitude % 30
                    }
                    logger.debug(f"{planet_name} (fallback): {sidereal_longitude:.6f}° in {get_zodiac_sign(sidereal_longitude)}")
                except Exception as fallback_error:
                    logger.error(f"Final fallback failed for {planet_name}: {fallback_error}")
                    continue

        # Calculate Ketu as exact opposite of Rahu with enhanced precision
        if "Rahu" in positions:
            rahu_longitude = positions["Rahu"]["longitude"]
            ketu_longitude = (rahu_longitude + 180) % 360
            
            positions["Ketu"] = {
                'longitude': ketu_longitude,
                'tropical_longitude': (positions["Rahu"]["tropical_longitude"] + 180) % 360,
                'speed': -positions["Rahu"]["speed"],  # Opposite motion
                'is_retrograde': positions["Rahu"]["speed"] > 0,  # Opposite of Rahu
                'sign': get_zodiac_sign(ketu_longitude),
                'degree_in_sign': ketu_longitude % 30
            }
        
        # Ensure we have at least some planets calculated
        if not positions:
            raise RuntimeError("No planets could be calculated - check Swiss Ephemeris installation")
        
        logger.debug(f"Successfully calculated {len(positions)} celestial bodies")
        
        # Return just longitudes for backward compatibility, but store full data
        simple_positions = {}
        for planet, data in positions.items():
            simple_positions[planet] = data['longitude']
            
        return simple_positions
        
    except Exception as e:
        logger.error(f"Error in calculate_planet_positions: {e}")
        raise RuntimeError(f"Failed to calculate planet positions: {e}")


def calculate_ascendant(jd, lat, lon):
    """
    Calculate the sidereal ascendant with enhanced precision and validation.
    """
    try:
        # Validate coordinates
        if not (-90 <= lat <= 90):
            raise ValueError(f"Invalid latitude: {lat}. Must be between -90 and 90.")
        if not (-180 <= lon <= 180):
            raise ValueError(f"Invalid longitude: {lon}. Must be between -180 and 180.")
        
        # Set sidereal mode consistently
        swisseph.set_sid_mode(swisseph.SIDM_LAHIRI)
        ayanamsa = swisseph.get_ayanamsa(jd)
        
        # Calculate houses with proper house system (Placidus is default)
        houses_result = swisseph.houses(jd, lat, lon, b'P')  # 'P' for Placidus
        
        if not houses_result or len(houses_result) < 2:
            raise RuntimeError("Failed to calculate houses")
        
        houses = houses_result[0]  # House cusps
        ascmc = houses_result[1]   # Ascendant, MC, etc.
        
        # Get tropical ascendant (first element is ascendant)
        tropical_ascendant = ascmc[0]
        
        # Convert to sidereal with proper normalization
        sidereal_ascendant = (tropical_ascendant - ayanamsa) % 360
        
        logger.debug(f"Tropical Ascendant: {tropical_ascendant:.6f}°")
        logger.debug(f"Sidereal Ascendant: {sidereal_ascendant:.6f}° in {get_zodiac_sign(sidereal_ascendant)}")
        
        return sidereal_ascendant
        
    except Exception as e:
        logger.error(f"Error calculating ascendant: {e}")
        raise RuntimeError(f"Failed to calculate ascendant: {e}")


def assign_planets_to_houses(planet_positions, ascendant):
    """
    Assign planets to houses using Whole Sign House System with enhanced accuracy.
    """
    try:
        houses = {i: [] for i in range(1, 13)}  # Create empty house mapping
        
        # Normalize ascendant to 0-360 range
        ascendant = ascendant % 360
        asc_sign = int(ascendant / 30) + 1  # Ascendant sign (1-12)
        
        logger.debug(f"Ascendant sign number: {asc_sign}")
        
        for planet, position in planet_positions.items():
            # Normalize planet position
            position = position % 360
            planet_sign = int(position / 30) + 1  # Planet's sidereal sign (1-12)
            
            # Calculate house using Whole Sign system
            # House = (Planet Sign - Ascendant Sign + 12) % 12 + 1
            house = ((planet_sign - asc_sign + 12) % 12) + 1
            
            # Ensure house is in valid range
            if house < 1 or house > 12:
                house = 1
                logger.warning(f"Invalid house calculated for {planet}, defaulting to house 1")
            
            houses[house].append(planet)
            logger.debug(f"{planet} in sign {planet_sign} assigned to house {house}")

        return houses
        
    except Exception as e:
        logger.error(f"Error assigning planets to houses: {e}")
        raise RuntimeError(f"Failed to assign planets to houses: {e}")


def get_nakshatra(longitude):
    """
    Calculate nakshatra and pada with enhanced precision and validation.
    """
    try:
        nakshatra_names = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 
            'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 
            'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra', 
            'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 
            'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 
            'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada', 
            'Uttara Bhadrapada', 'Revati'
        ]
        
        # Normalize longitude
        longitude = longitude % 360
        
        # Enhanced precision calculations
        degrees_per_nakshatra = 360.0 / 27.0  # 13.333... degrees
        degrees_per_pada = degrees_per_nakshatra / 4.0  # 3.333... degrees

        nakshatra_index = int(longitude / degrees_per_nakshatra)
        
        # Validate nakshatra index
        if nakshatra_index < 0 or nakshatra_index >= 27:
            nakshatra_index = 0
            logger.warning(f"Invalid nakshatra index calculated, defaulting to Ashwini")
        
        # Calculate pada with proper rounding
        pada_position = (longitude % degrees_per_nakshatra) / degrees_per_pada
        pada = int(pada_position) + 1
        
        # Ensure pada is within valid range (1-4)
        if pada < 1 or pada > 4:
            pada = 1
            logger.warning(f"Invalid pada calculated, defaulting to pada 1")

        nakshatra_name = nakshatra_names[nakshatra_index]
        
        logger.debug(f"Longitude: {longitude:.6f}°, Nakshatra: {nakshatra_name}, Pada: {pada}")
        return nakshatra_name, pada
        
    except Exception as e:
        logger.error(f"Error calculating nakshatra: {e}")
        return "Ashwini", 1  # Default fallback


def get_ruling_planet(moon_sign):
    """
    Determine the ruling planet based on the Moon sign with validation.
    """
    # Clean the moon_sign input
    if isinstance(moon_sign, str):
        moon_sign = moon_sign.strip()
    
    ruling_planets = {
        "Aries": "Mars",
        "Taurus": "Venus",
        "Gemini": "Mercury",
        "Cancer": "Moon",
        "Leo": "Sun",
        "Virgo": "Mercury",
        "Libra": "Venus",
        "Scorpio": "Mars",
        "Sagittarius": "Jupiter",
        "Capricorn": "Saturn",
        "Aquarius": "Saturn",
        "Pisces": "Jupiter"
    }
    
    ruling_planet = ruling_planets.get(moon_sign, "Unknown")
    
    if ruling_planet == "Unknown":
        logger.warning(f"Unknown moon sign: {moon_sign}")
    
    return ruling_planet


def validate_birth_coordinates(lat, lon):
    """
    Validate geographical coordinates for accuracy.
    """
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        raise ValueError("Latitude and longitude must be numeric")
    
    if not (-90 <= lat <= 90):
        raise ValueError(f"Latitude {lat} is out of range. Must be between -90 and 90 degrees.")
    
    if not (-180 <= lon <= 180):
        raise ValueError(f"Longitude {lon} is out of range. Must be between -180 and 180 degrees.")
    
    return True


def get_planetary_dignities(planet_positions):
    """
    Calculate planetary dignities (Exaltation, Debilitation, Own Sign) for enhanced accuracy.
    """
    dignities = {}
    
    # Exaltation degrees and signs
    exaltations = {
        "Sun": {"sign": "Aries", "degree": 10},
        "Moon": {"sign": "Taurus", "degree": 3},
        "Mars": {"sign": "Capricorn", "degree": 28},
        "Mercury": {"sign": "Virgo", "degree": 15},
        "Jupiter": {"sign": "Cancer", "degree": 5},
        "Venus": {"sign": "Pisces", "degree": 27},
        "Saturn": {"sign": "Libra", "degree": 20}
    }
    
    # Own signs
    own_signs = {
        "Sun": ["Leo"],
        "Moon": ["Cancer"],
        "Mars": ["Aries", "Scorpio"],
        "Mercury": ["Gemini", "Virgo"],
        "Jupiter": ["Sagittarius", "Pisces"],
        "Venus": ["Taurus", "Libra"],
        "Saturn": ["Capricorn", "Aquarius"]
    }
    
    for planet, longitude in planet_positions.items():
        if planet in ["Rahu", "Ketu"]:  # Skip nodes
            continue
            
        sign = get_zodiac_sign(longitude)
        degree = longitude % 30
        
        dignity = "Neutral"
        
        # Check for exaltation
        if planet in exaltations:
            exalt_info = exaltations[planet]
            if sign == exalt_info["sign"]:
                dignity = "Exalted"
        
        # Check for own sign
        if planet in own_signs and sign in own_signs[planet]:
            dignity = "Own Sign" if dignity == "Neutral" else dignity
        
        # Check for debilitation (opposite of exaltation)
        if planet in exaltations:
            exalt_sign_index = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                               "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"].index(exaltations[planet]["sign"])
            debil_sign_index = (exalt_sign_index + 6) % 12
            debil_sign = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"][debil_sign_index]
            
            if sign == debil_sign:
                dignity = "Debilitated"
        
        dignities[planet] = dignity
    
    return dignities


# Wrapper function to maintain backward compatibility
def calculate_planet_positions_legacy(jd):
    """
    Legacy wrapper to maintain backward compatibility.
    """
    return calculate_planet_positions(jd)


# def cleanup_swiss_ephemeris():
#     """
#     Clean up Swiss Ephemeris resources to prevent memory leaks.
#     """
#     try:
#         swisseph.close()
#         logger.debug("Swiss Ephemeris resources cleaned up")
#     except Exception as e:
#         logger.warning(f"Error cleaning up Swiss Ephemeris: {e}")

def get_julian_day_from_date(date_obj: datetime) -> float:
    """
    Convert a datetime object to Julian Day.

    Args:
        date_obj: datetime object (assumed to be in UTC)

    Returns:
        Julian Day number as float
    """
    try:
        jd = swisseph.julday(
            date_obj.year,
            date_obj.month,
            date_obj.day,
            date_obj.hour + date_obj.minute / 60.0 + date_obj.second / 3600.0
        )
        return jd
    except Exception as e:
        logger.error(f"Error calculating Julian Day from datetime: {e}")
        raise ValueError(f"Invalid datetime object: {e}")
