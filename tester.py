import getdata
import portfolio
import analyzer
from datetime import datetime as dt

stocks_n_transactions = {'AAPL': 
							{
							1: {'price': 120, 'ttype': 'B', 'num': 5, 'date': '2015/05/01'},
							2: {'price': 125, 'ttype': 'B', 'num': 5, 'date': '2015/06/01'},
							3: {'price': 100, 'ttype': 'S', 'num': 5, 'date': '2015/06/15'}
							},
						'FB':
							{
							1: {'price': 65, 'ttype': 'B', 'num': 100, 'date': '2014/06/01'},
							},
						'MRO':
							{
							1: {'price': 25, 'ttype': 'B', 'num': 100, 'date': '2014/06/01'},
							2: {'price': 27, 'ttype': 'S', 'num': 50, 'date': '2015/06/01'},
							}
						}
def createPortfolio():
	a = []
	for ticker in stocks_n_transactions:
		s = portfolio.Stock(ticker)
		for k in stocks_n_transactions[ticker]:
			t = stocks_n_transactions[ticker][k]
			s.addTransaction(t['price'],t['ttype'],t['num'],t['date'])
		a.append(s)
	p = portfolio.Portfolio('Test')
	for stock in a:
		p.addStock(stock)
	return p
	
#print analyzer.construct_ranking_table(createPortfolio(),lookbackDays=30,oldTable=None,enddate=dt.today().date(),index=None,silent=False)

#def createPortfolioFromCsv(csv):
	