from app import db

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    full_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

    height_cm = db.Column(db.Float, nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)

    goal = db.Column(db.String(50), nullable=True)
    activity_level = db.Column(db.String(50), nullable=True)

    user = db.relationship('User', backref=db.backref('profile', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'height_cm': self.height_cm,
            'weight_kg': self.weight_kg,
            'goal': self.goal,
            'activity_level': self.activity_level,
        }