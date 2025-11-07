# ML Dataset Preparation Plan for Complete Kundali Analysis
**Comprehensive Guide for Training-Ready Dataset**

**Date:** November 8, 2025
**Purpose:** Prepare dataset for ML model training on Kundali astrology analysis
**Status:** Planning Phase

---

## 🎯 PART 1: DATASET STRUCTURE & SCHEMA

### 1.1 Core Dataset Format

```python
# Single Kundali Record (Training Data)
{
  # Birth Information
  "birth_details": {
    "date": "YYYY-MM-DD",           # Birth date
    "time": "HH:MM",                # Birth time
    "latitude": float,              # Birth latitude (-90 to 90)
    "longitude": float,             # Birth longitude (-180 to 180)
    "timezone": str,                # Timezone (e.g., "Asia/Kolkata")
    "location": str                 # City/Location name
  },

  # Calculated Birth Chart
  "birth_chart": {
    "ascendant_degree": float,      # 0-360
    "ascendant_sign": str,          # Zodiac sign
    "ascendant_nakshatra": str,     # Nakshatra name
    "moon_sign": str,               # Moon's zodiac sign
    "sun_sign": str,                # Sun's zodiac sign
    "ruling_planet": str            # Moon sign ruler
  },

  # Planet Positions (9 Planets)
  "planets": {
    "planet_name": {
      "longitude": float,           # 0-360 degrees
      "sign": str,                  # Zodiac sign
      "house": int,                 # 1-12
      "nakshatra": str,             # Nakshatra
      "retrograde": bool,           # Retrograde status
      "speed": float,               # Daily speed in degrees
      "is_exalted": bool,           # Exalted position
      "is_debilitated": bool,       # Debilitated position
      "is_own_sign": bool           # Own sign placement
    }
    # Repeat for Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
  },

  # Houses Analysis (12 Houses)
  "houses": {
    "house_number": {
      "sign": str,                  # Sign in house
      "lord": str,                  # House lord planet
      "lord_strength": float,       # 0-100 percentage
      "planets_count": int,         # Number of planets
      "planets": [str],             # List of planets in house
      "strength": str               # Strong/Moderate/Weak
    }
    # Repeat for houses 1-12
  },

  # Dasha System (Vimshottari)
  "dasha": {
    "moon_nakshatra": str,
    "current_maha_dasha": str,
    "current_maha_dasha_remaining_years": float,
    "current_antar_dasha": str,
    "dasha_start_year": int,
    "dasha_end_year": int,
    "dasha_timeline": [
      {
        "planet": str,
        "duration": int,            # In years
        "start_year": int,
        "end_year": int
      }
    ]
  },

  # Planetary Strengths (Shad Bala)
  "shad_bala": {
    "planet_name": {
      "sthana_bala": float,         # 0-15
      "dig_bala": float,            # 0-15
      "kala_bala": float,           # 0-15
      "chesta_bala": float,         # 0-15
      "naisargika_bala": float,     # 0-15
      "drishti_bala": float,        # 0-15
      "total_strength": float,      # 0-60
      "strength_percentage": float, # 0-100
      "strength_status": str        # Very Strong/Strong/Moderate/Weak/Very Weak
    }
    # For all 9 planets
  },

  # Divisional Charts
  "divisional_charts": {
    "D1": {                         # Rasi Chart (Birth Chart)
      "planets": {...},
      "ascendant_sign": str
    },
    "D2": {                         # Hora (Wealth)
      "planets": {...},
      "ascendant_sign": str,
      "wealth_significance": float
    },
    "D7": {                         # Saptamsha (Children)
      "planets": {...},
      "ascendant_sign": str,
      "fertility_score": float
    },
    "D9": {                         # Navamsha (Marriage)
      "planets": {...},
      "ascendant_sign": str,
      "marriage_significance": float,
      "d1_d9_alignment_score": float  # 0-100
    }
  },

  # Aspects & Conjunctions
  "aspects": {
    "conjunctions": [
      {
        "planet1": str,
        "planet2": str,
        "orb": float,               # Degrees apart
        "strength": str             # Strong/Moderate
      }
    ],
    "oppositions": [...],           # 180 degree aspects
    "squares": [...],               # 90 degree aspects
    "trines": [...],                # 120 degree aspects
    "total_benefic_aspects": int,
    "total_malefic_aspects": int
  },

  # Yogas (Auspicious Combinations)
  "yogas": {
    "benefic_yogas": [
      {
        "yoga_name": str,           # Raj Yoga, Gaj Kesari, etc
        "type": str,
        "strength_score": float,    # 0-100
        "significance": str
      }
    ],
    "malefic_yogas": [...],
    "total_yoga_count": int,
    "yoga_strength_average": float
  },

  # Transits (Current/On Specific Date)
  "transits": {
    "transit_date": "YYYY-MM-DD",
    "planet_name": {
      "current_sign": str,
      "current_degree": float,
      "birth_sign": str,
      "aspects_to_birth": [
        {
          "birth_planet": str,
          "aspect": str,            # Conjunction, Square, Trine, Opposition
          "orb": float,
          "strength": str
        }
      ],
      "transit_quality": str        # Benefic/Malefic/Neutral
    }
    # For all planets
  },

  # Retrograde Status
  "retrograde_planets": {
    "planet_name": {
      "retrograde": bool,
      "karmic_lesson": str,
      "remedies": [str]
    }
    # For planets with retrograde status
  },

  # Derived ML Features (Numerical Aggregates)
  "ml_features": {
    # Planet Position Features
    "sun_degree": float,
    "moon_degree": float,
    "mars_degree": float,
    "mercury_degree": float,
    "jupiter_degree": float,
    "venus_degree": float,
    "saturn_degree": float,
    "rahu_degree": float,
    "ketu_degree": float,

    # Sign Features (Encoded)
    "sun_sign_encoded": int,        # 0-11
    "moon_sign_encoded": int,
    "ascendant_sign_encoded": int,
    # ... all planets

    # House Features
    "planets_in_house_1": int,
    "planets_in_house_2": int,
    # ... all houses

    # Strength Features
    "avg_planet_strength": float,   # 0-100
    "sun_strength": float,
    "moon_strength": float,
    # ... all planets

    # Aspect Features
    "total_aspects": int,
    "benefic_aspects_count": int,
    "malefic_aspects_count": int,
    "aspect_ratio": float,

    # Yoga Features
    "yoga_count": int,
    "benefic_yoga_count": int,
    "malefic_yoga_count": int,
    "avg_yoga_strength": float,

    # Dasha Features
    "dasha_planet_strength": float,
    "years_in_dasha": int,

    # Varga Features (Alignment Scores)
    "d1_d2_alignment": float,
    "d1_d7_alignment": float,
    "d1_d9_alignment": float,
    "avg_varga_alignment": float,

    # Retrograde Features
    "retrograde_planet_count": int,
    "retrograde_strength_planets": int,
    "retrograde_weak_planets": int
  },

  # Target Variables (What we're predicting)
  "targets": {
    # Life Area Predictions
    "career_potential": float,        # 0-100
    "wealth_potential": float,        # 0-100
    "marriage_happiness": float,      # 0-100
    "children_prospects": float,      # 0-100
    "health_status": float,           # 0-100
    "spiritual_inclination": float,   # 0-100

    # Life Events Prediction
    "marriage_year": int,             # Age at marriage
    "children_count": int,            # Expected children
    "career_switches": int,           # Career change frequency
    "health_issues_probability": float, # 0-100

    # Overall Assessment
    "chart_strength": float,          # 0-100
    "life_ease_score": float,         # 0-100
    "success_probability": float,     # 0-100

    # Compatibility Indicators
    "relationship_compatibility_potential": float,
    "financial_success_likelihood": float
  },

  # Metadata
  "metadata": {
    "gender": str,                    # Male/Female/Other
    "current_age": int,               # Age when chart generated
    "country": str,                   # Birth country
    "data_quality_score": float,      # 0-100
    "generated_timestamp": "ISO-8601",
    "is_synthetic": bool              # True if generated, False if real
  }
}
```

