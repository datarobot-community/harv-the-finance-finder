from datetime import datetime
from flask import render_template, request, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db, seed_stocks
from app.forms import LoginForm, RegisterForm, ResetPasswordForm, ResetPasswordRequestForm, PortfolioForm, StockForm
from app.models import User, Portfolio
from time import strftime
import json


@app.route('/')
def index():
    # Seed DB stuff here on first run
    # seed_stocks.seed_stock_quotes()
    # seed_stocks.seed_esgs()

    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.has_portfolio():
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('create_portfolio'))

@app.route('/portfolio/build', methods=['GET', 'POST'])
@app.route('/portfolio_build', methods=['GET', 'POST'])
def create_portfolio():
    form = PortfolioForm()
    if form.validate_on_submit():
        
        new_portfolio = Portfolio(
            name = form.name.data, 
            p_type = form.portfolio_type.data,
            owner_id=current_user.id,

             # Filters - include stock markets
            include_nyse = form.include_nyse.data,
            include_nasdaq = form.include_nasdaq.data,
            include_nyse_arca = form.include_nyse_arca.data,
            include_nyse_american = form.include_nyse_american.data,

            # Filters - exclude sectors
            exclude_communications = form.exclude_communications.data,
            exclude_energy_minerals = form.exclude_energy_minerals.data,
            exclude_non_energy_minerals = form.exclude_non_energy_minerals.data,
            exclude_health_technology = form.exclude_health_technology.data,
            exclude_health_services = form.exclude_health_services.data,
            exclude_utilities = form.exclude_utilities.data,
            exclude_distribution_services = form.exclude_distribution_services.data,
            exclude_finance = form.exclude_finance.data,
            exclude_process_industries = form.exclude_process_industries.data,
            exclude_producer_manufacturing = form.exclude_producer_manufacturing.data,
            exclude_commercial_services = form.exclude_commercial_services.data,
            exclude_industrial_services = form.exclude_industrial_services.data,
            exclude_transportation = form.exclude_transportation.data,
            exclude_consumer_durables = form.exclude_consumer_durables.data,
            exclude_consumer_non_durables = form.exclude_consumer_non_durables.data,
            exclude_retail_trade = form.exclude_retail_trade.data,
            exclude_electronic_technology = form.exclude_electronic_technology.data,
            exclude_technology_services = form.exclude_technology_services.data,

            # ESG category (from our AI)
            # Will be lowest possible risk category (1 - low, 2 - medium, 3- high, 4 - all - include extreme risk)
            esg_risk_category =  form.esg_risk_category.data
            
            # Oher stuff..
        )
        db.session.add(new_portfolio)
        db.session.commit()
        flash('Congratulations, you have created a portfolio')
        return redirect(url_for('dashboard'))
    return render_template('portfolio_build.html', title='Portfolio Wizard', form=form)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    portfolios = current_user.portfolios.all()
    return render_template('dashboard.html', user=current_user, user_portfolios=portfolios)

@app.route('/portfolio/<portfolio_id>')
def portfolio(portfolio_id):
    if current_user.is_authenticated:
        for portfolio in current_user.portfolios.all():
            print(portfolio.id)
            if portfolio.id == int(portfolio_id):
                print('Found portfolio')
                return render_template('portfolio.html', portfolio=portfolio)
        print('Didnt find portfolio')
        return render_template('portfolio.html', portfolio=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
