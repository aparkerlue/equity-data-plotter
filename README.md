# Equity Data Plotter

Web application for plotting historical equity data


## Run

1.  Define `FLASK_SECRET_KEY` and `QUANDL_API_KEY` in `.env`

2.  Run via either Flask,

        FLASK_APP=edp FLASK_DEBUG=1 pipenv run flask run

    Gunicorn,

        pipenv run gunicorn edp:app

    or Heroku

        pipenv run heroku local