---

## 🎯 PART 2: DATA COLLECTION STRATEGY

### 2.1 Real Data Collection (Phase 1)

**Sources:**
1. **User Database** - Existing users with birth data
2. **Public Records** - Historical astrology databases
3. **Astrology Forums** - Community data (with consent)
4. **Astrological Websites** - Public Kundali data
5. **Research Institutions** - Academic astrology studies

**Data Collection Process:**
```
1. Gather 50-100 real birth charts
   ├── Record complete birth data
   ├── Calculate all astrological features
   ├── Manually collect life outcomes
   └── Validate accuracy

2. Build Real Data Corpus
   ├── Birth data: 50-100 records
   ├── Calculation results: 100%
   ├── Life events data: 50-100 records
   └── Outcomes verified by astrologers
```

**Minimum Real Data Target:** 100-500 verified records

### 2.2 Synthetic Data Generation (Phase 2)

**Why Synthetic Data?**
- Real Kundali data is limited and private
- Need thousands of records for effective ML
- Can generate diverse scenarios
- Maintain privacy and ethical standards
- Cost-effective data expansion

---

## 🎯 PART 3: SYNTHETIC DATA GENERATION STRATEGY

### 3.1 Architecture for Synthetic Data Generation

```
┌─────────────────────────────────────────────────┐
│         Synthetic Data Generator                 │
│                                                   │
│  ┌──────────────────────────────────────────┐   │
│  │  1. Birth Parameter Generator            │   │
│  │  - Random valid dates (1950-2020)        │   │
│  │  - Random times (00:00-23:59)            │   │
│  │  - Random locations (major cities)       │   │
│  │  - Valid timezone assignment             │   │
│  └──────────────────────────────────────────┘   │
│                  ↓                                │
│  ┌──────────────────────────────────────────┐   │
│  │  2. Call Backend API                     │   │
│  │  POST /kundali/generate_kundali          │   │
│  │  - Input: birth_details                  │   │
│  │  - Output: Complete Kundali              │   │
│  └──────────────────────────────────────────┘   │
│                  ↓                                │
│  ┌──────────────────────────────────────────┐   │
│  │  3. Feature Extraction                   │   │
│  │  - Parse API response                    │   │
│  │  - Extract numerical features            │   │
│  │  - Normalize values                      │   │
│  │  - Handle missing data                   │   │
│  └──────────────────────────────────────────┘   │
│                  ↓                                │
│  ┌──────────────────────────────────────────┐   │
│  │  4. Target Label Generation              │   │
│  │  - Rule-based predictions (Astrology)    │   │
│  │  - Probabilistic assignments             │   │
│  │  - Domain knowledge integration          │   │
│  └──────────────────────────────────────────┘   │
│                  ↓                                │
│  ┌──────────────────────────────────────────┐   │
│  │  5. Data Validation & Quality Check      │   │
│  │  - Check for duplicates                  │   │
│  │  - Validate ranges                       │   │
│  │  - Ensure diversity                      │   │
│  └──────────────────────────────────────────┘   │
│                  ↓                                │
│  ┌──────────────────────────────────────────┐   │
│  │  6. Storage in CSV/Database              │   │
│  │  - Save to CSV file                      │   │
│  │  - Upload to Firebase                    │   │
│  │  - Version control                       │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### 3.2 Synthetic Data Generation Algorithm

**Algorithm Step-by-Step:**

```python
def generate_synthetic_kundali_dataset(target_records=10000):
    """
    Generate synthetic Kundali records using the backend API

    Process:
    1. Generate random but valid birth parameters
    2. Call backend API to calculate Kundali
    3. Extract features from API response
    4. Generate target labels based on Vedic astrology rules
    5. Validate and store records
    6. Create training CSV
    """

    dataset = []

    for i in range(target_records):
        # Step 1: Generate Random Birth Parameters
        birth_params = {
            'birthDate': generate_random_date(),        # 1950-2020
            'birthTime': generate_random_time(),        # Valid time
            'latitude': generate_random_latitude(),     # -90 to 90
            'longitude': generate_random_longitude(),   # -180 to 180
            'timezone': get_timezone_for_location()     # Appropriate TZ
        }

        # Step 2: Call Backend API
        try:
            response = requests.post(
                'http://localhost:8000/kundali/generate_kundali',
                json=birth_params
            )
            kundali = response.json()['data']  # Extract Kundali data

            # Step 3: Extract Features
            features = {
                # Planet degrees (0-360)
                'sun_degree': kundali['planets']['Sun']['longitude'],
                'moon_degree': kundali['planets']['Moon']['longitude'],
                'mars_degree': kundali['planets']['Mars']['longitude'],
                # ... extract all planets

                # House information
                'planets_in_1st_house': len(kundali['houses'][1]['planets']),
                'planets_in_7th_house': len(kundali['houses'][7]['planets']),
                # ... all houses

                # Strength values
                'sun_strength': kundali['shad_bala']['planetary_strengths']['Sun']['strength_percentage'],
                'moon_strength': kundali['shad_bala']['planetary_strengths']['Moon']['strength_percentage'],
                # ... all planets

                # Dasha information
                'current_dasha': kundali['dasha']['current_maha_dasha'],
                'years_in_dasha': calculate_years_in_dasha(),

                # Divisional charts
                'd1_d9_alignment': kundali['divisional_charts']['alignment_analysis']['alignment_percentage'],

                # Varga/Yoga counts
                'yoga_count': len(kundali['yogas']['benefic_yogas']) + len(kundali['yogas']['malefic_yogas']),
                'benefic_yoga_count': len(kundali['yogas']['benefic_yogas']),

                # Retrograde
                'retrograde_planet_count': count_retrograde_planets(kundali),
            }

            # Step 4: Generate Target Labels (Rule-Based)
            targets = {
                'career_potential': calculate_career_potential(kundali),      # 0-100
                'wealth_potential': calculate_wealth_potential(kundali),      # 0-100
                'marriage_happiness': calculate_marriage_happiness(kundali),  # 0-100
                'children_prospects': calculate_children_prospects(kundali),  # 0-100
                'health_status': calculate_health_status(kundali),            # 0-100
                'spiritual_inclination': calculate_spiritual_inclination(kundali),
                'chart_strength': calculate_chart_strength(kundali),          # 0-100
                'life_ease_score': calculate_life_ease(kundali),              # 0-100
            }

            # Step 5: Combine and Validate
            record = {
                'id': i,
                'is_synthetic': True,
                'metadata': {...},
                **features,
                **targets
            }

            dataset.append(record)

            # Log progress
            if (i + 1) % 100 == 0:
                print(f"Generated {i+1}/{target_records} records")

        except Exception as e:
            print(f"Error generating record {i}: {str(e)}")
            continue

    return dataset
