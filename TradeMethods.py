from parse import Line


class Massive:
    data = []

    def avg_elem(self):
        answ = 0
        for elem in Massive.data:
            answ += elem[1]
        return answ / (len(Massive.data) + int(not (len(Massive.data))))

    def clear(self):
        Massive.data.clear()

    def amount(self):
        answ = 0
        for elem in Massive.data:
            answ += elem[2]
        return answ


selling = []


def into_data_elem_ru(str):
    data_elem = str.split(',')
    returner = Line()
    returner.Open = float(data_elem[0])
    returner.Close = float(data_elem[1])
    returner.High = float(data_elem[2])
    returner.Low = float(data_elem[3])
    returner.Date = data_elem[6]
    return returner


def into_data_elem_fg(str):
    data_elem = str.split(',')
    returner = Line()
    returner.Open = float(data_elem[0])
    returner.High = float(data_elem[1])
    returner.Low = float(data_elem[2])
    returner.Close = float(data_elem[3])
    returner.Date = data_elem[6]
    return returner


def binary_search(money, price):
    l = -1
    r = money // price + 1
    while (r - l > 1):
        mid = l + (r - l) // 2
        if 2 * price * mid >= money:
            r = mid
        else:
            l = mid
    return r


def umnozh(a, c):
    a.Close = a.Close * c
    a.Open = a.Open * c
    a.High = a.High * c
    a.Low = a.Low * c
    return a


def razn(string1, string2):
    if len(string1) == 19:
        return string1
    return string2


def consumes(candle1, candle2):
    if (candle1.Close - candle1.Open) * (candle2.Close - candle2.Open) > 0:
        return 0
    if candle2.Close > candle1.High and candle1.Low > candle2.Open:
        return 1


def kostil(a):
    if a:
        return a
    return 1


# def three_black_crows(data, number):
#     if ((data[number - 1].High < data[number - 2].High and
#         data[number - 1].High > data[number].High and
#         data[number - 1].Low < data[number - 2].Low and
#         data[number - 1].Low > data[number].Low) and
#         (not IsWhite(data[number]) and not IsWhite(data[number - 1]) and not IsWhite(data[number - 2]))):
#         return 1
#     return 0

