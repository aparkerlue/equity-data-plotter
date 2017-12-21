from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from . import models

instrumdat = Blueprint('instrumdat', __name__)


@instrumdat.route('/<ticker>')
def show(ticker):
    try:
        x = models.fetch_instr(ticker)
        return str(x)
    except TemplateNotFound:
        abort(404)
