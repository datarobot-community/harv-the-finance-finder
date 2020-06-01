from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt
from app import db, login
from sqlalchemy import desc
import locale 
locale.setlocale(locale.LC_ALL, '')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True)
    email = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    portfolios = db.relationship('Portfolio', backref='owner', lazy='dynamic')
    firstname = db.Column(db.String(30))
    
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

    def has_portfolio(self):
        return True if self.portfolios.all() else False
        
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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Growth vs value (just growth for now)
    p_type = db.Column(db.String(200))

    # Filters - include stock markets
    include_nyse = db.Column(db.Boolean)
    include_nasdaq = db.Column(db.Boolean)
    include_nyse_arca = db.Column(db.Boolean)
    include_nyse_american = db.Column(db.Boolean)

    # Filters - exclude sectors
    exclude_communications = db.Column(db.Boolean)
    exclude_energy_minerals = db.Column(db.Boolean)
    exclude_health_technology = db.Column(db.Boolean)
    exclude_non_energy_minerals = db.Column(db.Boolean)
    exclude_utilities = db.Column(db.Boolean)
    exclude_technology_services = db.Column(db.Boolean)
    exclude_consumer_durables = db.Column(db.Boolean)
    exclude_distribution_services = db.Column(db.Boolean)
    exclude_finance = db.Column(db.Boolean)
    exclude_process_industries = db.Column(db.Boolean)
    exclude_producer_manufacturing = db.Column(db.Boolean)
    exclude_commercial_services = db.Column(db.Boolean)
    exclude_industrial_services = db.Column(db.Boolean)
    exclude_transportation = db.Column(db.Boolean)
    exclude_consumer_non_durables = db.Column(db.Boolean)
    exclude_health_services = db.Column(db.Boolean)
    exclude_retail_trade = db.Column(db.Boolean)
    exclude_electronic_technology = db.Column(db.Boolean)

    # ESG category (from our AI)
    # Will be lowest possible risk category (1 - low, 2 - medium, 3- high, 4 - all - include extreme risk)
    esg_risk_category = db.Column(db.Integer)

    def riskLevel(self):
        if self.esg_risk_category is 1: return 'Low'
        if self.esg_risk_category is 2: return 'Medium'
        if self.esg_risk_category is 3: return 'High'
        else: return 'All'

    def exchanges(self): 
        permitted_exchanges = []
        if self.include_nasdaq: permitted_exchanges.append('NASDAQ')
        if self.include_nyse: permitted_exchanges.append('New York Stock Exchange')
        if self.include_nyse_arca: permitted_exchanges.append('NYSE Arca')
        if self.include_nyse_american: permitted_exchanges.append('NYSE American')
        return permitted_exchanges

    def excludedSectors(self):
        excluded_sectors = []

        if self.exclude_communications: excluded_sectors.append('Communications')
        if self.exclude_energy_minerals: excluded_sectors.append('Energy Minerals')
        if self.exclude_health_technology: excluded_sectors.append('Health Technology')
        if self.exclude_non_energy_minerals: excluded_sectors.append('Non-Energy Minerals')
        if self.exclude_utilities: excluded_sectors.append('Utilities')
        if self.exclude_technology_services: excluded_sectors.append('Technology Services')
        if self.exclude_consumer_durables: excluded_sectors.append('Consumer Durables')
        if self.exclude_distribution_services: excluded_sectors.append('Distribution Services')
        if self.exclude_finance: excluded_sectors.append('Finance')
        if self.exclude_process_industries: excluded_sectors.append('Process Industries')
        if self.exclude_producer_manufacturing: excluded_sectors.append('Producer Manufacturing')
        if self.exclude_commercial_services: excluded_sectors.append('Commercial Services')
        if self.exclude_industrial_services: excluded_sectors.append('Industrial Services')
        if self.exclude_transportation: excluded_sectors.append('Transportation')
        if self.exclude_consumer_non_durables: excluded_sectors.append('Consumer Non-Durables')
        if self.exclude_health_services: excluded_sectors.append('Health Services')
        if self.exclude_retail_trade: excluded_sectors.append('Retail Trade')
        if self.exclude_electronic_technology: excluded_sectors.append('Electronic Technology')

        return excluded_sectors

    def stockSuggestions(self):
        suggestions = StockQuote.query \
        .join(StockEsg, StockQuote.symbol == StockEsg.symbol) \
        .filter(StockQuote.primaryExchange.in_(self.exchanges())) \
        .filter(StockQuote.sector.notin_(self.excludedSectors())) \
        .filter(StockEsg.esg_risk_category <= self.esg_risk_category) \
        .filter(StockQuote.peRatio != None ) \
        .filter(StockQuote.latestPrice != None) \
        .filter(StockQuote.week52Low != None) \
        .filter(StockQuote.week52Low > 0) \
        .order_by(
            desc(
                StockQuote.latestPrice / 
                StockQuote.week52Low
            )
        ) \
        .limit(10)
        return suggestions
    
class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(5))
    holding_long = db.Column(db.String(250))
    shares = db.Column(db.Float)
    price = db.Column(db.Float)
    change = db.Column(db.Float)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    
class StockQuote(db.Model): # This is the "main quote object"
    __tablename__ = 'stockquotes'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(12))
    companyName = db.Column(db.String(250))
    primaryExchange = db.Column(db.String(60))
    peRatio = db.Column(db.Numeric)
    sector = db.Column(db.String(60))
    openPrice = db.Column(db.Numeric)
    closePrice = db.Column(db.Numeric)
    marketOpen = db.Column(db.Numeric)
    latestPrice = db.Column(db.Numeric)
    latestVolume = db.Column(db.Numeric)
    previousClose = db.Column(db.Numeric)
    change = db.Column(db.Numeric)
    changePercent = db.Column(db.Float)
    avgTotalVolume = db.Column(db.Numeric)
    marketCap = db.Column(db.Numeric)
    avgTotalVolume = db.Column(db.Numeric)
    week52High = db.Column(db.Numeric)
    week52Low = db.Column(db.Numeric)
    ytdChange = db.Column(db.Numeric)
    previousVolume = db.Column(db.Numeric)
    volume = db.Column(db.Numeric)
    high = db.Column(db.Numeric)
    low = db.Column(db.Numeric)
    
    def growth_in_last_year(self):
        return self.latestPrice / self.week52Low

    def fmt_growth_in_last_year(self):
        return "{:.4%}".format(self.growth_in_last_year()) 

    def __repr__(self):
        return f"{self.companyName} ({self.symbol}) \n Price {locale.currency(self.latestPrice, grouping=True)} Growth: {self.fmt_growth_in_last_year()}"

class StockEsg(db.Model):
    __tablename__ = 'stock_esgs'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(12))
    esg_risk_category = db.Column(db.Integer)

class Stock(db.Model):
    __tablename__ = 'stocks'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))

    def __init__(self, symbol):
        self.symbol = symbol    
    
    def __repr__(self):
        return f"<Stock {self.symbol}"

class StockSector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))
    security = db.Column(db.String(500))
    sector = db.Column(db.String(120))
    sub_industry = db.Column(db.String(120))
    
class Stock_Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(6))
    image_url = db.Column(db.String(1024))
    
class Stock_Highlow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(6))
    high_val52wk = db.Column(db.Numeric)
    low_val52wk = db.Column(db.Numeric)
