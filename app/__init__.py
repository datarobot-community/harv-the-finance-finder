from flask import Flask
import os
from dotenv import load_dotenv
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail
import click

app = Flask(__name__)
app.config.from_object(Config)
db =SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
bootstrap = Bootstrap(app)
mail = Mail(app)

APCA_API_KEY = os.getenv("APCA_API_KEY")
APCA_SECRET_KEY = os.getenv("APCA_SECRET_KEY")
APCA_HEADERS = {'APCA-API-KEY-ID': APCA_API_KEY, 'APCA-API-SECRET-KEY': APCA_SECRET_KEY}
APCA_BASE_URL = "https://paper-api.alpaca.markets"
        
IEX_ACCOUNT = os.getenv("IEX_ACCOUNT")
IEX_KEY = os.getenv("IEX_KEY")
IEX_BASE_URL = "https://cloud.iexapis.com/stable/stock/"

from app import routes, models, forms, seed_stocks

# Run flask seed_data to seed your initial stocks from the attached csvs
@app.cli.command('seed_data')
def seed_data():
    seed_stocks.seed_stock_quotes()
    seed_stocks.seed_esgs()