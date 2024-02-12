# import mplfinance as mpf
# import pandas as pd
import datetime
# from moeximporter import MoexImporter, MoexSecurity, MoexCandlePeriods
from parse import parse, create_csv
from data_get import isForeign
from TradeMethods import razn, into_data_elem_ru, into_data_elem_fg, binary_search, umnozh, selling
from TheStrategy import we_are_so_back, it_is_so_over, buying



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

def coefficient(company_name):
    if not isForeign(company_name):
        return lot[company_name]
    return 1

def main_strat(comp, period, date_start, date_end, money):  #comp - 'название фирмы'; date_start/end - массивы с датами, [г, м, д]; period - 1day и проч

    def merge(array1, array2):
        returner = []
        first = 0
        second = 0
        while first < len(array1) and second < len(array2):
            if array1[first][0] <= array2[second][0]:
                array1[first].append('')
                returner.append(array1[first])
                first += 1
            else:
                array2[second].append(str(selling[second][2] / coefficient(comp)))
                returner.append(array2[second])
                second += 1
        if first == len(array1):
            for elem in range(second, len(array2)):
                array2[second].append(str(selling[second][2] / coefficient(comp)))
                returner.append(array2[second])
        else:
            for elem in range(second, len(array1)):
                array1[first].append('')
                returner.append(array1[first])
        return returner

    tmp1 = datetime.datetime(year=date_start[0], month=date_start[1], day=date_start[2])
    sr_line_length = 200

    money_start = money
    data = []  # Массив Line

    p = 280
    if period == '1hour':
        p = 15
    elif period == '1week':
        p *= 7
    elif period == '1month':
        p *= 30

    if not (isForeign(comp)):
        c = lot[comp]

        tmp1 = tmp1 - datetime.timedelta(days=p)
        tmp1 = [tmp1.year, tmp1.month, tmp1.day]
        create_csv(comp, period, tmp1, date_start)
        company = parse(comp)

        sr_line_length = len(company) - 1
        last_date = company[sr_line_length]
        create_csv(comp, period, tmp1, date_end)
        company = parse(comp)  # open, close, high, low, value, quantity, end;

        for inex in range(1, sr_line_length + 1):
            data.append(umnozh(into_data_elem_ru(company[inex][0]), c)) #  (+ ',', str(inex))
    else:
        tmp1 = tmp1 - datetime.timedelta(days=p)
        tmp1 = [tmp1.year, tmp1.month, tmp1.day]
        create_csv(comp, period, tmp1, date_start)
        company = parse(comp)

        sr_line_length = len(company) - 1
        last_date = company[sr_line_length]
        create_csv(comp, period, tmp1, date_end)
        company = parse(comp)

        for inex in range(1, sr_line_length + 1):
            data.append(into_data_elem_fg(company[inex][0] + ',' + str(inex-1)))  # (+ ',', str(inex))

    buying_string = []
    selling_string = []
    buying_return = []

    # if (last_date == data[st_line_length
    for current in range(sr_line_length + 1, len(company)):
        if not (isForeign(comp)):
            data.append(umnozh(into_data_elem_ru(company[current][0]), c))
        else:
            data.append(into_data_elem_fg(company[current][0] + ',' + str(current-1)))
        if we_are_so_back(data, sr_line_length) and money >= data[current-1].Close:

            tmp = 1.0003 * data[current-1].Close * binary_search(money, data[current-1].Close)

            buying.data.append([current-(sr_line_length + 1), data[current-1].Low, binary_search(money, data[current-1].Close)])
            buying_return.append([current - (sr_line_length + 1), data[current - 1].Low])
            buying_string.append([razn(data[current-1].Date, str(current - sr_line_length + 1)), -tmp])

            money -= tmp

        elif it_is_so_over(data) and buying.avg_elem():

            tmp = 0.9997 * data[current-1].Close * buying.amount()

            selling.append([current - (sr_line_length + 1), data[current-1].High, data[current-1].Close - buying.avg_elem()])
            selling_string.append([razn(data[current-1].Date, str(current - sr_line_length + 1)), tmp])

            money += tmp
            buying.clear()

    if buying.avg_elem():

        tmp = 0.9997 * data[len(company) - 1 - 1].Close * buying.amount()

        selling.append([len(company)-1 - (sr_line_length + 1), data[len(company)-1 - 1].High, data[len(company)-1 - 1].Close - buying.avg_elem()])
        selling_string.append([razn(data[len(company)-1 - 1].Date, str(len(company)-1 - sr_line_length + 1)), tmp])

        money += tmp
        buying.clear()

    returner = merge(buying_string, selling_string)

    if (len(returner)):
        return [returner, buying_return, selling, (money-money_start)/money_start * 100]
    else:
        return 'Не фиксируем прибыль'


# company_name = 'AMZN'
# period = '1week'
# date_start = [2022, 1, 1]
# date_end = [2023, 5, 1]
# # create_csv(company_name, period, date_start, date_end)
# returner = main_strat(company_name, period, date_start, date_end, 100000)
# if returner == 'Не фиксируем прибыль':
#     print(returner)
# else:
#     print(returner[3])
#     plot(company_name, returner[1], returner[2], period, date_start, date_end)

# json
#русские - проверяй, не больше ли при первом создании csv последняя дата даты старта