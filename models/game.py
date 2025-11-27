from database.db import db
from datetime import datetime
import json


class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=1)  # 1: Easy, 2: Medium, 3: Hard
    grid_size = db.Column(db.Integer, default=8)

    # Store grid as JSON string
    grid_data = db.Column(db.Text, nullable=False)

    # Store words as JSON list
    words_to_find = db.Column(db.Text, nullable=False)

    # Store found words as JSON list
    found_words = db.Column(db.Text, default='[]')

    # Game state
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    is_completed = db.Column(db.Boolean, default=False)
    time_taken = db.Column(db.Integer)  # in seconds

    # Score details
    score = db.Column(db.Integer, default=0)
    max_possible_score = db.Column(db.Integer, default=100)

    def __init__(self, **kwargs):
        super(GameSession, self).__init__(**kwargs)
        # Convert lists to JSON strings when setting
        if 'grid_data' in kwargs and isinstance(kwargs['grid_data'], list):
            self.grid_data = json.dumps(kwargs['grid_data'])
        if 'words_to_find' in kwargs and isinstance(kwargs['words_to_find'], list):
            self.words_to_find = json.dumps(kwargs['words_to_find'])
        if 'found_words' in kwargs and isinstance(kwargs['found_words'], list):
            self.found_words = json.dumps(kwargs['found_words'])

    @property
    def grid(self):
        """Get grid as Python list"""
        return json.loads(self.grid_data) if self.grid_data else []

    @grid.setter
    def grid(self, value):
        """Set grid from Python list"""
        self.grid_data = json.dumps(value)

    @property
    def words(self):
        """Get words to find as Python list"""
        return json.loads(self.words_to_find) if self.words_to_find else []

    @words.setter
    def words(self, value):
        """Set words from Python list"""
        self.words_to_find = json.dumps(value)

    @property
    def found_words_list(self):
        """Get found words as Python list"""
        return json.loads(self.found_words) if self.found_words else []

    @found_words_list.setter
    def found_words_list(self, value):
        """Set found words from Python list"""
        self.found_words = json.dumps(value)

    def calculate_score(self):
        """Calculate score based on found words and time taken"""
        if not self.end_time:
            return 0

        total_words = len(self.words)
        found_count = len(self.found_words_list)

        if total_words == 0:
            return 0

        # Base score: percentage of words found
        completion_ratio = found_count / total_words
        base_score = int(completion_ratio * 1000)  # Max 1000 points for completion

        # Time bonus (faster completion = more points)
        if self.time_taken:
            time_bonus = max(0, 300 - self.time_taken)  # 5-minute max, decrease bonus over time
        else:
            time_bonus = 0

        # Level multiplier
        level_multiplier = {1: 1.0, 2: 1.5, 3: 2.0}.get(self.level, 1.0)

        final_score = int((base_score + time_bonus) * level_multiplier)
        self.score = final_score
        return final_score

    def end_game(self):
        """Mark game as completed and calculate score"""
        self.end_time = datetime.utcnow()
        self.is_completed = True

        # Calculate time taken in seconds
        if self.start_time and self.end_time:
            self.time_taken = (self.end_time - self.start_time).total_seconds()

        self.calculate_score()

        # Create score record
        from models.score import Score
        score_record = Score(
            user_id=self.user_id,
            game_session_id=self.id,
            score=self.score,
            level=self.level,
            words_found=len(self.found_words_list),
            total_words=len(self.words),
            time_taken=self.time_taken
        )
        db.session.add(score_record)

    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'level': self.level,
            'grid_size': self.grid_size,
            'grid': self.grid,
            'words_to_find': self.words,
            'found_words': self.found_words_list,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'is_completed': self.is_completed,
            'time_taken': self.time_taken,
            'score': self.score,
            'progress': f"{len(self.found_words_list)}/{len(self.words)}"
        }