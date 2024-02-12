from shutil import move
import os
from flask import Flask, render_template, request
from TradeSterategy import main_strat
import codecs
from graphic import plot
import json
from mystrategy import my_strategy

def strategy(company_name):
    data_file = open('data_base.json')
    f = data_file.read()
    data = json.loads(f)
    period = data[1]["period"]
    dateStart = data[1]["dateStart"]
    dateEnd = data[1]["dateEnd"]
    str = company_name + period + '.jpg'
    path = "static/img/" + str
    if os.path.isfile(path):
        move(path, str)
        os.remove(str)
    # запускаем страту
    returner = main_strat(company_name, period, dateStart, dateEnd, 100000)
    if returner != 'Не фиксируем прибыль':
        plot(company_name, returner[1], returner[2], period, dateStart, dateEnd)
        move(str, path)
    return returner

def description():
    file = codecs.open('comp_description.txt', 'r', 'utf_8_sig')
    s = file.read()
    file.close()
    company_desc = s.split("\r\n")
    company_description = {
        "AFLT": company_desc[0],
        "VTBR": company_desc[1],
        "LKOH": company_desc[2],
        "SBER": company_desc[3],
        "GAZP": company_desc[4],
        "MTSS": company_desc[5],
        "ROSN": company_desc[6],
        "SVCB": company_desc[7],
        "YNDX": company_desc[8],
        "FEES": company_desc[9],
        "AMZN": company_desc[10],
        "NVDA": company_desc[11],
        "AAPL": company_desc[12],
        "AMD": company_desc[13],
        "SPOT": company_desc[14],
        "DOGE-USD": " ",
        "BTC-USD": " ",
        "ETH-USD": " "
    }
    return company_description

app = Flask(__name__)

@app.route("/") 
@app.route("/index")
def index():
    with open('data_base.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    kwargs = dict()
    kwargs['username'] = data[3]['name']
    return render_template("home.html",  **kwargs)


@app.route("/sign_in", methods=['POST', 'GET'])
def sign_in():
    with open('data_base.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    kwargs = dict()
    if request.method == 'GET':
        return render_template("sign_in.html")
    elif request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        kwargs['username'] = name
        data[3]['name'] = name
        with open('data_base.json', 'w') as file:
            json.dump(data, file)
        return render_template("home.html", **kwargs)

@app.route("/analytics/<company_name>/", methods=['POST', 'GET'])
def analytics(company_name):
    with open('data_base.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    company_description = description()
    if request.method == 'GET':
        returner = strategy(company_name)
        kwargs = dict()
        if returner != 'Не фиксируем прибыль':
            kwargs["companyPeriod"] = company_name + data[1]["period"]
        else:
            returner = [[0, 0, 0, 0]], [[0, 0, 0, 0]]
            kwargs["companyPeriod"] = 'error'
        kwargs["strategy"] = returner
        kwargs["name"] = company_name
        kwargs["company_description"] = company_description[company_name]
        kwargs["comps"] = data[0]["company_list"]
        kwargs['username'] = data[3]['name']
        return render_template("html.html", **kwargs)
    elif request.method == 'POST':
        print(request.form)
        period = request.form['class']
        if " " in period:
            temp = period.split(" ")
            period = temp[0] + temp[1]
        dateStart = request.form['start'].split('-')
        dateEnd = request.form['finish'].split('-')
        method = request.form['strat']
        if method == 'mystrategy.py':
            data[2]["std_strategy"] = 0
            data[2]["strategy_name"] = request.method['strat']
        else:
            data[2]["std_strategy"] = 1
        for i in range(0,len(dateStart)):
            dateStart[i] = int(dateStart[i])
            dateEnd[i] = int(dateEnd[i])
        data[1]["dateStart"] = dateStart
        data[1]["dateEnd"] = dateEnd
        print(dateStart, dateEnd)
        data[1]["period"] = period
        with open('data_base.json', 'w') as file:
            json.dump(data, file)
        kwargs_temp = dict()
        kwargs_temp['username'] = data[3]['name']
        return render_template("back.html", **kwargs_temp)


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")

