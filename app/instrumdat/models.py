from flask import current_app
import pandas as pd
import requests


def fetch_instr(ticker):
    apikey = current_app.config['instrumdat']['apikey']
    url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json'
    r = requests.get(url, params={
        'ticker': ticker,
        'api_key': apikey,
        'date': '1999-11-18,1999-11-19',
    })
    jdata = r.json()
    df = pd.DataFrame(
        jdata['datatable']['data'],
        columns=[x['name'] for x in jdata['datatable']['columns']]
    )
    return df
