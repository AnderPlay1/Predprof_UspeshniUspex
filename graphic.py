import mplfinance as mpf
from data_get import isForeign
import numpy as np
import pandas as pd
from parse import create_csv
from TradeSterategy import  main_strat
lot = { 'AFLT': 10,
        'VTBR': 10000,
        'LKOH': 1,
        'SBER': 10,
        'GAZP': 10,
        'MTSS': 10,
        'ROSN': 1,
        'SVCB': 100,
        'YNDX': 1,
        'FEES': 10000}


def plot(company_name, buing, selling, period, date_start, date_end):
    companyPeriod = company_name + period
    df = create_csv(company_name, period, date_start, date_end)
    buy = [np.NAN] * len(df)
    sell = [np.NAN] * len(df)
    c = 1
    if not isForeign(company_name):
        c = lot[company_name]
    for element in buing:
        buy[element[0]] = (element[1]/c) * 1.0001
    for element in selling:
        sell[element[0]] = (element[1]/c) * 9.9999
    filename = companyPeriod + '.jpg'
    save = dict(fname=filename)
    apd = [mpf.make_addplot(buy, type='scatter', marker='^', color='r'),
           mpf.make_addplot(sell, type='scatter', marker='v', color='g')]
    mpf.plot(df, type="candle", style='yahoo', addplot=apd, savefig=save)

# dateStart = [2023, 1, 1]
# dateEnd = [2023, 1, 9]
# returner = main_strat("BTC-USD", "1hour", dateStart, dateEnd, 100000)
# plot ("BTC-USD", returner[1], returner[2], "1hour", dateStart, dateEnd)