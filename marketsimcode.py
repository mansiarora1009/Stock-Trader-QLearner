#### NAME : MANSI ARORA 
#### USER ID: marora33
#### GT ID: 903339702

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
#orders_file = "./orders/orders-12.csv"
#start_val = 1000000
#commission=0
#impact=0.005
def author():
    return 'marora33'

def compute_portvals(orders, start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    #orders = pd.read_csv(orders_file)
    start_date = dt.datetime.strptime(orders['Date'].min(), "%Y-%m-%d")
    end_date = dt.datetime.strptime(orders['Date'].max(), "%Y-%m-%d")
    df_price = get_data(list(orders['Symbol'].unique()), pd.date_range(start_date, end_date))
    df_price['CASH'] = 1
    df_price = df_price.drop('SPY', axis=1)

    # deleting non-trading days from the orders file
    dates = pd.date_range(start_date, end_date)
    orders['Date'] = orders['Date'].apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%d"))
    orders = orders.set_index('Date')
    tf = [i in dates for i in orders.index]
    orders = orders.drop(orders.index[[i for i, x in enumerate(tf) if not(x)]])

    df_trades = df_price.copy()
    df_trades[:] = 0

    for row in orders.iterrows():
        if(row[1][1] == 'BUY'):
            df_trades.loc[str(row[0]),row[1][0]]+= int(row[1][2])
            df_trades.loc[str(row[0]),'CASH']-= int(row[1][2])*df_price.loc[str(row[0]),row[1][0]]
        else:
            df_trades.loc[str(row[0]),row[1][0]]-= int(row[1][2])
            df_trades.loc[str(row[0]),'CASH']+= int(row[1][2])*df_price.loc[str(row[0]),row[1][0]]
        if (int(row[1][2])!=0):
                df_trades.loc[str(row[0]),'CASH']-= commission
                df_trades.loc[str(row[0]),'CASH']-= impact*int(row[1][2])*df_price.loc[str(row[0]),row[1][0]]

    df_holdings = df_trades.copy()
    df_holdings[:] = 0
    df_holdings.iloc[0] = df_trades.iloc[0]
    df_holdings['CASH'][0]+= start_val

    temp = df_holdings.index[0]
    for row in df_holdings[1:].iterrows():
        df_holdings.loc[str(row[0])]+=df_holdings.loc[temp] + df_trades.loc[str(row[0])]
        temp = str(row[0])

    df_value = df_holdings*df_price

    portvals = df_value.sum(axis=1)

    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
