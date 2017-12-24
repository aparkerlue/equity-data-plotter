from flask import (
    Blueprint, Markup, abort, flash, redirect, render_template, request,
    url_for
)
from jinja2 import TemplateNotFound
from . import models

instrumdat = Blueprint('instrumdat', __name__)

INSTRUMENT_VARIABLES = (
    'close',
    'adj_close',
    'open',
    'adj_open',
)


@instrumdat.route('/')
def show_index():
    if not request.args:
        return render_template('index.html')

    if 'ticker' in request.args:
        args = {
            'ticker': request.args['ticker'].upper(),
            **{k: v for k, v in request.args.items() if k != 'ticker'},
        }
        return redirect(url_for('instrumdat.plot_ticker', **args))
    else:
        abort(404)


@instrumdat.route('/<ticker>')
def plot_ticker(ticker):
    if ticker != ticker.upper():
        args = {'ticker': ticker.upper(), **request.args}
        return redirect(url_for('instrumdat.plot_ticker', **args))

    instrvars = [x for x in request.args if x in INSTRUMENT_VARIABLES]
    args = {'ticker': ticker, 'selections': instrvars}

    try:
        tickdat = models.fetch_instr(ticker)
    except ValueError:
        s = "Unable to fetch data for ticker <code>{}</code>".format(ticker)
        flash(Markup(s))
    else:
        if not instrvars:
            instrvars.append('close')
        comps = models.build_plot(tickdat, instrvars)
        args.update({
            'script': Markup(comps[0]),
            'div': Markup(comps[1]),
        })

    try:
        return render_template('index.html', **args)
    except TemplateNotFound:
        abort(404)