```

### 3.3 Target Label Generation Rules

**Using Vedic Astrology Rules to Create Labels:**

```python
def calculate_career_potential(kundali) -> float:
    """
    Calculate career potential based on Vedic astrology

    Factors:
    - 10th house strength (career house)
    - Saturn strength (career planet)
    - Dasha planet (timing)
    """
    score = 0

    # 10th house planets
    house_10_planets = kundali['houses'][10]['planets']
    planets_in_10 = len(house_10_planets)
    score += planets_in_10 * 10  # Each planet = +10

    # 10th house lord strength
    lord_strength = kundali['houses'][10]['lord_strength']
    score += (lord_strength / 100) * 30  # Max +30

    # Saturn strength (career planet)
    saturn_strength = kundali['shad_bala']['planetary_strengths']['Saturn']['strength_percentage']
    score += (saturn_strength / 100) * 20  # Max +20

    # Sun strength (authority)
    sun_strength = kundali['shad_bala']['planetary_strengths']['Sun']['strength_percentage']
    score += (sun_strength / 100) * 20  # Max +20

    # Raj Yoga presence
    if 'Raj Yoga' in [y['yoga_name'] for y in kundali['yogas']['benefic_yogas']]:
        score += 20

    return min(100, max(0, score))  # Clamp to 0-100


