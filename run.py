import logging
from app import app

logging.getLogger().setLevel(logging.INFO)
app.run(port=33507, debug=True)
