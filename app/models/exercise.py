from app import db
from datetime import datetime

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=True)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self, fields=None):
        if fields:
            return {field: getattr(self, field) for field in fields if hasattr(self, field)}
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}