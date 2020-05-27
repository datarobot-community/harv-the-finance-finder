from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, PasswordField, BooleanField, SelectField, SelectMultipleField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, ValidationError, EqualTo, DataRequired
from app.models import User, Portfolio, Position


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Sign In')
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    password2 = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
    
class PortfolioForm(FlaskForm):
    name = StringField('Portfolio Name', validators=[InputRequired(), Length(min=1, max=100)])
    portfolio_type = SelectField(u'Type of Portfolio', choices=[('Aggressive', 'Aggressive'), ('Defensive', 'Defensive'), ('Hybrid', 'Hybdrid')])
    initial = DecimalField('Initial Investment Amount', validators=[InputRequired()])
    target = DecimalField('Target Value of Portfolio', validators=[InputRequired()])
    tolerance = DecimalField('As a percentage how much risk are you willing to tolorate?', validators=[InputRequired()])
    priority = SelectField(u'Portfolio Focus', choices=[('loss', 'Focus on loss tolerance'), ('target', 'Focus on Target Portfolio Value')])
    us_equities = BooleanField('US Equities')
    us_bonds = BooleanField('US Equities')
    treasury = BooleanField('US Treasury')
    int_equities = BooleanField('International Equities')
    commodities = BooleanField('Commodities')
    real_estate = BooleanField('Real Estate')
    mlps = BooleanField('MLPs')
    int_bonds = BooleanField('International Bonds')
    financial = BooleanField('Financial')
    utilities = BooleanField('Utilities')
    health_care = BooleanField('Health Care')
    con_dis = BooleanField('Consumer Discretionary')
    energy = BooleanField('Energy')
    industrials = BooleanField('Industrials')
    con_staples = BooleanField('Consumer Staples')
    re = BooleanField('Real Estate')
    tech = BooleanField('Technology')
    materials = BooleanField('Materials')
    telco = BooleanField('Telecom')
    etf = BooleanField('Include ETFs?')
    restricted = StringField('Enter stock sticker symbol to have them excluded from AI and Analyst consideration')
    strategy =  SelectField(u'Portfolio Strategy', choices=[('growth', 'Focus on growth assets'), ('value', 'Focus on value assets')])
    
class StockForm(FlaskForm):
    symbol = StringField('Ticker Symbol', validators=[InputRequired(), Length(min=1, max=6)])