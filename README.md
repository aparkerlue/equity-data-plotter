# Equity Data Plotter

Web application for plotting historical equity data


## Run

1.  Define `FLASK_SECRET_KEY` and `QUANDL_API_KEY` in `.env`

2.  Run via either [Gunicorn](http://gunicorn.org/)

        pipenv run gunicorn edp:app

    or [Heroku](https://www.heroku.com/).

        pipenv run heroku local

You can also run this application with Flask's built-in server:

    FLASK_APP=edp FLASK_DEBUG=true pipenv run flask run

But that requires installing the application as a package. See [Larger
Applications — Flask Documentation (0.12)](http://flask.pocoo.org/docs/0.12/patterns/packages/).
