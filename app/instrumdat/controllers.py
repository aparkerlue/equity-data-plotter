from flask import (
    Blueprint, abort, flash, redirect, render_template, request, url_for
)
from jinja2 import TemplateNotFound
from . import models

instrumdat = Blueprint('instrumdat', __name__)

instrument_variables = {
    'close': True,
    'adj_close': False,
    'open': False,
    'adj_open': False,
}


@instrumdat.route('/')
@instrumdat.route('/<ticker>')
def show(ticker=None):
    # return str(models.fetch_instr(ticker))
    try:
        comps = models.build_plot(
            ticker,
            [k for k, v in instrument_variables.items() if v],
        )
    except ValueError:
        comps = None

    try:
        if comps is not None:
            return render_template(
                'index.html',
                ticker=ticker,
                script=comps[0],
                div=comps[1],
            )
        else:
            flash("Unable to fetch data for ticker `{}'".format(ticker))
            return render_template('index.html')
    except TemplateNotFound:
        abort(404)


@instrumdat.route('/request-ticker', methods=['GET'])
def request_ticker():
    ticker = request.args.get('ticker').upper()
    for k in instrument_variables:
        instrument_variables[k] = k in request.args.getlist('instr_variable')
    return redirect(url_for('instrumdat.show', ticker=ticker))
