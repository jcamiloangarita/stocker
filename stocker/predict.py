from stocker.get_data import total
from stocker.lstm import run
import datetime as dt


def tomorrow(stock, features=None, steps=1, training=0.9, period=14, years=1, error_method='mape', plot=False):
    """
    Function to predict the "close price" for the next day.

    Arguments:
        stock (str): stock label
        features (list): ['Interest', 'Wiki_views', 'RSI', '%K', '%R']
        steps (int): previous days to consider for generating the model.
        training (float): fraction assigned for training the model
        period (int): number of days considered for calculating indicators.
        years (int or float): years of data to be considered
        error_method (str): 'mape' or 'mse'
        plot (bool): generate performance plot

    Returns:
        Result for the next business day. [price, error, date]
    """

    if features is None:
        features = []

    # GET ALL THE DATA:
    stock_data = total(stock, years=years, interest='Interest' in features, wiki_views='Wiki_views' in features,
                       indicators='RSI' and '%K' and '%R' in features, period=period)

    # SPLIT DATA, CREATE THE MODEL, GENERATE AND CALCULATE THE ERROR:
    result, y_predicted, df = run(stock_data, features, steps, training, error_method)

    date = (dt.datetime.today() + dt.timedelta(days=1))
    while date.weekday() == 5 or date.weekday() == 6:
        date = date + dt.timedelta(days=1)
    date = date.strftime('%Y-%m-%d')
    result.append(date)

    if not plot:
        return result

    if plot:
        dates = df.index.tolist()
        from pandas.plotting import register_matplotlib_converters
        register_matplotlib_converters()
        import matplotlib.pyplot as plt
        plt.plot(dates, y_predicted)
        plt.plot(dates, df.Close.tolist())
        plt.title(stock + ' - %1.2f' % result[0] + ' - %1.3f' % result[1] + '% - ' + result[2])
        plt.xlabel('Date')
        plt.ylabel('Close price (USD)')
        plt.legend(['Predicted', 'True'])
        plt.gcf().autofmt_xdate()
        plt.show()

        return result
