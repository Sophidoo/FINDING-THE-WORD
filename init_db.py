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
                Word(word="PYTHON", definition="A programming language", difficulty="easy", length=6,
                     category="technology"),
                Word(word="JAVASCRIPT", definition="A scripting language", difficulty="medium", length=10,
                     category="technology"),
                Word(word="DATABASE", definition="Structured data storage", difficulty="medium", length=8,
                     category="technology"),
                Word(word="ALGORITHM", definition="Step-by-step procedure", difficulty="hard", length=9,
                     category="technology"),
                Word(word="FUNCTION", definition="Reusable code block", difficulty="easy", length=8,
                     category="technology"),
                Word(word="VARIABLE", definition="Storage for data values", difficulty="easy", length=8,
                     category="technology"),
                Word(word="FUNCTION", definition="Reusable code block", difficulty="easy", length=8,
                     category="technology"),
                Word(word="ELEPHANT", definition="Large mammal with trunk", difficulty="medium", length=8,
                     category="animals"),
                Word(word="BUTTERFLY", definition="Flying insect with colorful wings", difficulty="hard", length=9,
                     category="animals"),
                Word(word="COMPUTER", definition="Electronic device for processing data", difficulty="easy", length=8,
                     category="technology")
            ]

            for word in sample_words:
                db.session.add(word)

            db.session.commit()
            print("✅ Sample words added to database!")
        else:
            print("ℹ️  Database already contains data, skipping sample words.")


if __name__ == '__main__':
    init_database()