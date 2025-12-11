from app import create_app
from database.db import db
from models.user import User
from models.word import Word
from models.achievement import Achievement

app = create_app()

def seed_database():
    """Master seed script to initialize the database with all required data."""
    with app.app_context():
        print("🌱 Starting database seeding...")
        
        # 1. Create Tables
        db.create_all()
        print("✅ Database tables created.")

        # --- SEED 1: ADMIN USER ---
        admin_email = "admin@findtheword.com"
        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                username="SuperAdmin",
                email=admin_email,
                is_admin=True
            )
            admin.set_password("Admin123!")
            db.session.add(admin)
            print("✅ Admin user created.")
        else:
            print("ℹ️  Admin user already exists.")

        # --- SEED 2: ACHIEVEMENTS ---
        achievements_data = [
            # Score
            {'name': 'Bronze Scorer', 'description': 'Reach 500 total points', 'icon': '🥉', 'category': 'score', 'threshold': 500},
            {'name': 'Silver Scorer', 'description': 'Reach 1000 total points', 'icon': '🥈', 'category': 'score', 'threshold': 1000},
            {'name': 'Gold Scorer', 'description': 'Reach 2000 total points', 'icon': '🥇', 'category': 'score', 'threshold': 2000},
            
            # Games Played
            {'name': 'Getting Started', 'description': 'Play 10 games', 'icon': '🎮', 'category': 'games', 'threshold': 10},
            {'name': 'Marathon Player', 'description': 'Play 50 games', 'icon': '🏃', 'category': 'games', 'threshold': 50},
            {'name': 'Expert Player', 'description': 'Play 100 games', 'icon': '👑', 'category': 'games', 'threshold': 100},
            
            # Special
            {'name': 'Perfectionist', 'description': 'Complete a game with 100% words found', 'icon': '💯', 'category': 'perfect', 'threshold': 1},
            
            # Difficulty Mastery
            {'name': 'Easy Master', 'description': 'Complete 10 Easy games', 'icon': '✅', 'category': 'completion_easy', 'threshold': 10},
            {'name': 'Medium Master', 'description': 'Complete 10 Medium games', 'icon': '✅✅', 'category': 'completion_medium', 'threshold': 10},
            {'name': 'Hard Master', 'description': 'Complete 10 Hard games', 'icon': '✅✅✅', 'category': 'completion_hard', 'threshold': 10},
        ]

        new_achievements = 0
        for data in achievements_data:
            if not Achievement.query.filter_by(name=data['name']).first():
                ach = Achievement(**data)
                db.session.add(ach)
                new_achievements += 1
        
        if new_achievements > 0:
            print(f"✅ Added {new_achievements} new achievements.")
        else:
            print("ℹ️  Achievements already exist.")

        # --- SEED 3: SAMPLE WORDS ---
        if Word.query.count() == 0:
            sample_words = [
                # Easy
                Word(word="PYTHON", definition="Popular programming language", difficulty="easy", length=6, category="technology", example="I code in Python.", trivia="Python is named after Monty Python."),
                Word(word="COMPUTER", definition="Electronic device for processing data", difficulty="easy", length=8, category="technology", example="Turn on the computer.", trivia="The first computer bug was a real moth."),
                Word(word="INTERNET", definition="Global network of computers", difficulty="easy", length=8, category="technology", example="Surf the internet.", trivia="The internet started as ARPANET."),
                
                # Medium
                Word(word="ELEPHANT", definition="Large mammal with a trunk", difficulty="medium", length=8, category="animals", example="The elephant trumpeted.", trivia="Elephants can't jump."),
                Word(word="DATABASE", definition="Organized collection of data", difficulty="medium", length=8, category="technology", example="Query the database.", trivia="SQL stands for Structured Query Language."),
                
                # Hard
                Word(word="ALGORITHM", definition="Step-by-step procedure", difficulty="hard", length=9, category="technology", example="The algorithm is efficient.", trivia="The word comes from Al-Khwarizmi."),
                Word(word="CRYPTOLOGY", definition="Study of secret codes", difficulty="hard", length=10, category="technology", example="Cryptology keeps data safe.", trivia="Enigma was a famous cipher machine."),
                
                # New Category Test
                Word(word="NEBULA", definition="A giant cloud of dust and gas in space.", category="space", difficulty="medium", length=6, example="The Orion Nebula is visible.", trivia="Nebulae are star nurseries.")
            ]

            for word in sample_words:
                db.session.add(word)
            print(f"✅ Added {len(sample_words)} sample words.")
        else:
            print("ℹ️  Words database already populated.")

        # Final Commit
        db.session.commit()
        print("✨ Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()