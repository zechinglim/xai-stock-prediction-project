'''

----------
config.py
----------

Central configuration for all modules
All constants are stored here for easy maintenance

'''

# =====================================================
# STOCK LIST
# =====================================================

STOCKS = {
    'Malaysia':
        [('Maybank', '1155.KL'),
        ('Public Bank', '1295.KL'),
        ('CIMB Group', '1023.KL'),
        ('RHB Bank', '1066.KL'),
        ('Hong Leong Bank', '5819.KL'),
        ('AmBank', '1015.KL'),
        ('Alliance Bank', '2488.KL'),
        ('AFFIN Bank', '5185.KL'),
        ('BIMB Holdings', '5258.KL')],

    'Singapore':
        [('DBS Bank', 'D05.SI'),
        ('OCBC Bank', 'O39.SI'),
        ('UOB Bank', 'U11.SI')]
        }

# =====================================================
# DATE RANGE
# =====================================================

START_DATE = '2018-01-01'
END_DATE = None  # None = today's date

# =====================================================
# PATHS
# =====================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # Finding project root

RAW_DATA_PATH = BASE_DIR / "data" / "raw"
FEATURE_DATA_PATH = BASE_DIR / "data" / "features"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed"
MODELS_PATH = BASE_DIR / "models"

# =====================================================
# FEATURE COLUMNS
# =====================================================

FEATURES_v1 = ['rsi',
            'macd',
            'macd_signal',
            'macd_diff',
            'sma_20',
            'sma_50',
            'ema_20',
            'ema_50',
            'bb_high',
            'bb_mid',
            'bb_low',
            'volume_sma',
            'returns',
            ]

FEATURES_v2 = ['rsi',
            'macd',
            'macd_signal',
            'macd_diff',
            'sma_20',
            'sma_50',
            'ema_20',
            'ema_50',
            'bb_high',
            'bb_mid',
            'bb_low',
            'volume_sma',
            'returns',

            # Additional features
            'returns_lag_1',
            'returns_lag_3',
            'returns_lag_5',
            'volatility_10',
            'volatility_20',
            'daily_range',
            'volume_change'
            ]

# =====================================================
# TARGET COLUMNS
# =====================================================

TARGET = 'target'

# =====================================================
# MODEL SETTINGS
# =====================================================
WALK_FORWARD_START_YEAR = 2021
