from app import db
from datetime import datetime

class FoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    weight_grams = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, default=datetime.now())

    def to_dict(self, fields=None):
        if fields:
            return {field: getattr(self, field) for field in fields if hasattr(self, field)}
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
