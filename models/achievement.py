from database.db import db
from datetime import datetime


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50), nullable=False)  # e.g., '🥉' or 'fa-trophy'

    # Logic Configuration
    category = db.Column(db.String(50), nullable=False)  # e.g., 'score', 'streak', 'games_played'
    threshold = db.Column(db.Integer, nullable=False)  # e.g., 500 (points), 10 (games)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'category': self.category,
            'threshold': self.threshold
        }


class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)

    achievement = db.relationship('Achievement')