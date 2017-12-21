from flask import Flask, render_template
import yaml
from app.instrumdat.controllers import instrumdat


def read_configuration(configfile):
    with open(configfile) as f:
        cf = yaml.safe_load(f)
    with open(cf['quandl_api_key_file']) as f:
        apikey = f.read().strip()
    config = {
        'apikey': apikey
    }
    return config


app = Flask(__name__)
app.config['instrumdat'] = read_configuration('config.yaml')
app.register_blueprint(instrumdat)


@app.route('/')
def index():
    return render_template('index.html')
