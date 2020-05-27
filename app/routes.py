from datetime import datetime
from flask import render_template, request, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db, r, q
from app.forms import LoginForm, RegisterForm, ResetPasswordForm, ResetPasswordRequestForm, PortfolioForm, StockForm
from app.models import User, Portfolio, Stock
from app.tasks import count_words
from time import strftime
import json

@app.route('/')
def index():
    return render_template('index.html', title="Harv AI")

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

@app.route('/portfolio_build', methods=['GET', 'POST'])
def create_portfolio():
    form = PortfolioForm()
    if form.validate_on_submit():
        new_portfolio = Portfolio(name=form.name.data, p_type=form.portfolio_type.data, initial=form.initial.data,
                                target=form.target.data, tolerance=form.tolerance.data, priority=form.priority.data, us_equities=form.us_equities.data,
                                us_bonds=form.us_bonds.data, treasury=form.treasury.data, int_equities=form.int_equities.data, commodities=form.commodities.data,
                                real_estate=form.real_estate.data, mlps=form.mlps.data, int_bonds=form.int_bonds.data, financial=form.financial.data,
                                utilitie=form.utilities.data, health_care=form.health_care.data, con_dis=form.con_dis.data, energy=form.energy.data,
                                industrials=form.industrials.data, con_staples=form.con_staples.data, re=form.re.data, tech=form.tech.data,
                                materials=form.materials.data, telco=form.telco.data, etf=form.etf.data, restricted=form.restricted.data,
                                strategy=form.strategy.data)
        db.session.add(new_portfolio)
        db.session.commit()
        flash('Congratulations, you have created a portfolio')
        return redirect(url_for('portfolio_build'))
    return render_template('portfolio_build.html', title='Portfolio Wizard', form=form)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route("/add-task", methods=["GET", "POST"])
def add_task():

    jobs = q.jobs  # Get a list of jobs in the queue
    message = None

    if request.args:  # Only run if a query string is sent in the request
        url = request.args.get("url")  # Gets the URL coming in as a query string
        task = q.enqueue(count_words, url)  # Send a job to the task queue
        jobs = q.jobs  # Get a list of jobs in the queue
        q_len = len(q)  # Get the queue length
        message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {q_len} jobs queued"

    return render_template("add_task.html", message=message, jobs=jobs)

@app.route("/add-stock", methods=["GET", "POST"])
def add_stock():
    form = StockForm()  
    if form.validate_on_submit():
        new_stock = Stock(symbol=form.symbol.data)
        db.session.add(new_stock)
        db.session.commit()
        flash("Stock successfully added")
        return redirect(url_for('portfolio'))
    return render_template('add_stock.html', form=form)

@app.route("/earnings-calendar")
def earnings_calendar():
    return render_template('earnings_calendar.html')

@app.route("/dashboard/stock-picks")
def stock_picks():
    return render_template('stock_picks.html')