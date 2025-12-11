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
                # --- EASY (3-4 Letters) ---
                Word(word="CAT", definition="A small domesticated carnivorous mammal.", difficulty="easy", length=3, category="animals", example="The cat meowed loudly.", trivia="Cats sleep for 70% of their lives."),
                Word(word="DOG", definition="A domesticated carnivorous mammal.", difficulty="easy", length=3, category="animals", example="The dog chased the ball.", trivia="Dogs have a sense of time."),
                Word(word="SUN", definition="The star around which the earth orbits.", difficulty="easy", length=3, category="nature", example="The sun is shining today.", trivia="The sun accounts for 99.86% of the mass in the solar system."),
                Word(word="CODE", definition="Program instructions.", difficulty="easy", length=4, category="technology", example="I write code every day.", trivia="Ada Lovelace is considered the first computer programmer."),
                Word(word="JAVA", definition="A high-level programming language.", difficulty="easy", length=4, category="technology", example="Java is used for Android apps.", trivia="Java was originally named Oak."),
                Word(word="LION", definition="A large cat of the genus Panthera.", difficulty="easy", length=4, category="animals", example="The lion is the king of the jungle.", trivia="A lion's roar can be heard from 5 miles away."),
                Word(word="MOON", definition="The natural satellite of the earth.", difficulty="easy", length=4, category="nature", example="The moon is full tonight.", trivia="The moon is drifting away from Earth."),
                Word(word="CAKE", definition="A sweet baked food.", difficulty="easy", length=4, category="food", example="We ate cake for his birthday.", trivia="The first cakes were very different from what we eat today."),
                Word(word="BLUE", definition="A color intermediate between green and violet.", difficulty="easy", length=4, category="colors", example="The sky is blue.", trivia="Blue is the most popular favorite color globally."),
                Word(word="BOOK", definition="A written or printed work consisting of pages.", difficulty="easy", length=4, category="objects", example="I am reading a good book.", trivia="The longest book in the world is 'Remembrance of Things Past'."),

                # --- MEDIUM (5-6 Letters) ---
                Word(word="APPLE", definition="The round fruit of a tree.", difficulty="medium", length=5, category="food", example="An apple a day keeps the doctor away.", trivia="Apples float because they are 25% air."),
                Word(word="TIGER", definition="A very large solitary cat.", difficulty="medium", length=5, category="animals", example="The tiger has stripes.", trivia="No two tigers have the same stripes."),
                Word(word="EARTH", definition="The planet on which we live.", difficulty="medium", length=5, category="nature", example="Earth is the third planet from the sun.", trivia="Earth is the only planet not named after a god."),
                Word(word="MOUSE", definition="A small handheld device used to control a cursor.", difficulty="medium", length=5, category="technology", example="Click the mouse button.", trivia="The first computer mouse was made of wood."),
                Word(word="CLOUD", definition="A visible mass of condensed water vapor.", difficulty="medium", length=5, category="nature", example="Look at that fluffy cloud.", trivia="A cumulus cloud can weigh more than 1 million pounds."),
                Word(word="PLANET", definition="A celestial body moving in an elliptical orbit.", difficulty="medium", length=6, category="space", example="Mars is a planet.", trivia="Mercury is the smallest planet in our solar system."),
                Word(word="PYTHON", definition="A popular programming language.", difficulty="medium", length=6, category="technology", example="Python is great for data science.", trivia="Python is named after the comedy group Monty Python."),
                Word(word="ORANGE", definition="A round juicy citrus fruit.", difficulty="medium", length=6, category="food", example="I drank orange juice.", trivia="The color orange was named after the fruit."),
                Word(word="FOREST", definition="A large area covered chiefly with trees.", difficulty="medium", length=6, category="nature", example="We hiked through the forest.", trivia="Forests cover 31% of the global land area."),
                Word(word="ROBOT", definition="A machine capable of carrying out a complex series of actions.", difficulty="medium", length=5, category="technology", example="The robot assembled the car.", trivia="The word 'robot' comes from the Czech word 'robota' meaning forced labor."),

                # --- HARD (7+ Letters) ---
                Word(word="GIRAFFE", definition="A large African mammal with a very long neck.", difficulty="hard", length=7, category="animals", example="The giraffe ate leaves from the tall tree.", trivia="A giraffe's tongue can be up to 20 inches long."),
                Word(word="JUPITER", definition="The largest planet in the solar system.", difficulty="hard", length=7, category="space", example="Jupiter is a gas giant.", trivia="Jupiter has over 75 moons."),
                Word(word="RAINBOW", definition="An arch of colors formed in the sky.", difficulty="hard", length=7, category="nature", example="I saw a rainbow after the rain.", trivia="You can never actually reach the end of a rainbow."),
                Word(word="INTERNET", definition="A global computer network.", difficulty="hard", length=8, category="technology", example="I surfed the internet.", trivia="The internet was originally called ARPANET."),
                Word(word="COMPUTER", definition="An electronic device for storing and processing data.", difficulty="hard", length=8, category="technology", example="My computer is very fast.", trivia="The first computer bug was an actual moth."),
                Word(word="ELEPHANT", definition="A heavy plant-eating mammal with a trunk.", difficulty="hard", length=8, category="animals", example="The elephant is the largest land animal.", trivia="Elephants are the only mammals that can't jump."),
                Word(word="DATABASE", definition="A structured set of data held in a computer.", difficulty="hard", length=8, category="technology", example="The database stores user info.", trivia="SQL is the standard language for relational databases."),
                Word(word="ASTRONAUT", definition="A person trained to travel in a spacecraft.", difficulty="hard", length=9, category="space", example="The astronaut walked on the moon.", trivia="The word astronaut comes from Greek words meaning 'star sailor'."),
                Word(word="CHOCOLATE", definition="A food preparation in the form of a paste or solid block made from cacao seeds.", difficulty="hard", length=9, category="food", example="I love dark chocolate.", trivia="White chocolate isn't technically chocolate."),
                Word(word="BUTTERFLY", definition="A nectar-feeding insect with two pairs of large wings.", difficulty="hard", length=9, category="animals", example="The butterfly landed on the flower.", trivia="Butterflies taste with their feet.")
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