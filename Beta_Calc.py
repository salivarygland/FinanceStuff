import pandas as pd
import numpy as np
import math
from pandas_datareader import data as ama
from datetime import datetime


ticker = 'JPM'
market_ticker = 'SPY'
closings = ama.DataReader(ticker, data_source='yahoo', start='2015-03-01',
                          end= datetime.date(datetime.now()))['Adj Close']
market = ama.DataReader(market_ticker, data_source='yahoo', start='2015-03-01',
                        end=datetime.date(datetime.now()))['Adj Close']


def calc_returns(data_here):
    daily_return = []
    for x in range(1, len(data_here)):
        day = np.log((data_here[x] / data_here[x-1]))
        daily_return.append(day)
    return daily_return


stock_returns = calc_returns(closings)
market_returns = calc_returns(market)


def cov(the_list: list, other_list: list):
    temp_value = 0
    mean_x = np.mean(the_list)
    mean_y = np.mean(other_list)
    count = 0
    for i in the_list:
        val = (i - mean_x) * (other_list[count]-mean_y)
        temp_value = temp_value + val
        count = count + 1
    temp_value = temp_value / len(the_list)
    return temp_value


covar = cov(stock_returns, market_returns)

print("Covariance is: ", covar)

market_var = np.var(market_returns)
print("Market Variance is: ", market_var)

Beta = (covar / market_var)
print("Beta is : ", Beta)


# CAPM Formula
new_ticker = 'SPY' #'^TNX'
tester = ama.DataReader(new_ticker, data_source='yahoo', start='2018-05-02',
                          end= datetime.date(datetime.now()))['Adj Close']
tres = ama.DataReader('^TNX', data_source='yahoo', start=datetime.date(datetime.now()),
                          end= datetime.date(datetime.now()))['Adj Close']

yuhhh = (((tester[-1])-tester[0])/tester[0])
print(tres, Beta, yuhhh)
CAPM = tres[0] + (Beta * (yuhhh - tres[0]))
print("CAPM is: ", CAPM)
