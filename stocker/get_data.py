import pandas as pd
import yfinance as yf
import requests
import datetime as dt
from pytrends.request import TrendReq


def main(stock, years=1):  # function to get data from Yahoo Finance
    end = dt.datetime.today().strftime('%Y-%m-%d')  # today as the end date
    start = (dt.datetime.today() - dt.timedelta(days=365*years)).strftime('%Y-%m-%d')  # 1 year ago as start
    df = yf.download(stock, start, end)

    return df, start, end


def company_name(stock):  # function to get the company's name from the stock
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(stock)  # source
    company = requests.get(url).json()['ResultSet']['Result'][0]['name']   # saving the name as 'company'

    return company


def get_interest(company, timeframe):  #  base function to get 'interest' from Google Trends
    pytrend = TrendReq()  # accessing to Google Trends using pytrends package
    pytrend.build_payload(kw_list=[company], timeframe=timeframe)  # finding interest for 'company' during 'timeframe'
    result = pytrend.interest_over_time().drop('isPartial', axis=1)  # saving the 'interest' values

    return result


def add_interest(df, company, years=1):  # main function to get 'interest' from Google Trends
    delta = int((365 * years / 73) - 1)  # dividing the year in groups of 73 days
    since = (dt.datetime.today() - dt.timedelta(days=365 * years)).strftime('%Y-%m-%d')
    until = (dt.datetime.today() - dt.timedelta(days=73 * delta)).strftime('%Y-%m-%d')
    timeframe = since + ' ' + until  # setting the required format
    trends = get_interest(company, timeframe)  # get the values for the first 73 days
    for x in range(delta):  # get the values for the rest of the year
        since = (dt.datetime.today() - dt.timedelta(days=73 * (delta - x))).strftime('%Y-%m-%d')
        until = (dt.datetime.today() - dt.timedelta(days=73 * (delta - 1 - x))).strftime('%Y-%m-%d')
        timeframe = since + ' ' + until
        trends.append(get_interest(company, timeframe))

    trends.rename(columns={company: 'Interest'}, inplace=True)  # changing title to 'Interest'
    trends.index.names = ['Date']
    df = df.merge(trends, how='left', on='Date')  # Add Interest column from Google Trends API - pytrends
    df.Interest.interpolate(inplace=True)  # interpolation for missing values

    return df


def add_wiki_views(df, company, start, end):  # function to get number of page views from Wikipedia
    start = start.replace('-', '')
    end = end.replace('-', '')
    link = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents' \
           '/{company}/daily/{st}/{end}'.format(company=company, st=start, end=end)
    r = requests.Session()
    r.headers = {"User-Agent": "stocker/0.1.7 (https://github.com/jcamiloangarita/stocker; camiloang94@gmail.com)"}
    response = r.get(link)
    wiki_data = response.json()  # get the data from Wikipedia API
    views = [i['views'] for i in wiki_data['items']]  # saving views values
    date = [i['timestamp'] for i in wiki_data['items']]  # saving dates
    date = [dt.datetime.strptime(date[:-2], '%Y%m%d').date().strftime('%Y-%m-%d') for date in date]  # change format
    wiki_views = pd.DataFrame(views, index=date, columns=['Wiki_views'])
    wiki_views.index.name = 'Date'
    wiki_views.index = pd.to_datetime(wiki_views.index)

    df = df.merge(wiki_views, how='left', on='Date')  # Add Wiki_views column from Wikipedia API
    df.Wiki_views.ffill(inplace=True)

    return df


def add_rsi(df, period):    # function to Calculate RSI values
    df['Change'] = df.Close - df.Open  # calculating gains and losses in a new column
    df['Gain'] = df.Change[df.Change > 0]  # new column of gains
    df['Loss'] = df.Change[df.Change < 0] * (-1)  # new column of losses
    df.drop(columns=['Change'], inplace=True)  # remove the column change

    # Filling missing values with 0
    df.Gain.fillna(0, inplace=True)
    df.Loss.fillna(0, inplace=True)

    df['Again'] = df.Gain.rolling(period).mean()  # calculate the average gain in the last 14 periods
    df['Aloss'] = df.Loss.rolling(period).mean()  # calculate the average loss in the last 14 periods

    df['RS'] = df.Again / df.Aloss  # calculating RS
    df['RSI'] = 100 - (100 / (1 + (df.Again / df.Aloss)))  # calculating RSI
    df.drop(columns=['Gain', 'Loss', 'Again', 'Aloss', 'RS'], inplace=True)  # remove undesired columns

    return df


def add_k(df, period):   # Calculate Stochastic Oscillator (%K)
    df['L14'] = df.Low.rolling(period).min()  # find the lowest price in the last 14 periods
    df['H14'] = df.High.rolling(period).max()  # find the highest price in the last 14 periods
    df['%K'] = ((df.Close - df.L14) / (df.H14 - df.L14)) * 100
    df.drop(columns=['L14', 'H14'], inplace=True)  # remove columns L14 and H14

    return df


def add_r(df, period):  # Calculate Larry William indicator (%R)
    df['HH'] = df.High.rolling(period).max()  # find the highest high price in the last 14 periods
    df['LL'] = df.Low.rolling(period).min()  # find the lowest low price in the last 14 periods
    df['%R'] = ((df.HH - df.Close) / (df.HH - df.LL)) * (-100)
    df.drop(columns=['HH', 'LL'], inplace=True)  # remove columns HH and LL

    return df


def total(stock, years=1, interest=False, wiki_views=False, indicators=False, period=14):
    # main function to combine data from Yahoo Finance, Google Trends, Wikipedia and calculated indicators.
    df, start, end = main(stock, years=years)  # get data from Yahoo Finance and define star and end
    company = company_name(stock)  # get the name of the company

    if interest:
        df = add_interest(df, company, years=years)  # adding Interest from Google Trends.

    if wiki_views:
        df = add_wiki_views(df, company, start, end)  # adding Wiki Views

    if indicators:  # Adding indicators
        df = add_k(df, period)  # generating %K column.
        df = add_r(df, period)  # generating %R column.
        df = add_rsi(df, period)  # generating RSI column.

    df = df.dropna()   # drop rows with missing data

    return df


def correlation(stock, years=1, interest=False, wiki_views=False, indicators=False, period=14, complete=True, limit=0.5):
    # function to get the Pearson correlation coefficients for all the features

    df = total(stock, years, interest, wiki_views, indicators, period)

    if complete:
        features = df.corr().Close
    else:  # only the coefficients against the close prices
        features = df.corr().Close[df.corr().Close > limit].index.tolist()

    return features
