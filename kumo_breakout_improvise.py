import pandas as pd 
from nsepy import get_history
from indicator_calculator import *
import datetime as dt
import indicator_calculator as ic
import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt

# global variable 

ticker = '' # ticker symbol 
profit = [] # list for storing profit at certain



def fetchTicker():
    global ticker
    ticker = input('Enter ticker symbol : ')

def fetchTickerData():
    global ticker
    data = get_history(ticker,start=dt.date(2014,10,1),end=dt.date(2020,2,20))
    data = pd.DataFrame(data)
    data = data.drop(columns = ['Volume','Turnover', 'Trades', 'Deliverable Volume','%Deliverble'])
    return data

def senkouBull(red,senkouA,senkouB):
    if red:
        return senkouA
    else:
        return senkouB

def senkouBear(red,senkouA,senkouB):
    if red:
        return senkouB
    else:
        return senkouA

def inrange(value,high,low):
    
    if value<=high and value>=low:
        # print(high,'\n',low,'\n',value)
        return True
    return False





def trading(data):
    global profit
    data = ic.adding_all_indicators(data)
    b = [0.0]*data.shape[0]
    inv = [0.0]*data.shape[0]
    sel = [0.0]*data.shape[0]
    prof = [0.0]*data.shape[0]
    data['Buy'] = b
    data['Invest'] = inv
    data['Sell'] = sel
    data['Profit'] = prof
    stoploss = 0
    quantity = 20
    bought = False
    red = False
    buying_signal = False
    # red = False
    sold = False
    selling_signal = False
    # stoploss = 0
    
    
    for i in range(51,data.shape[0]-28):
        curr_conv = data['Conversion Line'][i]
        curr_base = data['Base Line'][i]
        prev_senkou_a = data['Senkou A'][i-1]
        prev_senkou_b = data['Senkou B'][i-1]
        senkou_a = data['Senkou A'][i]
        senkou_b = data['Senkou B'][i]
        lag_span = data['Lagging span'][i]
        high_prev26_day = data['High'][i-25]
        curr_close = data['Close'][i]
        prev_close = data['Close'][i-1]
        # low_prev26_day = data['Low'][i-25]
        future_senkou_A = data['Senkou A'][i+26]
        future_senkou_B = data['Senkou B'][i+26]
        
        # conditions in brief
        # for a bullish entry -
        # 1 bullish T/K crossover 
        # 2 lagging span today should be greater than close price of 26 days back
        # 3 close price should be greater than senkau a
        
        if bought == False:
            # bullish entries
            if (high_prev26_day<lag_span) and (future_senkou_A>future_senkou_B):
                
                if curr_conv>curr_base:
                    # green cloud breakout normal
                    if ((prev_close<prev_senkou_a) and (prev_close>prev_senkou_b)) and ((curr_close>senkou_a) and (curr_close>senkou_b)):
                        nine_period_high  = float(np.amax(data['High'][i-8:i+1]))
                        # print('Above Green cloud bullish')
                        buying_signal = True
                        red = False 

                    # green cloud breakout special
                    if ((prev_close<prev_senkou_a)and (prev_close<prev_senkou_b)) and ((curr_close>senkou_a) and (curr_close>senkou_b)):
                        nine_period_high  = float(np.amax(data['High'][i-8:i+1]))
                        # print('Above Green cloud bullish')
                        buying_signal = True
                        red = False
                    
                    # red cloud breakout normal
                    if ((prev_close<prev_senkou_b)and (prev_close>prev_senkou_a)) and ((curr_close>senkou_b) and (curr_close>senkou_a)):
                        nine_period_high  = float(np.amax(data['High'][i-8:i+1]))
                        # print('Above Green cloud bullish')
                        buying_signal = True
                        red = True
                    
                    # red cloud breakout special
                    if ((prev_close<prev_senkou_b) and (prev_close<prev_senkou_a)) and ((curr_close>senkou_b) and (curr_close>senkou_a)):
                        nine_period_high  = float(np.amax(data['High'][i-8:i+1]))
                        # print('Above Green cloud bullish')
                        buying_signal = True
                        red = True
                    
        
        
        if buying_signal:
            curr_high = data['High'][i]
            if curr_high>nine_period_high:
                bought = True
                buying_signal = False
                buying_price = nine_period_high + 0.05
                invest = quantity * buying_price
                red = False
                data['Buy'][i]= buying_price
                data['Invest'][i] = invest
                
                
        
        if bought:
            curr_high = data['High'][i]
            curr_low = data['Low'][i]
            low_prev26_day = data['Low'][i-1]
            lag_span = data['Lagging span'][i]
            
            if lag_span<low_prev26_day:
                selling_price = curr_close            
                profit_value = float(selling_price - buying_price)*quantity
                profit.append(profit_value)
                data['Sell'][i]= selling_price
                data['Profit'][i] = profit_value
                bought = False
    
        #print(i+2,' ', bought)
                

        
        

    red = False
    sold = False
    selling_signal = False
    stoploss = 0
    
    
    for i in range(51,data.shape[0]-28):
        curr_conv = data['Conversion Line'][i]
        curr_base = data['Base Line'][i]
        prev_senkou_a = data['Senkou A'][i-1]
        prev_senkou_b = data['Senkou B'][i-1]
        senkou_a = data['Senkou A'][i]
        senkou_b = data['Senkou B'][i]
        lag_span = data['Lagging span'][i]
        low_prev26_day = data['Low'][i-26]
        curr_close = data['Close'][i]
        prev_close = data['Close'][i-1]
        future_senkou_A = data['Senkou A'][i+26]
        future_senkou_B = data['Senkou B'][i+26]
    
        if sold == False:
            #bearish entries
            if (lag_span<low_prev26_day) and (future_senkou_B>future_senkou_A):
                
                if curr_base>curr_conv:
                    
                    # green cloud breakout normal 
                    if((prev_close<prev_senkou_a)and (prev_close>prev_senkou_b)) and ((curr_close<senkou_b)and (curr_close<senkou_a)):
                        nine_period_low = float(np.amin(data['Low'][i-8:i+1]))
                        selling_signal = True
                        red = False
                        
                    # green cloud breakout special
                    if((prev_close>prev_senkou_a)and (prev_close>prev_senkou_b)) and ((curr_close<senkou_b) and (curr_close<senkou_a)):
                        nine_period_low = float(np.amin(data['Low'][i-8:i+1]))
                        selling_signal = True
                        red = False
                        
                    # red cloud breakout normal
                    if((prev_close<prev_senkou_b) and (prev_close>prev_senkou_a)) and ((curr_close<senkou_a) and (curr_close<senkou_b)):
                        nine_period_low = float(np.amin(data['Low'][i-8:i+1]))
                        selling_signal = True
                        red = True
                        
                    # red cloud breakout special
                    if((prev_close>prev_senkou_b) and (prev_close>prev_senkou_a)) and ((curr_close<senkou_b) and (curr_close<senkou_a)):
                        nine_period_low = float(np.amin(data['Low'][i-8:i+1]))
                        selling_signal = True
                        red = True
        
        if selling_signal:
            curr_low = data['Low'][i]
            if curr_low<nine_period_low:
                selling_price = nine_period_low - 0.05
                data['Sell'][i] = selling_price
                selling_signal = False
                sold = True
                red = False
        
        if sold:       
            curr_low = data['Low'][i]
            curr_high = data['High'][i]
            high_prev26_day = data['High'][i-1]
            lag_span = data['Lagging span'][i]
            if high_prev26_day<lag_span:
                buying_price = curr_close            
                profit_value = float(selling_price - buying_price)*quantity
                profit.append(profit_value)
                data['Buy'][i] = buying_price
                data['Invest'][i] = buying_price * quantity
                data['Profit'][i] = profit_value
                sold = False
         
    return data
        
            
if __name__ == "__main__":
    
    # print(inrange(10.0,12.050,9.99))
    fetchTicker()
    data = fetchTickerData()
    data = trading(data)
    data.to_excel('data.xlsx')
    # data.plot()
    # plt.show()
    print('Profit : ',sum(profit), 'No of Entries : ', len(profit))