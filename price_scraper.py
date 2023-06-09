# By Kevin Wang
# website: kvnwng11.github.io

import pandas as pd
import datetime as dt
import os
from collections import deque
from io import StringIO
from binance.client import Client
import warnings
warnings.filterwarnings("ignore")

# Declare Binance API variables
api_key = 'your_api_key'
api_secret = 'your_api_secret_key'
client = Client(api_key, api_secret)

# Declare variables
path = '/'
symbols = ['BTC', 'ETH']


def GetHistoricalData(coin, start_time, end_time):
    """
    Description: Given a start time and end time (not necessarily on the same day), returns the minute prices of a given cryptocurrency.

    Arguments:
        coin: The ticker of the coin
        start_time: The start of the time period
        end_time: The end of the time period
    """
    # Binance API Call
    api_result = client.get_historical_klines(
        f'{coin}USDT', Client.KLINE_INTERVAL_1MINUTE, str(start_time), str(end_time))

    # Format data
    price_data = pd.DataFrame(api_result, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'closeTime',
                                                   'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
    price_data['time'] = pd.to_datetime(
        price_data['time'], unit='ms').dt.strftime("%Y-%m-%d %H:%M:%S")
    price_data = price_data.drop(['closeTime', 'quoteAssetVolume', 'numberOfTrades',
                                  'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'], axis=1)

    return price_data[['time', 'close']]


def get_historical_prices():
    """
    Description: Obtains minute prices staarting January 1, 2022 until the present date. Outputs to a CSV file.
    """
    # Loop over all coins
    for asset in symbols:
        csv_path = path+asset+'.csv'

        # If no csv file exists, create it
        if not os.path.exists(csv_path):
            # Declare start date and end date
            end = dt.datetime.utcnow()
            end = end - \
                dt.timedelta(minutes=1, seconds=end.second,
                             microseconds=end.microsecond)
            start = dt.strptime("2022-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

            # Output to CSV
            prices = pd.DataFrame(GetHistoricalData(asset, start, end))
            prices[['time', 'close']].to_csv(
                csv_path, mode='w', header=False, index=False)


def update_prices():
    """
    Description: Fills in holes in the minute data. Also gets the most recent price. Writes everything to a CSV file.
    """
    # Loop over all coins
    for asset in symbols:
        csv_path = path+asset+'.csv'

        # Load in csv
        with open(csv_path, 'r') as f:
            N = 2
            q = deque(f, N)
        prices = pd.read_csv(StringIO(''.join(q)), header=None)

        # Rename columns
        prices.columns = ['time', 'close']

        # Get the current price
        start = dt.datetime.strptime(
            prices['time'].iloc[-1], "%Y-%m-%d %H:%M:%S") + dt.timedelta(minutes=1)
        end = dt.datetime.utcnow()
        end = end - dt.timedelta(seconds=end.second,
                                 microseconds=end.microsecond)
        prices = pd.DataFrame(GetHistoricalData(asset, start, end))

        # Write to CSV
        prices[['time', 'close']].to_csv(
            csv_path, mode='a', header=False, index=False)


get_historical_prices()
update_prices()
