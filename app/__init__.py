from flask import Flask
import os
from dotenv import load_dotenv
import redis
from rq import Queue
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail

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

r = redis.Redis()

q = Queue(connection=r)



from app import routes, models, forms, tasks, seed_stocks

# Seed DB stuff here
try:
    seed_stocks.seed_stock_quotes()
    seed_stocks.seed_esgs()
    pass
except:
    print("Error seeding stock quotes")
    pass
