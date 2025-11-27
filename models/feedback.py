from database.db import db
from datetime import datetime


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5 stars
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='new')  # new, read, responded

    def to_dict(self):
        from models.user import User
        user = User.query.get(self.user_id) if self.user_id else None

        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': user.username if user else 'Anonymous',
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'rating': self.rating,
            'submitted_at': self.submitted_at.isoformat(),
            'status': self.status
        }