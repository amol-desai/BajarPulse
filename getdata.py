import urllib2
import copy
import re
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
from pandas.io.data import DataReader
import numpy as np

def getIndexTicker(index):
#CHANGE THIS FOR CHANGES IN BASELINE
  if index in ['"NasdaqNM"','"NMS"']:
    return "^IXIC"
  else:
    return "^GSPC"

def getParamDict(field=None):
  params = {}
  params['book value'] = "b4"
  params['eps estimate current year'] = "e7"
  #params['float shares'] = "f6" has commas in return value
  params['52 week low'] = "j"
  params['market cap'] = "j1"
  params['change from 52 week low'] = "j5"
  params['percent change from 52 week low'] = "k5"
  params['change from 200 day moving average'] = "m5"
  params['percent change from 50 day moving average'] = "m8"
  params['price per eps estimate next yr'] = "r7"
  params['short ratio'] = "s7"
  params['dividend yield'] = "y"
  params['average daily volume'] = "a2"
  params['dividend per share'] = "d"
  params['earnings per share'] = "e"
  params['eps estimate - next year'] = "e8"
  params['52 week high'] = "k"
  params['percent change from 52 week high'] = "j6"
  params['50 day moving average'] = "m3"
  params['percent change from 200 day moving average'] = "m6"
  params['name'] = "n"
  params['price per sales'] = "p5"
  params['pe ratio'] = "r"
  params['peg ratio'] = "r5"
  #params['symbol'] = "s"
  params['one year target price'] = "t8"
  params['eps estimate next quarter'] = "e9"
  params['ebitda'] = "j4"
  params['change from 52 week high'] = "k4"
  params['200 day moving average'] = "m4"
  params['change from 50 day moving average'] = "m7"
  params['price per eps estimate current year'] = "r6"
  params['stock exchange'] = "x"
  #http://www.gummy-stuff.org/Yahoo-data.htm
  if not field:
    return params
  else:
    return params[field]

def getData(symbols,paramString):
  symbolstr = ''
  for symbol in symbols:
    symbolstr = symbolstr+'+'+symbol
  url = 'http://finance.yahoo.com/d/?s=%s&f=%s' %(symbolstr,paramString)
  #print url
  return urllib2.urlopen(url).read().strip()

def reformat(value):
  #name = re.compile('^[a-z].*[a-z]$',flags=re.IGNORECASE)
  milbiltril = re.compile('^([0-9]*|[0-9]*\.[0-9]*)(M|B|T)$',flags=re.IGNORECASE)
  perc = re.compile('^(\+|\-|)([0-9]*|[0-9]*\.[0-9]*)(%)$')
  num = re.compile('^([0-9]*|[0-9]*\.[0-9]*)$')
  num2 = re.compile('^(\+|\-|)([0-9]*|[0-9]*\.[0-9]*)$')
  
  m = milbiltril.search(value)
  mult = 0
  if m:
    if m.group(2) == 'M' or m.group(2) == 'm':
      mult = 1000000
    elif m.group(2) == 'B' or m.group(2) == 'b':
      mult = 1000000000
    elif m.group(2) == 'T' or m.group(2) == 't':
      mult = 1000000000000
    return float(m.group(1))*mult

  m = perc.search(value)
  if m:
    if m.group(1) == '-':
      return round(float(m.group(1)+m.group(2))/100,4)
    else:
      return round(float(m.group(2))/100,4)

  m = num.search(value)
  if m:
    return round(float(m.group(0)),4)

  m = num2.search(value)
  if m:
    return round(float(m.group(2)),4)

  return value
  
def get_monthlyData(symbol):
  params = getParamDict()
  #data = copy.deepcopy(params)
  data = params
  values = getData([symbol],''.join(params.values())).strip().split(',')
  for i,key in enumerate(data.keys()):
    data[key] = reformat(values[i])
    #data[key] = getData(symbol,data[key]).strip()
  data['date'] = dt.date(dt.now()).strftime("%Y %m %d")
  return data

def get_history(symbols,start_date,end_date=dt.now()):
  dfarr = []
  for symbol in symbols:
      dfarr.append(DataReader(symbol,"yahoo",start=start_date,end=end_date))
  return pd.concat(dfarr,keys=symbols)
  
def get_dividend_history(symbols,start_date,end_date=dt.today().date()):
#https://code.google.com/p/yahoo-finance-managed/wiki/csvHistQuotesDownload  
    dfarr = []
    try:
        #print symbols,start_date,end_date
        url = 'http://ichart.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=v&ignore=.csv' %(symbols,
                                                                                                       start_date.month,start_date.day,start_date.year,
                                                                                                       end_date.month,end_date.day,end_date.year)
        #print url
        return pd.DataFrame.from_csv(url)
    except urllib2.HTTPError:
        return pd.DataFrame(columns=['Dividends'])
    #except:
        #for symbol in symbols:
        #    print symbol,start_date,end_date
         #   dfarr.append(get_dividend_history(symbol,start_date,end_date))
        #return pd.concat(dfarr,keys=symbols)