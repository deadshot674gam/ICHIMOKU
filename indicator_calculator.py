def add_conversion_line(data):
    high_prices = data['High']
    low_prices = data['Low']
    nine_period_high =  high_prices.rolling(window=9).max()
    nine_period_low = low_prices.rolling(window=9).min()
    data['Conversion Line'] = (nine_period_high + nine_period_low) /2
    return data


def add_base_line(data):
    high_prices = data['High']
    low_prices = data['Low']
    period26_high = high_prices.rolling(window=26).max()
    period26_low = low_prices.rolling(window=26).min()
    data['Base Line'] = (period26_high + period26_low) / 2
    return data

def add_lagging_span(data):
    close_prices = data['Close']
    data['Lagging span'] = close_prices
    return data

def add_Kumo_cloud(data):
    high_prices = data['High']
    low_prices = data['Low']
    data['Senkou A'] = ((data['Conversion Line'] + data['Base Line']) / 2).shift(25)
    period52_high = high_prices.rolling(window=52).max()
    period52_low = low_prices.rolling(window=52).min()
    data['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(25)
    return data

def adding_all_indicators(data):
    high_prices = data['High']
    low_prices = data['Low']
    
    nine_period_high =  high_prices.rolling(window=9).max()
    nine_period_low = low_prices.rolling(window=9).min()
    data['Conversion Line'] = (nine_period_high + nine_period_low) /2
    
    period26_high = high_prices.rolling(window=26).max()
    period26_low = low_prices.rolling(window=26).min()
    data['Base Line'] = (period26_high + period26_low) / 2
    
    close_prices = data['Close']
    data['Lagging span'] = close_prices
    
    data['Senkou A'] = ((data['Conversion Line'] + data['Base Line']) / 2).shift(25)
    period52_high = high_prices.rolling(window=52).max()
    period52_low = low_prices.rolling(window=52).min()
    data['Senkou B'] = ((period52_high + period52_low) / 2).shift(25)
    
    return data