from database.db import db
from datetime import datetime


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_session_id = db.Column(db.Integer, db.ForeignKey('game_session.id'), nullable=False)

    # Score details
    score = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)  # 1: Easy, 2: Medium, 3: Hard
    words_found = db.Column(db.Integer, nullable=False)
    total_words = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer)  # in seconds

    # Timestamp
    achieved_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    game_session = db.relationship('GameSession', backref=db.backref('scores', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.player.username if self.player else 'Unknown',
            'score': self.score,
            'level': self.level,
            'level_name': {1: 'Easy', 2: 'Medium', 3: 'Hard'}.get(self.level, 'Unknown'),
            'words_found': self.words_found,
            'total_words': self.total_words,
            'time_taken': self.time_taken,
            'achieved_at': self.achieved_at.isoformat(),
            'completion_rate': f"{(self.words_found / self.total_words) * 100:.1f}%"
        }