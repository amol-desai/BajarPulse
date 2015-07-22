from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import getdata

class Portfolio(object):
    def __init__(self,name):
        self.stocks = []
        self.name = str(name)
    def getStocks(self):
        return self.stocks
    def getTickers(self):
        toret = []
        for stock in self.stocks:
            toret.append(stock.ticker)
        return toret
    def addStock(self,Stock):
        if Stock.ticker in self.getTickers():
			print "ERROR: This ticker already exists in this portfolio. You cannot add it again. Add a transaction instead."
        else:
			self.stocks.append(Stock)
			print "Added "+Stock.ticker+" to portfolio" 
	def deleteStock(self,ticker):
		tickers_in_portfolio = self.getTickers()
		if ticker not in tickers_in_portfolio:
			print "ERROR: This Stock doesn't exist in this portfolio. Nothing to Remove"
		else:
			self.stocks.pop(tickers_in_portfolio.index(ticker))
    def getHistory(self,start_date):
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
        self.dividend_balance = 0
        print "Created stock object "+self.ticker
    def updateSharesOwned(self,end_date):
        try:
            latest_transaction_date =  max([t['Date'] for t in self.transactions])
        except ValueError:
            latest_transaction_date = dt.today().date()
        dividends = getdata.get_dividend_history(self.ticker,latest_transaction_date-relativedelta(days=7),end_date)
        dividends['Date'] = dividends.index
        dividends.apply(lambda row: self.addTransaction(row['Dividends'],'D',
                                                        int(row['Dividends']*self.shares_owned/(getdata.get_history([self.ticker],
                                                                                                                    (row['Date']+pd.DateOffset(days=2)),
                                                                                                                    (row['Date']+pd.DateOffset(days=7)))
                                                                                                                    [-1:]['Close'].values[0])),
                                                        row['Date']+pd.DateOffset(days=7)),axis=1)
        return
    def addTransaction(self,price,ttype='B',num=0,date='1990/01/30'):
        if ttype != 'D':
            self.updateSharesOwned(getDateInDatetimeFormat(date))
        #if we are adding non-dividend transaction, make sure the transaction list is up to date
        transaction_number = len(self.transactions)+1
        transaction = {}
        transaction['id'] = transaction_number
        if ttype not in ['S','B','D']:
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
        elif ttype == 'D':
            ttype = 'Dividend'
            self.shares_owned += num
        if num == 0:
            print "ERROR:Num of shares in transaction must be > 0"
            return
        else:
            transaction['Number'] = num
        transaction['Price'] = price
        transaction['Date'] = getDateInDatetimeFormat(date)
        transaction['Type'] = ttype
        self.transactions.append(transaction)
        try: 
            datestr = str(date.year)+'/'+str(date.month)+'/'+str(date.day)
        except:
            datestr = date
        print "Added Transaction to "+self.ticker+": "+ttype+" "+str(num)+" on "+str(datestr)
        
    def deleteTransaction(self,id):
        try:
            toremove = self.transactions[id-1]
            self.transactions.pop(id-1)
        except IndexError:
            print "Nothing to Remove"
        print "Deleted Transaction From "+self.ticker+": "+toremove['Type']+" "+str(toremove['Number'])+" on "+str(toremove['Date']) 
    
    def getTransaction(self,date=None,ttype=None):
        toret = []
        if not date:
            return self.transactions
        elif not ttype:
            for transaction in self.transactions:
                if transaction['Date'] == getDateInDatetimeFormat(date):
                    toret.append(transaction)
        else:
            if ttype not in ['S','B','D']:
                print "ERROR:Invalid Transaction Type"
                return
            elif ttype == 'B':
                ttype = 'Bought'
            elif ttype == 'S':
                ttype = 'Sold'
            elif ttype == 'D':
                ttype = 'Dividend'
            for transaction in self.transactions:
                if ((transaction['Date'] == getDateInDatetimeFormat(date))
                 & (transaction['Type'] == ttype)):
                    toret.append(transaction)
        return toret
    def getSharesOwned(self):
        self.updateSharesOwned(dt.today().date())
        return self.shares_owned
	def getHistory(self,start_date):
		return getdata.get_history([self.ticker],start_date)

def getDateInDatetimeFormat(date='1990/01/30'):
    try:
        date_components = date.split('/')
        toret = dt(int(date_components[0]),
               int(date_components[1]),
               int(date_components[2])).date()
    except:
        toret = date.date()
    return toret
