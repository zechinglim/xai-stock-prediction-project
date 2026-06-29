
'''

-------------------
data_collection.py
-------------------

Downloads historical stock data from Yahoo Finance (yfinance) and saves it into structured raw dataset folder.

'''

# =====================================================
# IMPORTS
# =====================================================

import yfinance as yf
import pandas as pd
import os
import time
import logging
from datetime import datetime

from config import STOCKS, START_DATE, END_DATE, RAW_DATA_PATH

# =====================================================
# LOGGING SETUP
# =====================================================

logging.basicConfig(level = logging.INFO, format = '%(levelname)s | %(message)s')

# =====================================================
# OPTIMIZATION SETTINGS
# =====================================================

FORCE_REDOWNLOAD = True   # change to False if you want to skip existing files


# =====================================================
# DOWNLOAD SINGLE STOCK
# =====================================================

def download_stock_data(ticker, name, start_date=START_DATE, end_date=END_DATE):
    '''

    Download historical stock data from Yahoo Finance.

    '''

    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    logging.info(f'Downloading {name} ({ticker})')

    try:
        df = yf.download(ticker, start = start_date, end = end_date,progress=False)

        # Flatten MultiIndex columns returned by newer versions of yfinance
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if df.empty:
            logging.warning(f'No data found for {ticker}')
            return None

        # Add metadata
        df['Ticker'] = ticker
        df['Name'] = name

        # Convert index to column
        df.reset_index(inplace=True)

        # Standardize date format
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

        return df

    except Exception as e:
        logging.error(f'Failed {ticker}: {e}')
        return None


# =====================================================
# MAIN PIPELINE
# =====================================================

def download_all_stocks():
    '''

    Download data and save them in individual CSV file and combined dataset.

    '''

    # Create folder
    os.makedirs(RAW_DATA_PATH, exist_ok=True)

    # Setup counters
    all_data = []
    total = sum(len(v) for v in STOCKS.values())
    success = 0

    # Display status
    logging.info('=' * 60)
    logging.info(' STOCK DATA COLLECTION STARTED ')
    logging.info(f'Total stocks: {total}')
    logging.info('=' * 60)

    for country, stocks in STOCKS.items():

        logging.info(f'\nCountry: {country}')

        for name, ticker in stocks:

            # Create file names
            safe_ticker = ticker.replace('.', '_')
            safe_name = name.replace(' ', '_')

            file_path = os.path.join(RAW_DATA_PATH, f'{safe_ticker}_{safe_name}.csv')

            # Skip if file exists (this is when 'FORCE_REDOWNLOAD = False' in optimization settings)
            if not FORCE_REDOWNLOAD and os.path.exists(file_path):
                logging.info(f'Skipping existing file: {ticker}')
                continue

            df = download_stock_data(ticker, name)

            if df is None:
                continue

            # Save individual file
            df.to_csv(file_path, index=False)

            logging.info(f'Saved: {file_path}')

            all_data.append(df)
            success += 1

            time.sleep(0.5)  # avoid Yahoo Finance rate limit

    # =================================================
    # COMBINE ALL STOCKS
    # =================================================

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)

        combined_path = os.path.join(RAW_DATA_PATH,'all_stocks_combined.csv')

        combined.to_csv(combined_path, index=False)

        logging.info(f'Combined dataset saved: {combined_path}')
        logging.info(f'Total rows: {len(combined):,}')

    logging.info('=' * 60)
    logging.info(f'DONE: {success}/{total} stocks downloaded')
    logging.info('=' * 60)

    return all_data


# =====================================================
# VERIFICATION FUNCTION
# =====================================================

def verify_download():
    '''

    Quick check to confirm data integrity.

    '''

    try:
        path = os.path.join(RAW_DATA_PATH, 'all_stocks_combined.csv')
        df = pd.read_csv(path)

        logging.info(' ')
        logging.info('=' * 40)
        logging.info('DATA VALIDATION')
        logging.info('=' * 40)

        logging.info(f'Rows: {len(df):,}')
        logging.info(f'Stocks: {df['Ticker'].nunique()}')
        logging.info(f'Missing values: {df.isna().sum().sum()}')

        logging.info('Distribution:')
        logging.info(df['Ticker'].value_counts())

        return df

    except FileNotFoundError:
        logging.error('No dataset found. Run download first.')
        return None


# =====================================================
# MAIN EXECUTION
# =====================================================

if __name__ == '__main__':

    download_all_stocks()
    verify_download()
