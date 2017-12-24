import logging
import os
from flask import Flask, send_from_directory
from .instrumdat.controllers import instrumdat

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY=os.environ['FLASK_SECRET_KEY'],
    QUANDL_API_KEY=os.environ['QUANDL_API_KEY'],
))
app.register_blueprint(instrumdat)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