def calculate_wealth_potential(kundali) -> float:
    """
    Calculate wealth potential

    Factors:
    - 2nd house strength (wealth house)
    - 11th house strength (gains house)
    - Jupiter & Venus strength (wealth planets)
    - D2 Hora chart analysis
    """
    score = 0

    # 2nd house
    house_2_planets = len(kundali['houses'][2]['planets'])
    score += house_2_planets * 15
    score += kundali['houses'][2]['lord_strength'] / 5

    # 11th house (gains)
    house_11_planets = len(kundali['houses'][11]['planets'])
    score += house_11_planets * 15
    score += kundali['houses'][11]['lord_strength'] / 5

    # Jupiter & Venus strength
    jupiter_strength = kundali['shad_bala']['planetary_strengths']['Jupiter']['strength_percentage']
    venus_strength = kundali['shad_bala']['planetary_strengths']['Venus']['strength_percentage']
    score += (jupiter_strength + venus_strength) / 5

    # D2 Hora chart analysis
    if 'D2_Hora' in kundali['divisional_charts']:
        score += 20  # D2 favorable

    # Dhana Yoga presence
    if any(y['yoga_name'] == 'Dhana Yoga' for y in kundali['yogas']['benefic_yogas']):
        score += 20

    return min(100, max(0, score))


