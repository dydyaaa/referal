from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    referrals = db.relationship('Referral', backref='referrer', lazy=True)
    referred_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)