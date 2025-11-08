from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

# Request Schemas
class KundaliRequest(BaseModel):
    birthDate: str # Format: YYYY-MM-DD
    birthTime: str # Format: HH:MM
    latitude: float
    longitude: float
    timezone: str # e.g., "UTC", "America/New_York"


# Response Schemas
class Ascendant(BaseModel):
    index: int
    longitude: float
    sign: str
    nakshatra: str
    pada: int

class PlanetDetails(BaseModel):
    longitude: float
    sign: str
    nakshatra: str
    pada: int
    house: int

class HouseDetails(BaseModel):
    sign: int
    planets: List[str]

# Dasha Schemas
class DashaPeriod(BaseModel):
    planet: str
    duration: int
    start_year: int
    end_year: int
    is_current: bool
    remaining_years: Optional[float] = None

class AntarDasha(BaseModel):
    planet: str
    duration_years: float
    duration_months: int
    duration_days: int
    is_current: bool

class DashaInfo(BaseModel):
    moon_nakshatra: str
    moon_nakshatra_number: int
    current_maha_dasha: str
    maha_dasha_start_date: str
    maha_dasha_end_date: str
    maha_dasha_duration_years: int
    remaining_maha_dasha_years: float
    remaining_maha_dasha_months: float
    completed_maha_dasha_years: float
    current_antar_dasha: Optional[str] = None
    current_antar_dasha_duration_days: Optional[int] = None
    maha_dasha_timeline: List[DashaPeriod]
    antar_dasha_timeline: List[AntarDasha]
    next_dasha_lord: Optional[str] = None
    dasha_interpretations: Optional[List[str]] = None
    dasha_predictions: Optional[List[str]] = None
    dasha_remedies: Optional[List[str]] = None

# Planetary Strength Schemas
class PlanetaryStrengthBreakdown(BaseModel):
    sthana_bala: float = Field(..., description="Positional strength (0-15)")
    dig_bala: float = Field(..., description="Directional strength (0-15)")
    kala_bala: float = Field(..., description="Temporal strength (0-15)")
    chesta_bala: float = Field(..., description="Motion strength (0-15)")
    naisargika_bala: float = Field(..., description="Natural strength (0-15)")
    drishti_bala: float = Field(..., description="Aspect strength (0-15)")

class PlanetaryStrength(BaseModel):
    planet: str = Field(..., description="Planet name")
    total_strength: float = Field(..., description="Total strength (0-60)")
    strength_percentage: float = Field(..., description="Strength as percentage (0-100)")
    strength_status: str = Field(..., description="Status: Very Strong, Strong, Moderate, Weak, Very Weak")
    breakdown: Optional[Union[PlanetaryStrengthBreakdown, Dict[str, Any]]] = Field(None, description="Breakdown of strengths")
    is_strong: bool = Field(..., description="Is planet strong (>70%)")
    capacity: str = Field(..., description="Planet's capacity to give results")

class YogaAnalysis(BaseModel):
    yoga_name: str = Field(..., description="Name of the yoga")
    house: Optional[int] = None
    planets: List[str] = Field(..., description="Planets involved")
    strength: float = Field(..., description="Strength of yoga (0-100)")
    benefic: bool = Field(..., description="Is yoga benefic")

class HouseLordStrength(BaseModel):
    house: int = Field(..., description="House number")
    lord: str = Field(..., description="House lord planet")
    strength_percentage: float = Field(..., description="Lord's strength (0-100)")
    status: str = Field(..., description="Strong/Moderate/Weak")

class YogaInfo(BaseModel):
    total_yoga_count: int = Field(..., description="Total yogas in chart")
    benefic_yoga_count: int = Field(..., description="Benefic yogas")
    malefic_yoga_count: int = Field(..., description="Malefic yogas")
    neutral_yoga_count: int = Field(..., description="Neutral yogas")
    yogas: Optional[List[YogaAnalysis]] = None

class ShaBalaInfo(BaseModel):
    planetary_strengths: Optional[Dict[str, Any]] = Field(None, description="Planetary strength data")
    chart_strength_assessment: Optional[Dict[str, Any]] = None
    house_lord_strengths: Optional[Dict[int, HouseLordStrength]] = None
    yogas: Optional[YogaInfo] = None
    aspect_strengths: Optional[Dict[int, float]] = None

# Divisional Charts Schemas
class VargaChart(BaseModel):
    name: str = Field(..., description="Chart name (D1, D2, D7, D9)")
    description: str = Field(..., description="Chart description")
    significance: str = Field(..., description="What this chart shows")
    planets: Dict[str, Any] = Field(..., description="Planet positions in this varga")
    ascendant: Optional[str] = Field(None, description="Ascendant in varga")

class DivisionalChartsInfo(BaseModel):
    D1_Rasi: Optional[VargaChart] = None
    D2_Hora: Optional[VargaChart] = None
    D7_Saptamsha: Optional[VargaChart] = None
    D9_Navamsha: Optional[VargaChart] = None
    alignment_analysis: Optional[Dict[str, Any]] = None

# Main Kundali Response
class KundaliResponse(BaseModel):
    ascendant: Ascendant
    planets: Dict[str, PlanetDetails]
    houses: Dict[int, HouseDetails]
    zodiac_sign: str
    ruling_planet: str
    dasha: Optional[DashaInfo] = None  # Dasha System
    shad_bala: Optional[ShaBalaInfo] = None  # NEW: Planetary Strengths
    divisional_charts: Optional[DivisionalChartsInfo] = None  # NEW: Vargas
    training_data: Optional[Dict[str, float]] = None
    ml_features: Optional[Dict[str, float]] = None
    generated_at: Optional[datetime] = None
  
class AscendantWestern(BaseModel):
    index: int
    longitude: float
    sign: str
   
class PlanetDetailsWestern(BaseModel):
    longitude: float
    sign: str
    house: int

class KundaliResponseWestern(BaseModel):
    ascendant: AscendantWestern
    planets: Dict[str, PlanetDetailsWestern]
   