"""
Transit API Endpoints
Provides endpoints for calculating and analyzing planetary transits.

Author: Astrology Backend
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from typing import Optional
import logging

from server.pydantic_schemas.kundali_schema import KundaliRequest, KundaliResponse
from server.services.transit_calculator import TransitCalculator
from server.rule_engine.rules.transit_rules import TransitRules
from server.pydantic_schemas.api_response import APIResponse, success_response, error_response
from server.services.logic import generate_kundali_logic

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/transits",
    tags=["transits"]
)


@router.post("/calculate")
async def calculate_transits(
    birth_details: KundaliRequest,
    transit_date: Optional[str] = None
) -> APIResponse:
    """
    Calculate current planetary transits.

    Args:
        birth_details: Birth chart details
        transit_date: Optional date to calculate transits for (format: YYYY-MM-DD)

    Returns:
        APIResponse with transit information
    """
    try:
        logger.info("Calculating transits")

        # Generate birth chart
        birth_chart = await generate_kundali_logic(birth_details)

        # Convert to dict for transit calculator
        birth_chart_dict = {
            'planets': {
                k: {
                    'longitude': v.longitude,
                    'sign': v.sign,
                    'nakshatra': v.nakshatra,
                    'house': v.house
                } for k, v in birth_chart.planets.items()
            },
            'houses': {
                k: {
                    'sign': v.sign,
                    'planets': v.planets
                } for k, v in birth_chart.houses.items()
            }
        }

        # Parse transit date if provided
        if transit_date:
            try:
                t_date = datetime.strptime(transit_date, "%Y-%m-%d")
            except ValueError:
                return error_response(
                    message="Invalid transit_date format. Use YYYY-MM-DD",
                    status_code=422
                )
        else:
            t_date = None

        # Calculate transits
        transit_calc = TransitCalculator(birth_chart_dict, t_date)
        transits = transit_calc.calculate_current_transits()

        # Add interpretations
        for planet, transit_info in transits.items():
            # Determine transit sign to use
            current_sign = transit_info.get('current_sign', '')

            # Generate interpretations based on planet
            if planet == 'Sun':
                interpretations = TransitRules.interpret_sun_transit(transit_info)
            elif planet == 'Moon':
                interpretations = TransitRules.interpret_moon_transit(transit_info)
            elif planet == 'Mars':
                interpretations = TransitRules.interpret_mars_transit(transit_info)
            elif planet == 'Mercury':
                interpretations = TransitRules.interpret_mercury_transit(transit_info)
            elif planet == 'Venus':
                interpretations = TransitRules.interpret_venus_transit(transit_info)
            elif planet == 'Jupiter':
                interpretations = TransitRules.interpret_jupiter_transit(transit_info)
            elif planet == 'Saturn':
                interpretations = TransitRules.interpret_saturn_transit(transit_info)
            elif planet == 'Rahu':
                interpretations = TransitRules.interpret_rahu_transit(transit_info)
            elif planet == 'Ketu':
                interpretations = TransitRules.interpret_ketu_transit(transit_info)
            else:
                interpretations = []

            transit_info['interpretations'] = interpretations
            transit_info['remedies'] = TransitRules.get_transit_remedies(
                planet, current_sign
            )

        return success_response(
            data={
                'transit_date': (t_date or datetime.now()).strftime('%Y-%m-%d'),
                'transits': transits,
                'important_transits': transit_calc.get_important_transits(),
                'predictions': transit_calc.get_transit_predictions()
            },
            message="Transits calculated successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating transits: {str(e)}")
        return error_response(
            message="Error calculating transits",
            detail=str(e),
            status_code=500
        )


@router.post("/upcoming")
async def get_upcoming_transits(
    birth_details: KundaliRequest,
    days: int = 365
) -> APIResponse:
    """
    Get upcoming important transits.

    Args:
        birth_details: Birth chart details
        days: Number of days to look ahead (default: 365)

    Returns:
        APIResponse with upcoming transit information
    """
    try:
        if days < 1 or days > 3650:
            return error_response(
                message="Days must be between 1 and 3650",
                status_code=422
            )

        logger.info(f"Getting upcoming transits for {days} days")

        # Generate birth chart
        birth_chart = await generate_kundali_logic(birth_details)

        # Convert to dict for transit calculator
        birth_chart_dict = {
            'planets': {
                k: {
                    'longitude': v.longitude,
                    'sign': v.sign,
                    'nakshatra': v.nakshatra,
                    'house': v.house
                } for k, v in birth_chart.planets.items()
            },
            'houses': {
                k: {
                    'sign': v.sign,
                    'planets': v.planets
                } for k, v in birth_chart.houses.items()
            }
        }

        # Calculate upcoming transits
        transit_calc = TransitCalculator(birth_chart_dict)
        upcoming = transit_calc.get_upcoming_important_transits(days)

        return success_response(
            data={
                'period_days': days,
                'period_until': (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d'),
                'upcoming_transits': upcoming,
                'total_upcoming': len(upcoming)
            },
            message="Upcoming transits retrieved successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting upcoming transits: {str(e)}")
        return error_response(
            message="Error getting upcoming transits",
            detail=str(e),
            status_code=500
        )


@router.post("/dasha-transit-analysis")
async def analyze_dasha_transit_conjunction(
    birth_details: KundaliRequest,
    current_dasha: str
) -> APIResponse:
    """
    Analyze interaction between current dasha and transits.

    Args:
        birth_details: Birth chart details
        current_dasha: Current dasha planet

    Returns:
        APIResponse with dasha-transit analysis
    """
    try:
        logger.info(f"Analyzing {current_dasha} dasha with transits")

        if current_dasha not in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
            return error_response(
                message="Invalid dasha planet",
                status_code=422
            )

        # Generate birth chart
        birth_chart = await generate_kundali_logic(birth_details)

        # Convert to dict for transit calculator
        birth_chart_dict = {
            'planets': {
                k: {
                    'longitude': v.longitude,
                    'sign': v.sign,
                    'nakshatra': v.nakshatra,
                    'house': v.house
                } for k, v in birth_chart.planets.items()
            },
            'houses': {
                k: {
                    'sign': v.sign,
                    'planets': v.planets
                } for k, v in birth_chart.houses.items()
            }
        }

        # Calculate transits and dasha conjunction
        transit_calc = TransitCalculator(birth_chart_dict)
        conjunction_analysis = transit_calc.analyze_transit_dasha_conjunction(current_dasha)

        # Get current transits for context
        transits = transit_calc.calculate_current_transits()
        current_dasha_transit = transits.get(current_dasha, {})

        return success_response(
            data={
                'dasha': current_dasha,
                'current_transit_sign': current_dasha_transit.get('current_sign', 'Unknown'),
                'analysis': conjunction_analysis,
                'significance': f"Strong {current_dasha} influence when dasha and transit align",
                'impact': 'High - Results manifest more quickly'
            },
            message=f"{current_dasha} dasha-transit analysis completed"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing dasha-transit: {str(e)}")
        return error_response(
            message="Error analyzing dasha-transit conjunction",
            detail=str(e),
            status_code=500
        )
