from datetime import date
from moeximporter import MoexImporter, MoexSecurity, MoexCandlePeriods
import json
import yfinance as yf


def dataGet(period, dateFrom, dateTo, company_name):
    if isForeign(company_name):
        df = YahooData(period, dateFrom, dateTo, company_name)
    else:
        df = MoexData(period, dateFrom, dateTo, company_name)
    return df


def isForeign(company_name):
    json_file = open('data_base.json')
    f = json_file.read()
    data = json.loads(f)
    if company_name in data[0]['ru_companies']:
        return 0
    else:
        return 1


def MoexData(period, dateFrom, dateTo, company_name):
    mi = MoexImporter()
    sec = MoexSecurity(company_name, mi)
    my_interval = {'1hour': MoexCandlePeriods.Period1Hour,
                   '1month': MoexCandlePeriods.Period1Month,
                   '1week': MoexCandlePeriods.Period1Week,
                   '1day': MoexCandlePeriods.Period1Day}
    df = sec.getCandleQuotesAsDataFrame(date(dateFrom[0], dateFrom[1], dateFrom[2]), date(dateTo[0], dateTo[1], dateTo[2]),
                                                interval=my_interval[period])
    return df


def YahooData(period, dateFrom, dateTo, company_name):
    my_interval = {"1hour": '1h',
                   "1month": '1mo',
                   "1week": '1wk',
                   "1day": '1d'}
    df = yf.download(company_name, start=date(dateFrom[0],dateFrom[1],dateFrom[2]), end=date(dateTo[0],dateTo[1],dateTo[2]),
                                                interval=my_interval[period])
    return df
