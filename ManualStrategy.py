#### NAME : MANSI ARORA 
#### USER ID: marora33
#### GT ID: 903339702

import indicators
import pandas as pd
import numpy as np
import datetime as dt
import marketsimcode
from util import get_data, plot_data


def testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
    dates = pd.date_range(sd, ed)
    a = []
    a.append(symbol)
    prices_all = get_data(a, dates)  
    prices = prices_all[symbol]
    prices_SPY = prices_all['SPY'] 
    orders = [] 
    sma = indicators.rolling_mean(prices, 10, True)
    ub,lb = indicators.bollinger_bands(prices, 10, True)
    cross, macd = indicators.macd(prices, True)
    rsi, ind = indicators.rsi(pd.DataFrame(prices), 10, True)
    
    orders = []
    holdings = 0
    
    for i in prices.index:
        if ind.loc[i][0] == 1 and cross.loc[i][0] ==1 and ub.loc[i] == 1 and (holdings==0 or holdings == 1000):
            orders.append((i,symbol,'SELL',1000))
            holdings-=1000
        elif ind.loc[i][0] == -1 and cross.loc[i][0]==-1 and lb.loc[i] == 1 and (holdings==0 or holdings == -1000):
            orders.append((i, symbol, 'BUY',1000))
            holdings+=1000
    
    orders = pd.DataFrame(orders)
    orders.columns = ['Date', 'Symbol',	'Order',	'Shares']
    orders['Date'] = orders['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))    
      
    return orders

    
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    ##### FOR IN-SAMPLE PERIOD
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2009,12,31)
    symbol = "JPM"
    sv = 1000000

    orders = testPolicy(symbol = "JPM", sd=sd, ed=ed, sv=sv)
    portvals = marketsimcode.compute_portvals(orders, start_val = 1000000, commission=9.95, impact=0.005)
    dates = pd.date_range(sd, ed)
    a = []
    a.append(symbol)
    prices_all = get_data(a, dates)  
    prices = prices_all[symbol]  
    
    cash = sv - 1000*prices[0]
    bm = prices.copy()
    bm[0] = sv
    bm[1:] = 1000*prices[1:]+cash
    
    x1, = plt.plot(bm/bm.iloc[0], 'blue', label='Benchmark')
    x2, = plt.plot(portvals/portvals[0], 'black', label='Manual Strategy')
    sell, = plt.plot([sd],[1],color='red', label='Short Entry')
    buy, = plt.plot([sd], [1],color='green', label='Long Entry')
    plt.legend(handles=[x1, x2, sell, buy], loc = 'upper left')
    plt.title("Manual Strategy vs Benchmark for In-Sample Period")
    
    selldates = orders['Date'][orders['Order']=='SELL']
    buydates = orders['Date'][orders['Order']=='BUY']
    
    for i in selldates:
        plt.axvline(x=i, ymin=0, ymax=0.1,color = 'r')
    
    for i in buydates:
        plt.axvline(x=i, ymin=0, ymax=0.1,color = 'g')
        
    cr = portvals[-1]/portvals[0] - 1
    
    dr = (portvals/portvals.shift()) - 1
    dr = dr[1:]
    
    adr = dr.mean()
 
    sdr = dr.std()
        

        
    ##### FOR OUT-SAMPLE PERIOD
    import matplotlib.pyplot as plt
    sd=dt.datetime(2010,1,1)
    ed=dt.datetime(2011,12,31)
    symbol = "JPM"
    sv = 1000000

    orders = testPolicy(symbol = "JPM", sd=sd, ed=ed, sv=sv)
    portvals = marketsimcode.compute_portvals(orders, start_val = 1000000, commission=9.95, impact=0.005)
    dates = pd.date_range(sd, ed)
    a = []
    a.append(symbol)
    prices_all = get_data(a, dates)  
    prices = prices_all[symbol]  
    
    cash = sv - 1000*prices[0]
    bm = prices.copy()
    bm[0] = sv
    bm[1:] = 1000*prices[1:]+cash
    
    x1, = plt.plot(bm/bm.iloc[0], 'blue', label='Benchmark')
    x2, = plt.plot(portvals/portvals[0], 'black', label='Manual Strategy')
    sell, = plt.plot([sd],[1],color='red', label='Short Entry')
    buy, = plt.plot([sd], [1],color='green', label='Long Entry')
    plt.legend(handles=[x1, x2, sell, buy], loc = 'upper left')
    plt.title("Manual Strategy vs Benchmark for Out-Sample Period")
    
    selldates = orders['Date'][orders['Order']=='SELL']
    buydates = orders['Date'][orders['Order']=='BUY']
    
    for i in selldates:
        plt.axvline(x=i, ymin=0, ymax=0.1,color = 'r')
    
    for i in buydates:
        plt.axvline(x=i, ymin=0, ymax=0.1,color = 'g')
    
    cr = portvals[-1]/portvals[0] - 1
    
    dr = (portvals/portvals.shift()) - 1
    dr = dr[1:]
    
    adr = dr.mean()
 
    sdr = dr.std()
    
    
    