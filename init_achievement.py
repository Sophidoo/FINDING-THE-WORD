from app import create_app
from database.db import db
from models.achievement import Achievement

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()

    achievements = [
        Achievement(name='Bronze Scorer', description='Reach 500 total points', icon='🥉', category='score',
                    threshold=500),
        Achievement(name='Silver Scorer', description='Reach 1000 total points', icon='🥈', category='score',
                    threshold=1000),
        Achievement(name='Gold Scorer', description='Reach 2000 total points', icon='🥇', category='score',
                    threshold=2000),
        Achievement(name='Getting Started', description='Play 10 games', icon='🎮', category='games', threshold=10),
        Achievement(name='Marathon Player', description='Play 50 games', icon='🏃', category='games', threshold=50),
        Achievement(name='Expert Player', description='Play 100 games', icon='👑', category='games', threshold=100),
        Achievement(name='Perfectionist', description='Complete a game with 100% words found', icon='💯',
                    category='perfect', threshold=1),
        Achievement(
            name='Easy Master',
            description='Complete 10 Easy games',
            icon='✅',
            category='completion_easy',
            threshold=10
        ),
        Achievement(
            name='Medium Master',
            description='Complete 10 Medium games',
            icon='✅✅',
            category='completion_medium',
            threshold=10
        ),
        Achievement(
            name='Hard Master',
            description='Complete 10 Hard games',
            icon='✅✅✅',
            category='completion_hard',
            threshold=10
        ),
    ]

    print("Adding achievements...")

    for a in achievements:
        exists = Achievement.query.filter_by(name=a.name).first()
        if not exists:
            db.session.add(a)

    db.session.commit()
    print("Done! Database updated.")