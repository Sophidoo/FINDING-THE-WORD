from app import create_app, db
# from models.feedback import Feedback


def init_database():
    """Initialize the database with all tables"""
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")

        # Optional: Add some sample data
        from models.word import Word

        # Check if words already exist to avoid duplicates
        if Word.query.count() == 0:
            sample_words = [
                # EASY words (short, very common, lots of vowels/consonants people expect)
                Word(word="PYTHON", definition="Popular programming language", difficulty="easy", length=6,
                     category="technology"),
                Word(word="COMPUTER", definition="Electronic device for processing data", difficulty="easy", length=8,
                     category="technology"),
                Word(word="VARIABLE", definition="Named storage for data", difficulty="easy", length=8,
                     category="technology"),
                Word(word="FUNCTION", definition="Reusable block of code", difficulty="easy", length=8,
                     category="technology"),
                Word(word="INTERNET", definition="Global network of computers", difficulty="easy", length=8,
                     category="technology"),

                # MEDIUM words (7–9 letters, moderately common)
                Word(word="ELEPHANT", definition="Large mammal with a trunk", difficulty="medium", length=8,
                     category="animals"),
                Word(word="BUTTERFLY", definition="Insect with colorful wings", difficulty="medium", length=9,
                     category="animals"),
                Word(word="JAVASCRIPT", definition="Web scripting language", difficulty="medium", length=10,
                     category="technology"),
                Word(word="DATABASE", definition="Organized collection of data", difficulty="medium", length=8,
                     category="technology"),
                Word(word="KEYBOARD", definition="Input device with keys", difficulty="medium", length=8,
                     category="technology"),

                # HARD words (longer, rarer letters, or tricky spelling)
                Word(word="ALGORITHM", definition="Step-by-step procedure", difficulty="hard", length=9,
                     category="technology"),
                Word(word="CRYPTOLOGY", definition="Study of secret codes", difficulty="hard", length=10,
                     category="technology"),
                Word(word="HIPPOCAMPU", definition="Part of the brain (hippocampus)", difficulty="hard", length=11,
                     category="science"),
                Word(word="JAZZ", definition="Music genre with improvisation", difficulty="hard", length=4,
                     category="music"),  # short but rare letters (J,Z)
                Word(word="QUICKFOX", definition="The quick brown fox (phrase)", difficulty="hard", length=8,
                     category="fun")
            ]

            for word in sample_words:
                db.session.add(word)

            db.session.commit()
            print("✅ Sample words added to database!")
        else:
            print("ℹ️  Database already contains data, skipping sample words.")


if __name__ == '__main__':
    init_database()