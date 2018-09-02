#### NAME : MANSI ARORA 
#### USER ID: marora33
#### GT ID: 903339702

# This is Experiment 2
import ManualStrategy
import StrategyLearner
import datetime as dt
import matplotlib.pyplot as plt
import marketsimcode
from util import get_data, plot_data
import pandas as pd


# Specifying training time periods
train_sd=dt.datetime(2008,1,1)
train_ed=dt.datetime(2009,12,31)
# Specifying symbol
symbol = "JPM"
# Specifying Start value
sv = 100000
impact = 0.03

############################ Strategy Learner #################################
st = StrategyLearner.StrategyLearner(impact = impact)
st.addEvidence(symbol = symbol, \
        sd=train_sd, \
        ed=train_ed, \
        sv = sv)
orders_strategy = st.testPolicy(symbol = symbol , sd=train_sd, ed=train_ed, sv=sv)

# converting strategy learner orders to correct format
orders_q = orders_strategy[(orders_strategy != 0).values]
orders_q['Symbol'] = symbol
orders_q['Order'] = 0
orders_q['Order'][orders_q[symbol] > 0] = 'BUY'
orders_q['Order'][orders_q[symbol] < 0] = 'SELL'
orders_q = orders_q.reset_index()
orders_q.columns.values[1] = 'Shares'
orders_q.columns.values[0] = 'Date'
orders_q['Shares'] = abs(orders_q['Shares'])
orders_q['Date'] = orders_q[['Date']].astype(str)
orders_q = orders_q.iloc[:,[0,2,3,1]]

portvals_strategy = marketsimcode.compute_portvals(orders_q, start_val = sv, commission=0, impact=impact)

########################### Benchmark ##########################################

#benchmark
start_cash = sv
bm_data = get_data(symbols = ["JPM"], dates = pd.date_range(train_sd, train_ed))
bm_data.drop(['SPY'], axis=1, inplace=True)
bm_data.head(5)
bm_pf_val = bm_data*1000
bm_pf_val["JPM"][0] = bm_pf_val["JPM"][0]*(1+ impact)
bm_pf_val.head()
initial_cash = start_cash - bm_pf_val.iloc[0].sum()
bm_pf_val["cash"]= initial_cash 
bm_pf_final = bm_pf_val.sum(axis=1).to_frame()
bm_pf_final.columns = ['Benchmark']
bm_return = bm_pf_final.iloc[-1]- bm_pf_final.iloc[0]


########################## Strategy Learner #################################

x1, = plt.plot(bm_pf_final/bm_pf_final.iloc[0], 'blue', label='Benchmark')
x3, = plt.plot(portvals_strategy/portvals_strategy[0], 'brown', label='Strategy Learner')
sd=dt.datetime(2008,1,1)

sell, = plt.plot([sd],[1],color='red', label='Short Entry')
buy, = plt.plot([sd], [1],color='green', label='Long Entry')
plt.legend(handles=[x1, x3, sell, buy], loc = 'upper left')
plt.title("Strategy Learner vs Benchmark for In-Sample Period")
    
selldates = orders_q['Date'][orders_q['Order']=='SELL']
buydates = orders_q['Date'][orders_q['Order']=='BUY']
    
for i in selldates:
    plt.axvline(x=i, ymin=0, ymax=0.1,color = 'r')

for i in buydates:
    plt.axvline(x=i, ymin=0, ymax=0.1,color = 'g')

##################### Portfolio Statistics ####################################

# Strategy Learner
cr_strategy = portvals_strategy[-1]/portvals_strategy[0] - 1
dr_strategy = (portvals_strategy/portvals_strategy.shift()) - 1
dr_strategy = dr_strategy[1:]
adr_strategy = dr_strategy.mean()
sdr_strategy = dr_strategy.std()
sr_strategy = (252**.5)*adr_strategy/sdr_strategy


# Benchmark
cr_bm = bm_pf_final.iloc[-1][0]/bm_pf_final.iloc[0][0] - 1
dr_bm = (bm_pf_final/bm_pf_final.shift()) - 1
dr_bm = dr_bm[1:]
adr_bm = dr_bm.mean()
sdr_bm = dr_bm.std()
sr_bm = (252**.5)*adr_bm/sdr_bm



