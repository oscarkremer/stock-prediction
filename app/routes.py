KEY = 'TSHI91Q1K43R9H5M'
from flask_login import current_user, login_required, login_user, logout_user
from flask import render_template, url_for, flash, redirect, request, abort, send_file, make_response
from werkzeug.urls import url_parse
from app import app, db, bcrypt
from app.forms import *
from app.models import User, Stock
from sqlalchemy import desc
from time import sleep
import requests, json, atexit, time
from alpha_vantage.timeseries import TimeSeries

@app.route('/home')
def index():
    return render_template("index.html", title='Home Page')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                'http://127.0.0.1:8000/dashboard', code=302)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))

@app.route('/symbol/new')
@login_required
def create_symbol():
    logout_user()

    return redirect(url_for('index'))


@app.route("/company/new", methods=['GET', 'POST'])
@login_required
def new_company():
    form = CompanyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                TimeSeries(key=KEY, output_format='pandas').get_intraday(symbol=form.symbol.data.upper(),interval='1min')
                company = Stock(stock_name=form.name.data, symbol = form.symbol.data)
                db.session.add(company)
                db.session.commit()
                flash('A new company has been registered!', 'success')
                return redirect(url_for('/home'))
            except Exception as e:
                print(e)
                flash('Error connecting to API, please verify SYMBOL', 'danger')                
        else:
            flash('Error, please check the added information', 'danger')
    return render_template('create_company.html', title='New Company',
                           form=form, legend='New Company')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
            email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

