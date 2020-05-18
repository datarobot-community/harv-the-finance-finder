from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True)
    email = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    portfolios = db.relationship('Portfolio', backref='owner', lazy='dynamic')
    
    def __unicode__(self):
        return self.username
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
        
    @staticmethod
    def verify_reset_password(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
            
        except:
            return
        return User.query.get(id)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

    
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    p_type = db.Column(db.String(200))
    holding = db.Column(db.String(5))
    holding_long = db.Column(db.String(250))
    shares = db.Column(db.Float)
    price = db.Column(db.Float)
    change = db.Column(db.Float)
    
class Risk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initial = db.Column(db.Numeric)
    target = db.Column(db.Numeric)
    tolerance = db.Column(db.Numeric)
    priority = db.Column(db.String(100))
    
class Structure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    us_equities = db.Column(db.Boolean)
    us_bonds = db.Column(db.Boolean)
    treasury = db.Column(db.Boolean)
    int_equities = db.Column(db.Boolean)
    commodities = db.Column(db.Boolean)
    real_estate = db.Column(db.Boolean)
    mlps = db.Column(db.Boolean)
    int_bonds = db.Column(db.Boolean)
    
class Restriction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    financial = db.Column(db.Boolean)
    utilitie = db.Column(db.Boolean)
    health_care = db.Column(db.Boolean)
    con_dis = db.Column(db.Boolean)
    energy = db.Column(db.Boolean)
    industrials = db.Column(db.Boolean)
    con_staples = db.Column(db.Boolean)
    re = db.Column(db.Boolean)
    tech = db.Column(db.Boolean)
    materials = db.Column(db.Boolean)
    telco = db.Column(db.Boolean)
    etf = db.Column(db.Boolean)
    restricted = db.Column(db.String(500))
    
class Strategy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strategy = db.Column(db.String(50))    