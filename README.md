# Equity Data Plotter

Web application for plotting historical equity data


ip## Run

1.  Define `FLASK_SECRET_KEY` and `QUANDL_API_KEY` in `.env`

2.  Run via either [Gunicorn](http://gunicorn.org/)

        pipenv run gunicorn edp:app

    or [Heroku](https://www.heroku.com/).

        pipenv run heroku local

You can also run this application with Flask's built-in server:

    FLASK_APP=edp FLASK_DEBUG=true pipenv run flask run

But that requires first installing the application as a package
(`pipenv install -d '-e .'`).
