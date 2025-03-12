from app import db
from datetime import datetime

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    workout_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    workout_type = db.Column(db.String(100), default='regular workout')
    created_at = db.Column(db.DateTime, default=datetime.now())
    exercises = db.relationship('Exercise', backref='workout', lazy=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}