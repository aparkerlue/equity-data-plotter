from cachetools import cached
import datetime
from flask import current_app
import logging
import pandas as pd
import requests


class InstrumdatKey:
    def __init__(self, ticker, date=None):
        self.ticker = ticker
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
    jdata = r.json()
    df = pd.DataFrame(
        jdata['datatable']['data'],
        columns=[x['name'] for x in jdata['datatable']['columns']]
    )

    return df


def fetch_instr(ticker):
    """Fetch historical data for a financial instrument."""
    instrumdat_key = InstrumdatKey(ticker)
    df = _fetch_instr(instrumdat_key)

    return df
