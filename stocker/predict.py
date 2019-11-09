from stocker.get_data import total
from stocker.lstm import run
import datetime as dt


def tomorrow(stock, features=[], steps=1, training=0.9, interest=False, wiki_views=False, indicators=False, period=14,
             years=1, error_method='mape'):
    stock_data = total(stock, years, interest, wiki_views, indicators, period)
    result = run(stock_data, features, steps, training, error_method)
    date = (dt.datetime.today() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    result.append(date)

    return result

