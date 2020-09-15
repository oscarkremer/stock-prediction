from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(100), unique=True, nullable=False)
    analysis = db.relationship('Analysis', backref='company_author', lazy=True)
    image_file = db.Column(
        db.String(20),
        nullable=False,
        default='default.png')
    def __repr__(self):
        return f"Company('{self.name}')"

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    opened = db.Column(db.Float, nullable=False, default=0)
    high = db.Column(db.Float, nullable=False, default=0)
    low = db.Column(db.Float, nullable=False, default=0)
    close = db.Column(db.Float, nullable=False, default=0)
    volume = db.Column(db.Float, nullable=False, default=0)

db.create_all()
