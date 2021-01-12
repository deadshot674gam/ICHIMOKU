import pandas as pd 
from nsepy import get_history
from indicator_calculator import *
import datetime as dt
import indicator_calculator as ic
import pandas_datareader.data as web


# global variable 

ticker = '' # ticker symbol 
profit = [] # list for storing profit at certain



def fetchTicker():
    global ticker
    ticker = input('Enter ticker symbol : ')

def fetchTickerData():
    global ticker
    data = get_history(ticker,start=dt.date(2014,10,1),end=dt.date(2020,2,22))
    data = pd.DataFrame(data)
    data = data.drop(columns = ['Turnover', 'Trades', 'Deliverable Volume','%Deliverble'])
    return data
def senkou(red,senkouA,senkouB):
    if red:
        return senkouA
    return senkouB

def trading(data):
    global profit
    data = adding_all_indicators(data)
    b = [0]*data.shape[0]
    inv = [0]*data.shape[0]
    sel = [0]*data.shape[0]
    prof = [0]*data.shape[0]
    data['Buy'] = b
    data['Invest'] = inv
    data['Sell'] = sel
    data['Profit'] = prof
    stoploss = 0
    quantity = 20
    bought = False
    red = False
    buying_signal = False
    for i in range(51,data.shape[0]):
        curr_conv = data['Conversion Line'][i]
        curr_base = data['Base Line'][i]
        senkou_a = data['Senkou A'][i]
        senkou_b = data['Senkou B'][i]
        lag_span = data['Lagging span'][i]
        close_prev26_day = data['High'][i-26]
        curr_close = data['Close'][i]
        prev_close = data['Close'][i-1]
        
        # conditions in brief
        # for a bullish entry -
        # 1 bullish T/K crossover 
        # 2 lagging span today should be greater than close price of 26 days back
        # 3 close price should be greater than senkau a
        
        
        # when cloud is green
        if close_prev26_day<lag_span and (curr_base<curr_conv) and (prev_close<senkou_a and prev_close>senkou_b) and curr_close > senkou_a and bought == False:
            nine_period_high  = max(data['High'][i-9:i+1])
            buying_signal = True
            red = False
            # invest = quantity * buying_price
            # stoploss = senkou_b - 0.05
            # data['Buy'][i]= buying_price
            # data['Invest'][i] = invest
            # bought = True
         
        # when cloud is red
        elif close_prev26_day<lag_span  and (prev_close<senkou_b and prev_close>senkou_a) and curr_close > senkou_b and bought == False:
            nine_period_high  = max(data['High'][i-9:i+1])
            buying_signal = True
            red = True
            # invest = quantity * buying_price
            # stoploss = senkou_b - 0.05
            # data['Buy'][i]= buying_price
            # data['Invest'][i] = invest
            # bought = True
        
        if buying_signal:
            curr_high = data['High'][i]
            if curr_high>nine_period_high:
                buying_price = nine_period_high
                invest = quantity * buying_price
                stoploss = senkou(red,senkou_a,senkou_b) - 0.05
                data['Buy'][i]= buying_price
                data['Invest'][i] = invest
                red = False
                bought = True
                buying_signal = False
                
        
        if bought:
            prev_base = data['Base Line'][i-1]
            
            if curr_base> prev_base and curr_base<curr_conv:
                stoploss = curr_base
                
        if curr_close  <= stoploss and bought:
            selling_price = curr_close
            profit_value = (selling_price - buying_price)*quantity
            data['Sell'][i]= selling_price
            data['Profit'][i] = profit_value
            bought = False
    
    
    for i in range(data.shape[0]):
        curr_conv = data['Conversion Line'][i]
        curr_base = data['Base Line'][i]
        senkou_a = data['Senkou A'][i]
        senkou_b = data['Senkou B'][i]
        lag_span = data['Lagging span'][i]
        close_prev26_day = data['Low'][i-26]
        curr_close = data['Close'][i]
        prev_close = data['Close'][i-1]

        if lag_span<
    
    
    return data
        
            
if __name__ == "__main__":
    fetchTicker()
    data = fetchTickerData()
    data = trading(data)
    data.to_excel('data.xlsx')
    profit =[x for x in data['Profit'] if x!=0]
    print('Profit : ',sum(profit), 'No of Entries : ', len(profit))