import os, csv
import talib
import yfinance as yf
import pandas
from flask import Flask, escape, request, render_template
from flask import jsonify
from patterns import candlestick_patterns
from VasuTask1 import *

app = Flask(__name__)

@app.route('/snapshot')
def snapshot():
    with open('datasets/symbols.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            data = yf.download(symbol, start="2020-01-01", end="2020-08-01")
            data.to_csv('datasets/daily/{}.csv'.format(symbol))

    return {
        "code": "success"
    }

@app.route('/candlesticks')
def index():
    pattern  = request.args.get('pattern', False)
    stocks = {}

    with open('datasets/symbols.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}

    if pattern:
        for filename in os.listdir('datasets/daily'):
            df = pandas.read_csv('datasets/daily/{}'.format(filename))
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.')[0]

            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = results.tail(1).values[0]

                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
            except Exception as e:
                print('failed on filename: ', filename)

    return render_template('index.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dfc_model')
def dfcpage():
    return render_template('dfcpage.html') 

@app.route('/dcf_model/<company>')
def dcfmodel(company):
    x = fun(company)
    return  render_template('dcf.html' ,company = company,income_statement = x["income_statement"], balance_sheet = x['balance_sheet'] , CF_forec = x['CF_forec'] , last = x['last'] , forecastString = x['forecastString'] , Revenuegrowth =  x['Revenuegrowth'] , WACC = x['WACC'] , Perpetuity = x['Perpetuity'] )

if __name__ == "__main__":
    app.run(debug=True)