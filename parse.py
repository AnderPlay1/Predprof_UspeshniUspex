import csv
import data_get
import pandas as pd


class Line:
    Open = 0
    Close = 0
    High = 0
    Low = 0
    Value = 0
    Quantity = 0
    Date = 0


def parse(filename):
    file = filename + ".csv"
    file = open(file, encoding="utf8")
    reader = csv.reader(file, delimiter=";", quotechar='"')
    company=[]
    for line in reader:
        company.append(line)
    file.close()
    return company


def ParseToTxt(filecsv, filetxt):
    CsvFileName = filecsv + ".csv"
    TxtFileName = filetxt + ".txt"
    with open(CsvFileName, 'r') as f_in, open(TxtFileName, 'w') as f_out:
        content = f_in.read().replace(',', ' ')
        f_out.write(content)


def ParseToDataFrame(filecsv):
    df = pd.read_csv(filecsv)
    return df


def create_csv(company_name, period, dateFrom, dateTo):
    company = company_name + '.csv'
    df = data_get.dataGet(period, dateFrom, dateTo, company_name)
    df.to_csv(company, index=False)
    return df

