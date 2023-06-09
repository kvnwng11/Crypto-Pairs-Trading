# By Kevin Wang
# website: kvnwng11.github.io

import pandas as pd
import numpy as np
import statsmodels.api as sm
from collections import deque
from io import StringIO
import os
import shutil

""" Declare variables """
data_path = '/'  # Folder where price data is stored
state_path = '/'  # Folder where state is stored
pairs = [  # Pairs to trade
    ['BTC', 'ETH']
]

""" Declare variables """
window = 30 * 1440
stop_loss = -0.9
commission = 0
entry_zscore = 1
exit_zscore = 0


today = pd.to_datetime("today")  # Get current timestamp


def trade(pair):
    """
    Description: Backtests the strategy on the given pair of coins.

    Arguments:
        pair: An array containing the list of coins to trade (has only 2 elements).
    """
    # Initialize
    statefile = ''
    x_label = pair[0]
    y_label = pair[1]
    x_position = 0
    y_position = 0
    current_return = 0

    # Create statefile if non-existent
    if not os.path.exists(state_path+statefile):
        src = state_path+'template.csv'
        dst = state_path+statefile
        shutil.copy(src, dst)

    """ Load in data (removed) """
    raw_data = pd.DataFrame()

    # Starting balance
    balance = 1000

    # Loop through all price data
    for t in range(window+1, len(raw_data)):
        # Get the current position
        x_old_position = x_position
        y_old_position = y_position
        past_data = raw_data[[x_label, y_label]][t-window-1:t-1]
        x = np.array(past_data[x_label])
        y = np.array(past_data[y_label])

        # Get the curent price
        curr_x = raw_data[x_label][t]
        curr_y = raw_data[y_label][t]

        # Simple beta
        beta = 1

        """ Find current z-score (removed) """

        """ Calculate the current return """
        current_return = x_old_position * \
            (curr_x/raw_data[x_label][t-1] - 1) + \
            y_old_position*(curr_y/raw_data[y_label][t-1] - 1)

        """ Trading Logic (removed) """

        """ Calculate returns """
        balance *= (1+current_return)

        """ Update State File (removed)"""


def execute():
    """
    Description: Backtests.
    """
    for pair in pairs:
        trade(pair)


execute()
