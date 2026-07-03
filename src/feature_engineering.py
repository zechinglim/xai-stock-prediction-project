
'''

-----------------------
feature_engineering.py
-----------------------

Transform raw stock data into machine learning-ready technical indicators and target variables for price movement prediction.

'''

# =====================================================
# IMPORTS
# =====================================================

import os
import logging
import pandas as pd
import pandas_ta as ta

from config import RAW_DATA_PATH, PROCESSED_DATA_PATH

# =====================================================
# LOGGING SETUP
# =====================================================

logging.basicConfig(level = logging.INFO, format = '%(levelname)s | %(message)s')

# =====================================================
# MAIN FEATURES FUNCTION
# =====================================================

def add_features(df):

    df = df.copy()

    # returns
    df['returns'] = df['Close'].pct_change()

    # SMA
    df['sma_20'] = df['Close'].rolling(20).mean()
    df['sma_50'] = df['Close'].rolling(50).mean()

    # EMA
    df['ema_20'] = df['Close'].ewm(span=20, adjust = False).mean()
    df['ema_50'] = df['Close'].ewm(span=50, adjust = False).mean()

    # volume SMA
    df['volume_sma'] = df['Volume'].rolling(20).mean()

    # RSI
    df['rsi'] = ta.rsi(df['Close'], length = 14)

    # MACD
    macd = ta.macd(df['Close'])

    if macd is None:

        logging.warning('MACD returned None')

    else:
        df['macd'] = macd['MACD_12_26_9']
        df['macd_signal'] = macd['MACDs_12_26_9']
        df['macd_diff'] = macd['MACDh_12_26_9']

    # Bollinger Bands
    bb = ta.bbands(df['Close'], length = 20)
    df['bb_low'] = bb['BBL_20_2.0_2.0']
    df['bb_mid'] = bb['BBM_20_2.0_2.0']
    df['bb_high'] = bb['BBU_20_2.0_2.0']

    return df

# =====================================================
# MAIN PIPELINE
# =====================================================

def build_dataset(df):

    # In case if missing important columns
    if 'Close' not in df.columns:
        raise ValueError("Missing required column: Close")

    if 'Volume' not in df.columns:
        raise ValueError("Missing required column: Volume")

    if 'Ticker' not in df.columns:
        raise ValueError("Missing required column: Ticker")

    logging.info("Adding features to the dataset...")
    logging.info(f"Initial dataset shape: {df.shape}")

    df = df.groupby('Ticker', group_keys = False).apply(add_features)

    logging.info("Feature engineering completed!")

    # create target
    df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    # remove last row issue
    df = df.iloc[:-1]

    # drop NaNs
    df = df.dropna()

    logging.info(f"Final dataset shape: {df.shape}")

    return df

# =====================================================
# MAIN EXECUTION
# =====================================================

if __name__ == '__main__':

    try:

        logging.info("Loading raw data...")

        df = pd.read_csv(RAW_DATA_PATH / 'all_stocks_combined.csv')
        df['Date'] = pd.to_datetime(df['Date'])

        logging.info("Data loaded successfully.")

        df_processed = build_dataset(df)

        processed_path = os.path.join(PROCESSED_DATA_PATH,'processed_data.csv')

        df_processed.to_csv(processed_path, index = False)

        logging.info(f"Processed data saved to: {processed_path}")
        logging.info("Feature engineering pipeline completed successfully.")

    except Exception as e:

        logging.error(f"Feature engineering failed: {e}")

        raise
