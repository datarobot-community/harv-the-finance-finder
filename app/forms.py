from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, PasswordField, BooleanField, SelectField, SelectMultipleField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, ValidationError, EqualTo, DataRequired
from app.models import User, Portfolio

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
    portfolio_type = SelectField(u'Type of Portfolio', choices=[('growth', 'Growth')])
    # initial = DecimalField('Initial Investment Amount', validators=[InputRequired()])
    # target = DecimalField('Target Value of Portfolio', validators=[InputRequired()])
    # tolerance = DecimalField('As a percentage how much risk are you willing to tolorate?', validators=[InputRequired()])
    # priority = SelectField(u'Portfolio Focus', choices=[('loss', 'Focus on loss tolerance'), ('target', 'Focus on Target Portfolio Value')])
    
    # Filters - include stock markets
    include_nyse = BooleanField('New York Stock Exchange', default="checked")
    include_nasdaq = BooleanField('NASDAQ', default="checked")
    include_nyse_arca = BooleanField('NYSE Arca', default="checked")
    include_nyse_american = BooleanField('NYSE American', default="checked")

    # Filters - exclude sectors
    exclude_communications = BooleanField('Communications')
    exclude_energy_minerals = BooleanField('Energy Minerals')
    exclude_non_energy_minerals = BooleanField('Non Energy Minerals')
    exclude_health_technology = BooleanField('Health Technology')
    exclude_health_services = BooleanField('Health Services')
    exclude_utilities = BooleanField('Utilities')
    exclude_distribution_services = BooleanField('Distribution Services')
    exclude_finance = BooleanField('Finance')
    exclude_process_industries = BooleanField('Process Industries')
    exclude_producer_manufacturing = BooleanField('Producer Manufacturing')
    exclude_commercial_services = BooleanField('Commercial Services')
    exclude_industrial_services = BooleanField('Industrial Services')
    exclude_transportation = BooleanField('Transportation')
    exclude_consumer_durables = BooleanField('Consumer Durables')
    exclude_consumer_non_durables = BooleanField('Consumer Non-Durables')
    exclude_retail_trade = BooleanField('Retail / Trade')
    exclude_electronic_technology = BooleanField('Electronic Technology')
    exclude_technology_services = BooleanField('Technology - Services')

    # ESG category (from our AI)
    # Will be lowest possible risk category (1 - low, 2 - medium, 3- high, 4 - all - include extreme risk)
    esg_risk_category =  SelectField(u'ESG Risk Category', choices=[('1', 'Low'),('2', 'Medium'),('3', 'High'),('4', 'Any')])

 
class StockForm(FlaskForm):
    symbol = StringField('Ticker Symbol', validators=[InputRequired(), Length(min=1, max=6)])