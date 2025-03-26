from app import db
from datetime import datetime


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    weight = db.Column(db.Float, nullable=True)
    sets = db.Column(db.Integer, nullable=False)  # Количество подходов
    reps = db.Column(db.Integer, nullable=False)  # Количество повторений
    created_at = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self, fields=None):
        if fields:
            return {field: getattr(self, field) for field in fields if hasattr(self, field)}
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}