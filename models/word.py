from database.db import db


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False)
    definition = db.Column(db.Text)
    example = db.Column(db.Text)
    trivia = db.Column(db.Text)
    difficulty = db.Column(db.String(20), default='easy')  # easy, medium, hard
    length = db.Column(db.Integer)
    category = db.Column(db.String(50))  # animals, food, etc.

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'definition': self.definition,
            'difficulty': self.difficulty,
            'length': self.length,
            'category': self.category,
            'example': self.example,
            'trivia': self.trivia
        }