def calculate_marriage_happiness(kundali) -> float:
    """
    Calculate marriage happiness potential

    Factors:
    - 7th house strength (marriage)
    - Venus & Jupiter strength
    - D9 Navamsha alignment with D1
    - Absence of malefic combinations
    """
    score = 50  # Base score

    # 7th house analysis
    house_7_planets = len(kundali['houses'][7]['planets'])
    score += house_7_planets * 10
    score += kundali['houses'][7]['lord_strength'] / 2

    # Venus strength (marriage planet)
    venus_strength = kundali['shad_bala']['planetary_strengths']['Venus']['strength_percentage']
    score += (venus_strength / 100) * 20

    # Jupiter strength
    jupiter_strength = kundali['shad_bala']['planetary_strengths']['Jupiter']['strength_percentage']
    score += (jupiter_strength / 100) * 10

    # D9-D1 Alignment (very important)
    d9_alignment = kundali['divisional_charts']['alignment_analysis']['alignment_percentage']
    score += (d9_alignment / 100) * 20

    # Malefic aspects to 7th
    malefic_count = sum(1 for p in kundali['planets']
                        if p in ['Mars', 'Saturn', 'Rahu']
                        and kundali['planets'][p]['house'] == 7)
    score -= malefic_count * 10

    return min(100, max(0, score))
```

---

## 🎯 PART 4: ML FEATURES ENGINEERING PIPELINE

### 4.1 Feature Categories

**Category 1: Positional Features (18 features)**
```python
# Raw Planet Positions (0-360 degrees)
sun_degree, moon_degree, mars_degree, mercury_degree, jupiter_degree,
venus_degree, saturn_degree, rahu_degree, ketu_degree

# Sign Encodings (0-11)
sun_sign_encoded, moon_sign_encoded, mars_sign_encoded, ...,
ascendant_sign_encoded
```

**Category 2: Strength Features (27 features)**
```python
# For each planet: Shad Bala components
sun_sthana, sun_dig, sun_kala, sun_chesta, sun_naisargika, sun_drishti,
sun_total_strength, sun_strength_percentage

# Repeat for all 9 planets
# Total: 8 features × 9 planets = 72 features
```

**Category 3: House Features (48 features)**
```python
# For each house 1-12:
planets_in_house_1, house_1_lord_strength, house_1_strength,
planets_in_house_2, house_2_lord_strength, house_2_strength,
... (repeat for all 12 houses)

