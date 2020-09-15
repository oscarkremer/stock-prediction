from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app import bcrypt
from app.models import User, Stock



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])

    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountUpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user_query = User.query.filter_by(username=username.data).first()
            if user_query:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user_query = User.query.filter_by(email=email.data).first()
            if user_query:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')

class CompanyForm(FlaskForm):
    name = StringField('Company Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    symbol = StringField('Symbol',
                           validators=[DataRequired(), Length(min=2, max=100)])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])

    submit = SubmitField('New Company')
  
    def validate_symbol(self, symbol):
        stock = Stock.query.filter_by(stock_name=symbol.data).first()
        if stock:
            raise ValidationError(
                'That Symbol is taken. Please choose a different one.')