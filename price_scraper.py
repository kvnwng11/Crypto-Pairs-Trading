# Property of Kevin Wang
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
    Description: Given a start time and end time (not necessarily on the same day), returns the minute prices of a cryptocurrency

    Params:
        coin: The ticker of the coin
        start_time: The start of the time period
        end_time: The end of the time period
    """
    untilThisDate = end_time
    sinceThisDate = start_time
    candle = client.get_historical_klines(f'{coin}USDT', Client.KLINE_INTERVAL_1MINUTE, str(sinceThisDate), str(untilThisDate))

    df = pd.DataFrame(candle, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'closeTime',
                        'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
    df['time'] = pd.to_datetime(df['time'], unit='ms').dt.strftime("%Y-%m-%d %H:%M:%S")
    df = df.drop(['closeTime', 'quoteAssetVolume', 'numberOfTrades',
                    'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'], axis=1)

    return df[['time','close']]

def get_historical_prices():
    """
    Description: If needed, obtains minute prices staarting January 1, 2022 until the present date.
    """
    # create and populate needed csvs
    for asset in symbols:
        asset_path = path+asset+'.csv'
        # if no csv file exists, pull minute data from the last 30 days
        if not os.path.exists(asset_path):
            end = dt.datetime.utcnow()
            end = end - dt.timedelta(minutes=1, seconds=end.second, microseconds=end.microsecond)
            start = dt.strptime("2022-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

            prices = pd.DataFrame(GetHistoricalData(asset, start, end))
            prices[['time', 'close']].to_csv(asset_path, mode='w', header=False, index=False)

def update_prices():
    """
    Description: Fixes any gaps in the minute data and gets the most recent price.
    """
    # update any gaps in the csv file
    for asset in symbols:
        asset_path = path+asset+'.csv'
        # load in csv
        with open(asset_path, 'r') as f:
            N = 2
            q = deque(f, N)
        prices = pd.read_csv(StringIO(''.join(q)), header=None)
        prices.columns = ['time', 'close']

        start = dt.datetime.strptime(prices['time'].iloc[-1], "%Y-%m-%d %H:%M:%S") + dt.timedelta(minutes=1)
        end = dt.datetime.utcnow()
        end = end - dt.timedelta(seconds=end.second, microseconds=end.microsecond)
        prices = pd.DataFrame(GetHistoricalData(asset, start, end))
        prices[['time', 'close']].to_csv(asset_path, mode='a', header=False, index=False)

get_historical_prices()
update_prices()
