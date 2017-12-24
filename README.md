# Equity Data Plotter

Web application for plotting historical equity data


## Run

1.  Define `FLASK_SECRET_KEY` and `QUANDL_API_KEY` in `.env`

2.  Run via either [Gunicorn](http://gunicorn.org/),

        pipenv run gunicorn edp:app

    [Heroku](https://www.heroku.com/),

        pipenv run heroku local

    or [Flask](http://flask.pocoo.org/).

        FLASK_APP=edp FLASK_DEBUG=true pipenv run flask run

Running via Flask requires first installing the application as a
package (`pipenv install -d '-e .'`).
