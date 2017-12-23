from bokeh.plotting import figure
from bokeh.embed import components
from cachetools import cached
import datetime
from flask import current_app
import logging
import numpy as np
import pandas as pd
import requests


class InstrumdatKey:
    def __init__(self, ticker, date=None):
        self.ticker = ticker.upper()
        self.date = date if date is not None else datetime.date.today()

    def __eq__(self, other):
        return self.ticker == other.ticker \
            and self.date == other.date

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return '{}: {}'.format(self.date, self.ticker)


@cached(cache={})
def _fetch_instr(instrumdat_key):
    ticker = instrumdat_key.ticker
    if instrumdat_key.date != datetime.date.today():
        s = 'cannot fetch data as of {}'
        raise ValueError(s.format(instrumdat_key.date))

    api_key = current_app.config['quandl_api_key']
    url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json'

    logging.info("Fetching data for ticker `{}'".format(ticker))
    r = requests.get(url, params={
        'ticker': ticker,
        'api_key': api_key,
    })
    logging.info("{}".format(r.url.replace(api_key, 'API_KEY')))
    logging.info("Status code: {}".format(r.status_code))
    if r.status_code != 200:
        raise ValueError("invalid ticker `{}'".format(ticker))

    jdata = r.json()
    df = pd.DataFrame(
        jdata['datatable']['data'],
        columns=[x['name'] for x in jdata['datatable']['columns']]
    )
    if df.empty:
        raise ValueError("ticker `{}' returned no data".format(ticker))

    return df


def fetch_instr(ticker):
    """Fetch historical data for a financial instrument."""
    if ticker is None or len(ticker) == 0:
        raise ValueError('missing ticker argument')
    instrumdat_key = InstrumdatKey(ticker)
    df = _fetch_instr(instrumdat_key)

    return df


def moving_average(x, window, fill=True):
    """Return moving average."""
    if len(x) < window:
        s = 'series length {} is smaller than window({})'
        raise ValueError(s.format(len(x), window))
    w = np.ones(window) / float(window)
    a = np.convolve(x, w, 'valid')
    if fill:
        a = np.concatenate((np.nan * np.ones(window - 1), a))
    return a


def build_plot(df, instrument_variables, maxdays=252):
    n = min(len(df), maxdays)
    df = df[-n:]

    # prepare some data
    dates = np.array(df['date'].values, dtype=np.datetime64)
    window = 21

    # create a new plot with a a datetime axis type
    p = figure(width=800, height=350, x_axis_type="datetime")

    # add renderers
    if 'close' in instrument_variables:
        p.circle(dates, df['close'],
                 size=4, color='darkgrey', alpha=0.2, legend='close')
        avg = moving_average(df['close'], window)
        p.line(dates, avg, color='navy', legend='avg close')
    if 'adj_close' in instrument_variables:
        p.circle(dates, df['adj_close'],
                 size=4, color='darkgreen', alpha=0.2, legend='adj_close')
        avg = moving_average(df['adj_close'], window)
        p.line(dates, avg, color='green', legend='avg adj_close')
    if 'open' in instrument_variables:
        p.circle(dates, df['open'],
                 size=4, color='darkred', alpha=0.2, legend='open')
        avg = moving_average(df['open'], window)
        p.line(dates, avg, color='red', legend='avg open')
    if 'adj_open' in instrument_variables:
        p.circle(dates, df['adj_open'],
                 size=4, color='orange', alpha=0.2, legend='adj_open')
        avg = moving_average(df['adj_open'], window)
        p.line(dates, avg, color='brown', legend='avg adj_open')

    # customize by setting attributes
    p.title.text = \
        "One-month moving average, as of {}".format(max(dates))
    p.legend.location = "top_left"
    p.grid.grid_line_alpha = 0
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.ygrid.band_fill_color = "orange"
    p.ygrid.band_fill_alpha = 0.1

    return components(p)