# Aggregate features:
total_planets_count, average_planets_per_house, houses_with_planets
```

**Category 4: Aspect Features (10 features)**
```python
total_conjunctions, total_oppositions, total_squares,
total_trines, total_sextiles,
benefic_aspects_count, malefic_aspects_count,
aspect_benefic_ratio, aspect_diversity_score,
strongest_aspect_type
```

**Category 5: Yoga Features (8 features)**
```python
total_yoga_count, benefic_yoga_count, malefic_yoga_count,
average_yoga_strength,
raj_yoga_present, parivartana_yoga_present,
neecha_bhanga_yoga_present, gaj_kesari_yoga_present
```

**Category 6: Dasha Features (6 features)**
```python
dasha_planet_strength, current_dasha_duration,
years_into_current_dasha, years_remaining_in_dasha,
next_dasha_planet_strength, dasha_transition_timing
```

**Category 7: Varga Features (12 features)**
```python
d1_d2_alignment_score, d1_d7_alignment_score, d1_d9_alignment_score,
d2_d7_alignment_score, d2_d9_alignment_score, d7_d9_alignment_score,
average_varga_alignment,
d9_marriage_favorable, d2_wealth_favorable, d7_fertility_favorable,
varga_consistency_score, varga_diversity_score
```

**Category 8: Retrograde Features (5 features)**
```python
total_retrograde_planets, retrograde_strength_planets,
retrograde_weak_planets, retrograde_benefic_ratio,
retrograde_karmic_intensity
```

**Category 9: Nakshatra Features (10 features)**
```python
ascendant_nakshatra_encoded, moon_nakshatra_encoded,
sun_nakshatra_encoded,
total_planets_in_nakshatras, nakshatra_distribution_entropy,
lordship_strength_average,
aligned_nakshatras_count, conflicting_nakshatras_count,
nakshatra_element_balance, nakshatra_gunas_balance
```

**Total Features: ~150-200 numerical features**

### 4.2 Feature Normalization & Transformation

```python
def normalize_features(features_df):
    """
    Normalize all features to 0-1 range or standardize
    """

    # For degree-based features (0-360): Normalize to 0-1
    degree_features = [col for col in features_df.columns if 'degree' in col]
    features_df[degree_features] = features_df[degree_features] / 360

    # For percentage features (0-100): Normalize to 0-1
    percentage_features = [col for col in features_df.columns if 'strength' in col or 'percentage' in col]
    features_df[percentage_features] = features_df[percentage_features] / 100

    # For count features: Standardize using Z-score
    count_features = [col for col in features_df.columns if 'count' in col]
    for col in count_features:
        mean = features_df[col].mean()
        std = features_df[col].std()
        features_df[col] = (features_df[col] - mean) / (std + 1e-8)

    # Handle missing values
    features_df = features_df.fillna(0)

    return features_df
```

---

## 🎯 PART 5: DATA PREPARATION WORKFLOW

### 5.1 Complete Data Pipeline

```
Phase 1: DATA GENERATION
├── Generate 10,000 synthetic birth parameters
├── Call backend API for each
├── Extract Kundali data
└── Store raw responses

Phase 2: FEATURE EXTRACTION
├── Parse API responses
├── Extract ~200 features per record
├── Handle missing values
└── Store in intermediate format

Phase 3: LABEL GENERATION
├── Apply Vedic astrology rules
├── Calculate target variables
├── Ensure label distribution
└── Validate against domain knowledge

Phase 4: DATA VALIDATION
├── Check for duplicates
├── Verify value ranges
├── Detect outliers
├── Ensure data quality score > 80%

Phase 5: FEATURE ENGINEERING
├── Normalize features
├── Create interaction features
├── Perform dimensionality reduction
├── Select top features (PCA)

Phase 6: DATA SPLITTING
├── 70% Training set
├── 15% Validation set
├── 15% Test set
└── Stratified by target variables

Phase 7: CSV EXPORT
├── Export training data
├── Export validation data
├── Export test data
└── Save feature dictionary
```

### 5.2 Data Quality Checklist

```
✓ No duplicate records
✓ All features in valid ranges
✓ No more than 5% missing values
✓ Target distribution is balanced
✓ Feature correlations identified
✓ Outliers documented
✓ Date/time values valid
✓ Geographic coordinates valid
✓ Data version controlled
✓ Metadata complete
```

---

## 🎯 PART 6: ML MODEL TRAINING APPROACH

### 6.1 Prediction Tasks (Multi-Output Learning)

**Task 1: Life Area Assessment (Regression)**
```python
Targets:
- career_potential (0-100)
- wealth_potential (0-100)
- marriage_happiness (0-100)
- children_prospects (0-100)
- health_status (0-100)
- spiritual_inclination (0-100)

Model: Gradient Boosting (XGBoost) or Neural Network
Evaluation: R², RMSE, MAE
```

**Task 2: Overall Chart Analysis (Regression)**
```python
Targets:
- chart_strength (0-100)
- life_ease_score (0-100)
- success_probability (0-100)

