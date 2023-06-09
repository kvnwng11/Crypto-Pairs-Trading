# Property of Kevin Wang
# website: kvnwng11.github.io

import pandas as pd
import numpy as np
import statsmodels.api as sm
from collections import deque
from io import StringIO
import os
import shutil

""" Declare variables """
data_path = '/' # Folder where price data is stored
state_path = '/' # Folder where state data is stored
pairs = [ # list of pairs
    ['', '']
] 


window = 30 * 1440
stop_loss = -0.9
commission = 0
entry_zscore = 1
exit_zscore = 0


today = pd.to_datetime("today")  # get current timestamp


def trade(pair):
    """
    Description: Backtests a pairs trading strategy between a pair of coins.

    Params:
        pair: An array containing the list of coins to trade (has only 2 elements).
    """
    # initialize
    statefile = ''
    x_label = pair[0]
    y_label = pair[1]
    x_position = 0
    y_position = 0
    current_return = 0

    # create statefile if non-existent
    if not os.path.exists(state_path+statefile):
        src = state_path+'template.csv'
        dst = state_path+statefile
        shutil.copy(src, dst)

    """ Load in data (removed) """
    raw_data = pd.DataFrame()

    # starting balance
    balance = 1000

    # loop through all price data
    for t in range(window+1, len(raw_data)):
        x_old_position = x_position
        y_old_position = y_position
        past_data = raw_data[[x_label,y_label]][t-window-1:t-1]
        x = np.array(past_data[x_label])
        y = np.array(past_data[y_label])
        curr_x = raw_data[x_label][t]
        curr_y = raw_data[y_label][t]

        # simple beta (hacky solution)
        reg = sm.OLS(np.log(y), sm.add_constant(np.log(x)))
        reg = reg.fit()
        b0 = reg.params[1]
        hedge_ratio = b0

        """ Find current z-score (removed) """

        # calculate the current return of the portfolio
        current_return = x_old_position*(curr_x/raw_data[x_label][t-1] - 1) + y_old_position*(curr_y/raw_data[y_label][t-1] - 1)

        """ Trading Logic (removed) """

        # calculate returns
        balance *= (1+current_return)

        """ Update State File (removed)"""


def execute():
    """
    Description: Backtests the strategy for each pair of coins.
    """
    for pair in pairs:
        trade(pair)

execute()
