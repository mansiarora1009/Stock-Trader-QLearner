#### NAME : MANSI ARORA 
#### USER ID: marora33
#### GT ID: 903339702

import pandas as pd 
import numpy as np
import datetime as dt
from util import get_data, plot_data
import matplotlib.pyplot as plt


def rolling_mean(prices, w=10, gen_plot=False): #here the price dataframe passed has extra days to account for the window size
    rm_df = prices.rolling(window=w).mean()
    if gen_plot:
        df_temp = pd.concat([rm_df[w+1:], prices[w+1:], prices[w+1:]/rm_df[w+1:]], keys=['Rolling Mean', 'JPM Price', 'Ratio'], axis=1)
        df_temp[['Rolling Mean','JPM Price']] = df_temp[['Rolling Mean','JPM Price']]/df_temp[['Rolling Mean','JPM Price']].iloc[0]
        plot_data(df_temp, "Simple Moving Average Indicator, Window = "+str(w),  xlabel="Date", ylabel="Value")
        pass
    ratio = prices/rm_df
    ratio = ratio.fillna(method= 'bfill')

    return ratio
    

def macd(prices, gen_plot=False): #here the price dataframe passed has extra days to account for the window size
    emaslow = prices.ewm(26, min_periods=1).mean()
    emafast = prices.ewm(12, min_periods=1).mean()
    macd = emafast - emaslow
    signal = macd.ewm(span=9).mean()
    cross = np.where(macd > signal, 1, 0)
    cross = np.where(macd < signal, -1, cross)
    if gen_plot:
        df_temp = pd.concat([emaslow,emafast,macd,signal], keys=['emaslow','emafast','MACD','Signal'], axis=1)
        plot_data(df_temp.iloc[:,2:], "MACD Indicator",  xlabel="Date", ylabel="Value")
        pass
    cross = pd.DataFrame(cross, index=prices.index)
    cross = cross.rename(columns = {0 : 'MACD'})
    #return cross
    return cross, macd


def bollinger_bands(prices, w=10, gen_plot=False):
    sma = prices.rolling(window=w).mean()
    rsd_df = prices.rolling(window=w).std()
    upperband = sma + 2*rsd_df
    lowerband = sma - 2*rsd_df
    if gen_plot:
        df_temp = pd.concat([sma[w+1:], prices[w+1:], upperband[w+1:], lowerband[w+1:]], keys=['Rolling Mean', 'Price', 'Upperband', 'Lowerband'], axis=1)
        df_temp = df_temp/df_temp.iloc[0]
        plot_data(df_temp, "Bollinger Bands", xlabel="Date", ylabel="Value")
        pass
    
    bb = prices.copy()
    bb[:] = 0
    #bb[prices>upperband] = 1
    #bb[prices<lowerband] = -1
    #bb.columns.values[0] = 'BB'
    return (prices>upperband)*1, (prices<lowerband)*1
    #up = prices - upperband
    #up = up.fillna(method= 'bfill')
    #low = prices - lowerband
    #low = low.fillna(method = 'bfill')
    #return up,low


def rsi(prices, n=10, gen_plot=False):
    gain = prices.copy()
    loss = prices.copy()
    delta = prices.diff().dropna()
    gain = prices*0
    loss = prices*0    
    for i in prices.index[1:]:
        #print(i)
        if (delta.loc[i] > 0)[0]:
            gain.loc[i] = delta.loc[i]
        elif (delta.loc[i] < 0)[0]:
            loss.loc[i] = -delta.loc[i]  
    avg_gain = gain.rolling(n).mean()
    avg_loss = loss.rolling(n).mean()    
    rs = avg_gain/avg_loss
    ind = 100 - 100 / (1 + rs) 
    rsi = ind.copy()
    rsi = rsi.fillna(method = 'bfill')
    if gen_plot:
        prices.plot(title='Price')
        plt.show()
        ind.plot(title = 'RSI')
        plt.show()
        pass  
    for i in prices.index:
            if (ind.loc[i] > 70)[0]:
                ind.loc[i] = 1
            elif (ind.loc[i] < 30)[0]:
                ind.loc[i] = -1
            else:
                ind.loc[i] = 0
    #ind.columns.values[0] = 'RSI'
    #return ind
    return rsi, ind
    
        
