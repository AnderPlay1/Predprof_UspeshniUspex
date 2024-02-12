from TradeMethods import Massive
buying = Massive()


def sr_elem(data, el, delta):
    midle = 0
    for i in range (el - (delta-1), el + 1):
        midle += data[i].Close
    return midle/delta


def IsWhite(line_):
    if line_.Open < line_.Close:
        return 1
    return 0


def three_white_soldiers(data, number):    #number уже сдвинут, number - номер третьего солдата
    if ((data[number - 1].High > data[number - 2].High and
         data[number - 1].Low > data[number - 2].Low > data[number - 1].Low and
         data[number].High > data[number - 1].High and
         data[number].Low > data[number - 1].Low > data[number].Low) and
        (IsWhite(data[number]) and IsWhite(data[number - 1]) and IsWhite(data[number - 2]))):
        return 1
    return 0


def local_min(u, E, data):
    for elem in range(1, E+1):
        if not (data[u].Close <= data[u+elem].Close and data[u].Close <= data[u-elem].Close):
             return 0
    return 1


def local_max(u, E, data):
    for elem in range(1, E+1):
        if not (data[u].Close >= data[u+elem].Close and data[u].Close >= data[u-elem].Close):
             return 0
    return 1


def trend(u, data):

    data_local_min = []
    data_local_max = []

    E = 1
    i = u - E
    while not (len(data_local_min) >= 2 and len(data_local_max) >= 2):
        if local_min(i, E, data):
            data_local_min.append(i)
        elif local_max(i, E, data):
            data_local_max.append(i)
        i -= 1

    if data_local_min[0] >= data_local_min[1] and data_local_max[0] >= data_local_max[1]:
        return 1
    elif data_local_min[0] <= data_local_min[1] and data_local_max[0] <= data_local_max[1]:
        return -1
    else:
        return 0


def three_descensings_ascensions(data, number):    #number - индекс первого     1 - продолжение тренда до number
    if not IsWhite(data[number]):
        if not (data[number].High > data[number+1].High and data[number].Low < data[number+1].Low):
            return 0
        for i in range(2, 6):
            if IsWhite(data[number+i]):
                if not (data[number].High > data[number+i].High and data[number].Low < data[number+i].Low):
                    return 0
                if not (data[number + i].High > data[number + i - 1].High > data[number + i].Low > data[number + i - 1].Low):
                    return 0
            elif i > 2:
                return trend(number, data)
            return 0
    if IsWhite(data[number]):
        if not (data[number].High > data[number + 1].High and data[number].Low < data[number + 1].Low):
            return 0
        for i in range(2, 6):
            if not (IsWhite(data[number+i])):
                if not (data[number].High > data[number + i].High and data[number].Low < data[number + i].Low):
                    return 0
                if not (data[number + i].High > data[number + i - 1].High > data[number + i].Low > data[number + i - 1].Low):
                    return 0
            elif i > 2:
                return trend(number, data)
            return 0


def counter(data, day):
    n = len(data)
    c = 7
    minimum = 1e9
    maximum = -1e9
    EMA = (data[day - c].Low + data[day - c].High) / 2
    a = 2 / (c + 1)
    for j in range(day - c + 1, day + 1):
        minimum = min(minimum, data[j].Low)
        maximum = max(maximum, data[j].High)
        EMA = a * (data[j].Low + data[j].High) / 2 + (1 - a) * EMA
    temp = (data[day].Close - minimum) / (maximum - minimum) * 100
    return [temp, EMA]


def strat_to_sell(data, day):
    if day < 8:
        return 0
    cur = counter(data, day)
    prev = counter(data, day - 1)
    if cur[0] < cur[1] and prev[0] > prev[1]:
        return 1
    return 0


def we_are_so_back(data, sr_line_length):
    criteria = 0
    if three_white_soldiers(data, len(data)-1):
        criteria += 1
    if data[len(data)-1].Close < sr_elem(data, len(data)-1, sr_line_length):
        criteria += 1
    if trend(len(data) - 1, data) == 1:
        criteria += 1
    if trend(len(data) - 1, data) == 1:
        for elem in range(4, 7):
            if three_descensings_ascensions(data, len(data)-1-elem):
                criteria += 1
                break

    if criteria >= 2:
        return 1
    return 0


def it_is_so_over(data):
    criteria = 0
    E = 10
    if (1 + E/100)*buying.avg_elem() < data[len(data)-1].Close or (1-E/100)*buying.avg_elem() > data[len(data)-1].Close:
        criteria += 1
    if strat_to_sell(data, len(data) - 1):
        criteria += 1

    if criteria >= 1:
        return 1
    return 0
