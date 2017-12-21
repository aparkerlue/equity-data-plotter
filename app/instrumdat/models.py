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
        raise ValueError(
            'cannot fetch data as of {}'.format(instrumdat_key.date)
        )

    apikey = current_app.config['instrumdat']['apikey']
    url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json'

    logging.info("Fetching data for ticker `{}'".format(ticker))
    r = requests.get(url, params={
        'ticker': ticker,
        'api_key': apikey,
    })
    logging.info("{}".format(r.url))
    logging.info("Status code: {}".format(r.status_code))
    if r.status_code != 200:
        raise ValueError("invalid ticker `{}'".format(ticker))

    jdata = r.json()
    df = pd.DataFrame(
        jdata['datatable']['data'],
        columns=[x['name'] for x in jdata['datatable']['columns']]
    )

    return df


def fetch_instr(ticker):
    """Fetch historical data for a financial instrument."""
    if ticker is None or len(ticker) == 0:
        raise ValueError('missing ticker argument')
    instrumdat_key = InstrumdatKey(ticker)
    df = _fetch_instr(instrumdat_key)

    return df


def build_plot(ticker, instrument_variables):
    df = fetch_instr(ticker)

    # prepare some data
    close = np.array(df['adj_close'])
    dates = np.array(df['date'], dtype=np.datetime64)

    window_size = 30
    window = np.ones(window_size) / float(window_size)
    avg = np.convolve(close, window, 'same')

    # create a new plot with a a datetime axis type
    p = figure(width=800, height=350, x_axis_type="datetime")

    # add renderers
    p.circle(dates, close, size=4, color='darkgrey',
             alpha=0.2, legend='close')
    p.line(dates, avg, color='navy', legend='avg')

    # NEW: customize by setting attributes
    p.title.text = "df One-Month Average"
    p.legend.location = "top_left"
    p.grid.grid_line_alpha = 0
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.ygrid.band_fill_color = "olive"
    p.ygrid.band_fill_alpha = 0.1

    return components(p)
