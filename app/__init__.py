from flask import Flask
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




from app import routes, models, forms