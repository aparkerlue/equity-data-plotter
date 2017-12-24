# Equity Data Plotter

Web application for plotting historical equity data

## To run

    pipenv run heroku local
    pipenv run gunicorn edp:app
    FLASK_APP=edp FLASK_DEBUG=1 pipenv run flask run
