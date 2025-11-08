from datetime import datetime
import logging
from fastapi import HTTPException

from server.ml.feature_generator import KundaliMLDataGenerator
from server.pydantic_schemas.kundali_schema import (
    KundaliRequest,
    KundaliResponse,
    Ascendant,
    PlanetDetails,
    HouseDetails,
    DashaInfo,
    ShaBalaInfo,
    DivisionalChartsInfo,
)

from server.utils.astro_utils import (
    calculate_ascendant,
    get_nakshatra,
    calculate_planet_positions,
    assign_planets_to_houses,
    get_zodiac_sign,
    get_ruling_planet,
    get_julian_day_from_birth_details,
)

from server.services.dasha_calculator import DashaCalculator
from server.rule_engine.rules.dasha_rules import DashaRules
from server.utils.strength_calculator import StrengthCalculator
from server.utils.varga_calculator import VargaCalculator
from server.utils.shad_bala_enhancer import EnhancedShadBalaCalculator
from server.rule_engine.rules.strength_rules import StrengthRules
from server.rule_engine.rules.varga_rules import VargaRules

logger = logging.getLogger(__name__)

# Enhanced service function
async def generate_kundali_logic(birth_details: KundaliRequest) -> KundaliResponse:
    ml_generator = KundaliMLDataGenerator()
    
    try:
        logger.info(f"Generating Kundali for: {birth_details}")

        # Julian day
        jd = get_julian_day_from_birth_details(birth_details)

        # Ascendant
        asc_deg = calculate_ascendant(jd, birth_details.latitude, birth_details.longitude)
        asc_nakshatra, asc_pada = get_nakshatra(asc_deg)
        asc_sign = get_zodiac_sign(asc_deg)

        # Normalize asc_deg to 0–359.999
        asc_deg_normalized = asc_deg % 360

        ascendant = Ascendant(
            index=int(asc_deg_normalized / 30) + 1,
            longitude=asc_deg_normalized,
            sign=asc_sign,
            nakshatra=asc_nakshatra,
            pada=asc_pada,
        )

        # Planet positions with coordinates for enhanced accuracy
        planet_positions = calculate_planet_positions(jd)
        house_assignments = assign_planets_to_houses(planet_positions, asc_deg)
        planet_nakshatras = {p: get_nakshatra(pos) for p, pos in planet_positions.items()}

        # Planets
        planets = {
            planet: PlanetDetails(
                longitude=pos,
                sign=get_zodiac_sign(pos),
                nakshatra=planet_nakshatras[planet][0],
                pada=planet_nakshatras[planet][1],
                house=next(h for h, plist in house_assignments.items() if planet in plist),
            )
            for planet, pos in planet_positions.items()
        }

        # Houses
        houses = {
            house: HouseDetails(
                # sign=ml_generator.get_house_sign(house, asc_deg_normalized),
                sign = (int(asc_deg / 30) + house - 1) % 12 + 1,
                planets=plist,
            )
            for house, plist in house_assignments.items()
        }

        # Moon and Ruling Planet
        moon_sign = get_zodiac_sign(planet_positions["Moon"])
        ruling_planet = get_ruling_planet(moon_sign)

        # Generate comprehensive ML features
        ml_features = ml_generator.generate_comprehensive_features(
            birth_details, planet_positions, house_assignments, asc_deg_normalized, jd
        )

        # Calculate Dasha (Vimshottari Dasha System)
        try:
            dasha_calculator = DashaCalculator(
                birth_date=datetime.strptime(birth_details.birthDate, "%Y-%m-%d"),
                birth_time=birth_details.birthTime,
                moon_longitude=planet_positions["Moon"]
            )

            dasha_info_dict = dasha_calculator.calculate_complete_dasha_info()

            # Add interpretations and remedies
            if dasha_info_dict.get('current_maha_dasha'):
                dasha_interpretations = DashaRules.interpret_current_dasha(dasha_info_dict)
                dasha_predictions = DashaRules.predict_dasha_events(dasha_info_dict, planets)
                dasha_remedies = DashaRules.get_dasha_remedies(dasha_info_dict['current_maha_dasha'])

                dasha_info_dict['dasha_interpretations'] = dasha_interpretations
                dasha_info_dict['dasha_predictions'] = dasha_predictions
                dasha_info_dict['dasha_remedies'] = dasha_remedies

            dasha_info = DashaInfo(**dasha_info_dict)
        except Exception as e:
            logger.warning(f"Could not calculate Dasha information: {str(e)}")
            dasha_info = None

        # Calculate Shad Bala (Six Strength Measures) with enhancements
        shad_bala_info = None
        try:
            strength_calculator = StrengthCalculator(
                planets_info=planet_positions,
                ascendant_sign=ascendant.index,
                birth_date=datetime.strptime(birth_details.birthDate, "%Y-%m-%d")
            )
            shad_bala_data = strength_calculator.calculate_all_strengths()

            # Enhance with yoga and house lord strengths
            try:
                enhancer = EnhancedShadBalaCalculator(
                    ascendant_degree=asc_deg_normalized,
                    planet_positions=planet_positions,
                    house_assignments=house_assignments
                )

                # Add house lord strengths
                house_lord_strengths = enhancer.calculate_house_lord_strengths(
                    shad_bala_data.get('planetary_strengths', {})
                )

                # Add yoga analysis
                yogas = enhancer.calculate_yogas(
                    shad_bala_data.get('planetary_strengths', {})
                )

                # Add aspect strengths
                aspect_strengths = enhancer.calculate_aspect_strengths()

                shad_bala_data['house_lord_strengths'] = house_lord_strengths
                shad_bala_data['yogas'] = yogas
                shad_bala_data['aspect_strengths'] = aspect_strengths

                logger.info("Enhanced Shad Bala with house lord strengths, yogas, and aspects")
            except Exception as e:
                logger.warning(f"Could not enhance Shad Bala: {str(e)}")

            shad_bala_info = ShaBalaInfo(**shad_bala_data)
            logger.info("Successfully calculated Shad Bala (Planetary Strengths)")
        except Exception as e:
            logger.warning(f"Could not calculate Shad Bala: {str(e)}")
            shad_bala_info = None

        # Calculate Divisional Charts (Vargas)
        divisional_charts_info = None
        try:
            varga_calculator = VargaCalculator(
                planets_info=planet_positions,
                ascendant_degree=asc_deg_normalized
            )
            vargas_data = varga_calculator.calculate_all_vargas()

            # Get alignment analysis
            alignment_analysis = varga_calculator.compare_d1_d9_alignment()
            vargas_data['alignment_analysis'] = alignment_analysis

            divisional_charts_info = DivisionalChartsInfo(
                D1_Rasi=vargas_data.get('D1_Rasi'),
                D2_Hora=vargas_data.get('D2_Hora'),
                D7_Saptamsha=vargas_data.get('D7_Saptamsha'),
                D9_Navamsha=vargas_data.get('D9_Navamsha'),
                alignment_analysis=alignment_analysis
            )
            logger.info("Successfully calculated Divisional Charts (Vargas)")
        except Exception as e:
            logger.warning(f"Could not calculate Divisional Charts: {str(e)}")
            divisional_charts_info = None

        kundali_response = KundaliResponse(
            ascendant=ascendant,
            planets=planets,
            houses=houses,
            zodiac_sign=moon_sign,
            ruling_planet=ruling_planet,
            dasha=dasha_info,
            shad_bala=shad_bala_info,
            divisional_charts=divisional_charts_info,
            generated_at=datetime.now()
        )

        # Add ML features to response for training data
        kundali_response.ml_features = ml_features
        kundali_response.training_data = {
            # "birth_details": birth_details.dict(),
            "calculated_features": ml_features,
            "timestamp": datetime.now().isoformat(),
            "data_version": "1.0"
        }

        logger.info(f"Successfully generated Kundali with Dasha, Shad Bala, Divisional Charts and {len(ml_features)} ML features")

        return kundali_response

    except Exception as e:
        logger.error(f"Error generating Kundali: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during Kundali generation")
    # finally:
        # Clean up resources
        # cleanup_swiss_ephemeris()







