from app import create_app, db
from models.user import User

app = create_app()

with app.app_context():
    print("🔧 Testing database connection...")

    try:
        # Test database connection
        users = User.query.all()
        print(f"✅ Database connected! Found {len(users)} users")

        # Test creating a user
        test_user = User.query.filter_by(username='test').first()
        if not test_user:
            test_user = User(username='test', email='test@test.com')
            test_user.set_password('test123')
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created successfully!")
        else:
            print("✅ Test user already exists!")

    except Exception as e:
        print(f"❌ Error: {e}")