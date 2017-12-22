import logging
from app import app

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    app.run(port=33507, debug=True)
