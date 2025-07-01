from app import db
from datetime import datetime

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    sets = db.relationship('Set', backref='exercise', lazy=True)

    def to_dict(self, fields=None):
        if fields:
            return {field: getattr(self, field) for field in fields if hasattr(self, field)}
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}