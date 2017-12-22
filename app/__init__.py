from flask import Flask
import yaml
from app.instrumdat.controllers import instrumdat


def read_configuration(configfile):
    with open(configfile) as f:
        cf = yaml.safe_load(f)
    with open(cf['secret_key_file']) as f:
        secret_key = f.read().strip()
    with open(cf['quandl_api_key_file']) as f:
        api_key = f.read().strip()
    config = {
        'SECRET_KEY': secret_key,
        'quandl_api_key': api_key,
    }
    return config


app = Flask(__name__)
app.config.update(read_configuration('config.yaml'))
app.register_blueprint(instrumdat)
