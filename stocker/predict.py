from stocker.get_data import total
from stocker.lstm import run
import datetime as dt


def tomorrow(stock, features=[], steps=1, training=0.9, period=14, years=1, error_method='mape'):
    stock_data = total(stock, years=years, interest='Interest' in features, wiki_views='Wiki_views' in features,
                       indicators='RSI' and '%K' and '%R' in features, period=period)
    result = run(stock_data, features, steps, training, error_method)
    date = (dt.datetime.today() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    result.append(date)

    return result

