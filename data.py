import pandas as pd
import numpy as np
import datetime
from investiny import historical_data, search_assets


def get_data(assets, weights, from_date, to_date):
    start_time=datetime.datetime.strptime(from_date, '%m/%d/%Y') - datetime.timedelta(days=1)
    
    df = pd.DataFrame()
    
    for i in range(len(assets)):
        search_results = search_assets(query=assets[i], limit=1)
        investing_id = int(search_results[0]["ticker"])

        data = historical_data(investing_id=investing_id, from_date=datetime.datetime.strftime(start_time, '%m/%d/%Y'), to_date=to_date)
        data = pd.DataFrame(data)
        data.index = data['date']
        #Appending a new weighted column
        df=pd.concat([df, weights[i]*data['close']], axis=1)
        df.rename(columns={'close': f'{assets[i]}'}, inplace=True)
    
    df['total'] = df.sum(axis=1)
    df['returns'] = (df['total'] - df['total'].shift(1))/df['total'].shift(1)
    df.dropna(axis='rows', inplace=True)
    
    return df['returns']

 

def stocks_returns(assets, weights, from_date, to_date):
    return get_data(assets, weights, from_date, to_date)

def commodities_returns(assets, weights, from_date, to_date):
    return get_data(assets, weights, from_date, to_date)

def cryptocurrencies_returns(assets, weights, from_date, to_date):
    return get_data(assets, weights, from_date, to_date)