Model: Ensemble method
Evaluation: R², RMSE
```

**Task 3: Life Events Prediction (Classification/Regression)**
```python
Targets:
- marriage_age (regression, 16-60 years)
- children_count (regression, 0-5)
- career_changes_frequency (regression, 0-10)
- health_issues_probability (classification, High/Medium/Low)

Model: Separate models for each prediction type
```

### 6.2 Model Architecture

```
Input Layer (200 features)
    ↓
Normalization Layer
    ↓
Dense Layer (128 units, ReLU)
    ↓
Batch Normalization
    ↓
Dropout (0.3)
    ↓
Dense Layer (64 units, ReLU)
    ↓
Batch Normalization
    ↓
Dropout (0.2)
    ↓
Dense Layer (32 units, ReLU)
    ↓
Output Layers (Multi-task Learning):
├── Career Potential (Dense 1, Sigmoid 0-1)
├── Wealth Potential (Dense 1, Sigmoid 0-1)
├── Marriage Happiness (Dense 1, Sigmoid 0-1)
├── Children Prospects (Dense 1, Sigmoid 0-1)
├── Health Status (Dense 1, Sigmoid 0-1)
└── Spiritual Inclination (Dense 1, Sigmoid 0-1)
```

### 6.3 Model Training Configuration

```python
# Training Parameters
batch_size: 32
epochs: 100
validation_split: 0.15
learning_rate: 0.001
optimizer: Adam
loss_function: MSE (for regression) / Binary Crossentropy (for classification)
metrics: R², RMSE, MAE for regression; Accuracy, F1 for classification

# Early Stopping
patience: 15 epochs
restore_best_weights: True
monitor: validation_loss

# Learning Rate Schedule
initial_lr: 0.001
reduce_on_plateau: True
factor: 0.5
patience: 5
min_lr: 1e-6
```

---

## 🎯 PART 7: IMPLEMENTATION STEPS

### Step 1: Create Synthetic Data Generator Script

```python
# File: server/ml/synthetic_data_generator.py

import requests
import random
from datetime import datetime, timedelta
import json
import csv

class SyntheticKundaliGenerator:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        self.cities = [...]  # Major world cities with lat/long/timezone

    def generate_birth_date(self):
        """Generate random birth date 1950-2020"""
        start = datetime(1950, 1, 1)
        end = datetime(2020, 12, 31)
        return start + timedelta(days=random.randint(0, (end-start).days))

    def generate_synthetic_dataset(self, num_records=10000, output_file='training_data.csv'):
        """Generate num_records synthetic Kundali records"""
        dataset = []

        for i in range(num_records):
            # Generate birth parameters
            birth_date = self.generate_birth_date()
            birth_time = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}"
            city = random.choice(self.cities)

            # Call API
            response = self.call_api({
                'birthDate': birth_date.strftime('%Y-%m-%d'),
                'birthTime': birth_time,
                'latitude': city['latitude'],
                'longitude': city['longitude'],
                'timezone': city['timezone']
            })

            # Extract features
            features = self.extract_features(response)

            # Generate labels
            labels = self.generate_labels(response)

            # Combine
            record = {**features, **labels, 'is_synthetic': True}
            dataset.append(record)

            if (i+1) % 100 == 0:
                print(f"Generated {i+1}/{num_records}")

        # Save to CSV
        self.save_to_csv(dataset, output_file)
        return dataset
```

### Step 2: Create Feature Extractor

```python
# File: server/ml/feature_extractor.py

