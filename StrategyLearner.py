#### NAME : MANSI ARORA 
#### USER ID: marora33
#### GT ID: 903339702

"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""

import datetime as dt
import pandas as pd
import util as ut
import random
import indicators
import QLearner as ql
import numpy as np

class StrategyLearner(object):

    def author(self):
        return 'marora33'

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact

        self.learner = ql.QLearner(num_states=125,\
        num_actions = 3, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.7, \
        radr = 0.999, \
        dyna = 0, \
        verbose=False)


    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd+ dt.timedelta(-30), ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        #if self.verbose: print prices

        # indicators
        cross, macd = indicators.macd(prices)
        rsi,ind = indicators.rsi(prices)
        sma = indicators.rolling_mean(prices)
        macd = macd[macd.index > sd]
        rsi = rsi[rsi.index > sd]
        sma = sma[sma.index > sd]

        prices = prices[prices.index > sd]

        #discretization
        macd_bin = pd.cut(macd.transpose().iloc[0],5, labels=[0,1,2,3,4]).astype(int)
        rsi_bin = pd.cut(rsi.transpose().iloc[0],5, labels=[0,1,2,3,4]).astype(int)
        sma_bin = pd.cut(sma.transpose().iloc[0],5, labels=[0,1,2,3,4]).astype(int)

        state = macd_bin + rsi_bin*5 + sma_bin*25
        epoch = 0
        temp = 0
        total_reward = 10
        #
        
        # add your code to do learning here
        while temp!=total_reward and epoch < 200:
            #print(temp, total_reward)
            #print(state)
            epoch+=1            
            temp = total_reward
            action = self.learner.querysetstate(0)
            #print("a",action)
            holdings = 0     
            port_val = 0
            total_reward = 0
            cash = sv
            for i in range(1,len(prices)):
                if (action==0):
                    pass
                elif (action==1): #buy or long position
                    if (holdings == 1000):
                        pass
                    elif (holdings == 0): #buy 1000 shares
                        holdings +=  1000
                        cash -= (holdings*prices.iloc[i-1]*(1+self.impact))
                        port_val += (holdings*prices.iloc[i-1]*(1+self.impact))
                    elif (holdings == -1000): #buy 2000 shares
                        holdings +=  2000
                        cash -= (holdings*prices.iloc[i-1]*(1+self.impact))
                        port_val += (holdings*prices.iloc[i-1]*(1+self.impact))
                elif (action==2): #sell or short position
                    if (holdings == -1000):
                        pass
                    elif (holdings == 0): #short 1000 shares
                        holdings -=  1000
                        cash += (holdings*prices.iloc[i-1]*(1-self.impact))
                        port_val -= (holdings*prices.iloc[i-1]*(1-self.impact))
                    elif (holdings == 1000): #short 2000 shares
                        holdings -=  2000
                        cash += (holdings*prices.iloc[i-1]*(1-self.impact))
                        port_val -= (holdings*prices.iloc[i-1]*(1-self.impact))
                #stepreward = int((prices.iloc[i] - prices.iloc[i-1]))*holdings*(1-self.impact)
                stepreward = ((float((prices.iloc[i] - prices.iloc[i-1]))/float(prices.iloc[i-1]))-self.impact)*holdings
                action = self.learner.query(state[i], stepreward)
                total_reward += stepreward
            #print(total_reward)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        prices = prices_all[[symbol]]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        #if self.verbose: print prices

        # indicators
        cross, macd = indicators.macd(prices)
        rsi,ind = indicators.rsi(prices)
        sma = indicators.rolling_mean(prices)

        macd_bin = pd.cut(macd.transpose().iloc[0],5, labels=[0,1,2,3,4]).astype(int)
        rsi_bin = pd.cut(rsi.transpose().iloc[0],5, labels=[0,1,2,3,4]).astype(int)
        sma_bin = pd.cut(sma.transpose().iloc[0],5, labels=[0,1,2,3,4]).astype(int)

        state = macd_bin + rsi_bin*5 + sma_bin*25
        holdings = 0
        total_reward = 0
        port_val = sv

        #trades
        trades = prices_all[[symbol,]]  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later
        trades.values[:,:] = 0

        for j,i in state.iteritems():
            #print(int(port_val))
            action = np.argmax(self.learner.Q[i])
            if action == 0:
                reward = int((prices.iloc[i] - prices.iloc[i-1])*holdings*(1-self.impact))
                total_reward+=reward

            elif action == 2:
                #selling
                if holdings == 0:
                    reward = int((prices.iloc[i] - prices.iloc[i-1])*-1000*(1-self.impact))
                    holdings -= 1000
                    trades.loc[j][0] = -1000
                    total_reward+=reward
                    port_val-=prices.iloc[i-1]*1000
                elif holdings == 1000:
                    reward = int((prices.iloc[i] - prices.iloc[i-1])*-2000*(1-self.impact))
                    holdings -= 2000
                    trades.loc[j][0] = -2000
                    total_reward+=reward
                    port_val-=prices.iloc[i-1]*2000

            elif action == 1:
                #buying
                if holdings == -1000:
                    reward = int((prices.iloc[i] - prices.iloc[i-1])*2000*(1-self.impact))
                    holdings += 2000
                    trades.loc[j][0] = 2000
                    total_reward+=reward
                    port_val+=prices.iloc[i-1]*2000
                elif holdings == 0:
                    reward = int((prices.iloc[i] - prices.iloc[i-1])*1000*(1-self.impact))
                    holdings += 1000
                    trades.loc[j][0] = 1000
                    total_reward+=reward
                    port_val+=prices.iloc[i-1]*1000
        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        if self.verbose: print prices_all
        return trades

#if __name__=="__main__":
#    print "One does not simply think up a strategy"
#

#learner = StrategyLearner(verbose = False, impact = 0.000) # constructor
#learner.addEvidence(symbol = "AAPL", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000) # training phase
#df_trades = learner.testPolicy(symbol = "AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000) # testing phase
#df_trades.to_csv('trades.csv')

#    import datetime as dt
#    import pandas as pd
#    import util as ut
#    import random
#    import indicators2 as ind
#    import QLearner_submitted as ql
#    symbol = "IBM"
#    sd=dt.datetime(2008,1,1)
#    ed=dt.datetime(2009,1,1)
#    sv = 10000
#
#    st = StrategyLearner()
#    st.addEvidence()
#    print("starting testing...")
#
#    
#    trades = st.testPolicy()
#    trades.to_csv('trades.csv')
#
#
#import StrategyLearner as sl
