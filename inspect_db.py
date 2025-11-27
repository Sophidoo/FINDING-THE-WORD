from app import create_app, db
from models.user import User
from models.word import Word
from models.game import GameSession
from models.score import Score
from models.feedback import Feedback

app = create_app()

with app.app_context():
    print("=== DATABASE INSPECTION ===")

    # List all tables (updated method)
    print("\n📊 TABLES:")
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    for table in tables:
        print(f"  - {table}")

    # Count records in each table
    print("\n📈 RECORD COUNTS:")
    try:
        print(f"  Users: {User.query.count()}")
    except Exception as e:
        print(f"  Users: Error - {e}")

    try:
        print(f"  Words: {Word.query.count()}")
    except Exception as e:
        print(f"  Words: Error - {e}")

    try:
        print(f"  Game Sessions: {GameSession.query.count()}")
    except Exception as e:
        print(f"  Game Sessions: Error - {e}")

    try:
        print(f"  Scores: {Score.query.count()}")
    except Exception as e:
        print(f"  Scores: Error - {e}")

    try:
        print(f"  Feedback: {Feedback.query.count()}")
    except Exception as e:
        print(f"  Feedback: Error - {e}")

    # Show sample data
    print("\n👥 SAMPLE USERS:")
    try:
        users = User.query.limit(3).all()
        for user in users:
            print(f"  - {user.username} ({user.email}) - Admin: {user.is_admin}")
    except Exception as e:
        print(f"  Error loading users: {e}")

    print("\n📝 SAMPLE WORDS:")
    try:
        words = Word.query.limit(5).all()
        for word in words:
            print(f"  - {word.word} ({word.difficulty}) - {word.definition[:30]}...")
    except Exception as e:
        print(f"  Error loading words: {e}")

if __name__ == '__main__':
    print("Database inspection complete!")