
from database.db import db


class Achievement(db.Model):
    __tablename__ = 'achievement'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(20), default='Trophy')  # e.g., Star, Rocket
    requirement_type = db.Column(db.String(50), nullable=False)  # e.g., 'total_games'
    requirement_value = db.Column(db.Integer, nullable=False)
    is_secret = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'requirement_type': self.requirement_type,
            'requirement_value': self.requirement_value,
            'is_secret': self.is_secret
        }