class FeatureExtractor:
    def extract_features(self, kundali_response):
        """Extract 200+ features from Kundali response"""

        features = {}

        # Planet degrees
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
            features[f'{planet.lower()}_degree'] = kundali_response['planets'][planet]['longitude']
            features[f'{planet.lower()}_sign'] = self.encode_sign(kundali_response['planets'][planet]['sign'])

        # House features
        for house in range(1, 13):
            features[f'planets_in_house_{house}'] = len(kundali_response['houses'][house]['planets'])
            features[f'house_{house}_lord_strength'] = kundali_response['houses'][house]['lord_strength']

        # Strength features (Shad Bala)
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            strength_data = kundali_response['shad_bala']['planetary_strengths'][planet]
            features[f'{planet.lower()}_strength'] = strength_data['strength_percentage']
            features[f'{planet.lower()}_sthana'] = strength_data['breakdown']['sthana_bala']
            features[f'{planet.lower()}_dig'] = strength_data['breakdown']['dig_bala']
            # ... all 6 strength components

        # Yoga features
        features['yoga_count'] = len(kundali_response['yogas']['benefic_yogas']) + len(kundali_response['yogas']['malefic_yogas'])
        features['benefic_yoga_count'] = len(kundali_response['yogas']['benefic_yogas'])

        # Varga alignment
        features['d1_d9_alignment'] = kundali_response['divisional_charts']['alignment_analysis']['alignment_percentage']

        return features
```

### Step 3: Create Label Generator

```python
# File: server/ml/label_generator.py

class LabelGenerator:
    def generate_labels(self, kundali_response):
        """Generate target labels using Vedic astrology rules"""

        return {
            'career_potential': self.calculate_career_potential(kundali_response),
            'wealth_potential': self.calculate_wealth_potential(kundali_response),
            'marriage_happiness': self.calculate_marriage_happiness(kundali_response),
            'children_prospects': self.calculate_children_prospects(kundali_response),
            'health_status': self.calculate_health_status(kundali_response),
            'spiritual_inclination': self.calculate_spiritual_inclination(kundali_response),
            'chart_strength': self.calculate_chart_strength(kundali_response),
            'life_ease_score': self.calculate_life_ease_score(kundali_response)
        }
```

### Step 4: Data Validation Script

```python
# File: server/ml/data_validator.py

class DataValidator:
    def validate_dataset(self, dataset):
        """Validate generated dataset quality"""

        checks = {
            'duplicate_check': len(dataset) == len(set(str(r) for r in dataset)),
            'feature_ranges': self.check_feature_ranges(dataset),
            'missing_values': self.check_missing_values(dataset),
            'target_distribution': self.check_target_distribution(dataset),
            'outliers': self.detect_outliers(dataset)
        }

        quality_score = sum(checks.values()) / len(checks) * 100

        return {
            'checks': checks,
            'quality_score': quality_score,
            'status': 'PASS' if quality_score > 80 else 'FAIL'
        }
```

---

## 🎯 PART 8: TIMELINE & DELIVERABLES

### Week 1: Setup & Infrastructure
- [ ] Create synthetic data generator script
- [ ] Create feature extractor
- [ ] Create label generator
- [ ] Setup data validation

### Week 2: Data Generation
- [ ] Generate 10,000 synthetic records
- [ ] Validate data quality
- [ ] Handle errors and edge cases
- [ ] Create backup

### Week 3: Feature Engineering
- [ ] Extract all 200+ features
- [ ] Normalize and transform
- [ ] Perform EDA
- [ ] Feature selection

### Week 4: ML Model Training
- [ ] Create training pipeline
- [ ] Train initial models
- [ ] Hyperparameter tuning
- [ ] Performance evaluation

### Week 5: Deployment
- [ ] Save trained models
- [ ] Create prediction API endpoints
- [ ] Test end-to-end pipeline
- [ ] Document system

---

## 🎯 EXPECTED OUTCOMES

### Dataset Specifications
- **Total Records:** 10,000 synthetic + 100-500 real = 10,100-10,500 records
- **Features per Record:** 200+
- **Training/Validation/Test Split:** 70% / 15% / 15%
- **Target Variables:** 8 continuous + 2 categorical
- **Data Quality Score:** > 85%

### Model Performance Targets
- **Career Potential R²:** > 0.75
- **Wealth Potential R²:** > 0.75
- **Marriage Happiness R²:** > 0.70
- **Chart Strength R²:** > 0.80
- **Overall Model Accuracy:** > 80%

---

## ✅ READY TO IMPLEMENT

This plan provides:
1. ✅ Complete dataset schema
2. ✅ Synthetic data generation strategy
3. ✅ Feature engineering pipeline
4. ✅ ML model approach
5. ✅ Implementation steps
6. ✅ Timeline and deliverables

**Next Step:** Create and run the synthetic data generator script!