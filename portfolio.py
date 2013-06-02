import numpy as np
from datetime import datetime as dt
import getdata

class Portfolio(object):
    def __init__(self,name):
        self.stocks = np.asarray([])
        self.name = str(name)
    def getStocksInPortfolio(self):
        return self.stocks
    def getTickersInPortfolio(self):
        toret = []
        for stock in self.stocks:
            toret.append(stock.ticker)
        return toret
    def addStockToPortfolio(self,Stock):
        if Stock.ticker in self.getTickersInPortfolio():
            print "ERROR: This ticker already exists in this portfolio. You cannot add it again. Add a transaction instead."
            return
        else:
            print "Added "+Stock.ticker+" to portfolio" 
            self.stocks = np.append(self.stocks,Stock)
    def getHistoryForPortfolio(self,start_date):
        tickers = []
        for stock in self.stocks:
            ticker = stock.ticker
            tickers.append(ticker)
            index = getdata.getIndexTicker(getdata.getData([ticker],
                                getdata.getParamDict('stock exchange')))
            if index not in tickers:
                tickers.append(index)
        return getdata.get_history(tickers,start_date)

class Stock(object):
    def __init__(self,ticker):
        self.ticker = ticker
        self.shares_owned = 0
        self.transactions = []
        self.investment = 0
        print "Created stock object "+self.ticker
    def addTransaction(self,price,ttype='B',num=0,date='1990/01/30'):
        transaction = {}
        if (ttype != 'B') & (ttype != 'S'):
            print "ERROR:Invalid Transaction Type"
            return
        elif ttype == 'B':
            ttype = 'Bought'
            self.shares_owned += num
            self.investment += num*price
        elif ttype == 'S':
            if self.shares_owned >= num:
                self.shares_owned -= num
                self.investment -= num*price
            else:
                print "ERROR: You couldn't have sold more shares than you owned"
                return
            ttype = 'Sold'
        if num == 0:
            print "ERROR:Num of shares in transaction must be > 0"
            return
        else:
            transaction['Number'] = num
        transaction['Price'] = price
        transaction['Date'] = getDateInDatetimeFormat(date)
        transaction['Type'] = ttype
        self.transactions = np.append(self.transactions,transaction)
        print "Added Transaction to "+self.ticker+": "+ttype+" "+str(num)+" on "+str(date)
    def getTransactions(self,date=None,ttype=None):
        toret = np.asarray([])
        if not date:
            return self.transactions
        elif not ttype:
            for transaction in self.transactions:
                if transaction['Date'] == getDateInDatetimeFormat(date):
                    toret = np.append(toret,transaction)
        else:
            if (ttype != 'B') & (ttype != 'S'):
                print "ERROR:Invalid Transaction Type"
                return
            elif ttype == 'B':
                ttype = 'Bought'
            elif ttype == 'S':
                ttype = 'Sold'
            for transaction in self.transactions:
                if ((transaction['Date'] == getDateInDatetimeFormat(date))
                 & (transaction['Type'] == ttype)):
                    toret = np.append(toret,transaction)
        return toret
    def getSharesOwned(self):
        return self.shares_owned
    def addDividends(self,num):
        return self.shares_owned+num

def getDateInDatetimeFormat(date='1990/01/30'):
    if type(date) != dt:
        date_components = date.split('/')
        toret = dt(int(date_components[0]),
               int(date_components[1]),
               int(date_components[2]))
    else:
        toret = date
    return toret
