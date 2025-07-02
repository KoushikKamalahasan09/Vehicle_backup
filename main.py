# main.py

from flask import Flask
from config import Config
from app.models import db
from app.routes import register_routes
from app.__init__ import setup_database

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
setup_database(app)
register_routes(app)
# Configuration for the Flask app



if __name__ == "__main__":
    app.run(debug=True)
