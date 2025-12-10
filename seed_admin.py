from app import create_app
from database.db import db
from models.user import User

app = create_app()

def seed_admin():
    with app.app_context():
        # 1. Check if admin already exists
        admin_email = "admin@findtheword.com"
        existing_user = User.query.filter_by(email=admin_email).first()
        
        if existing_user:
            print(f"User {admin_email} already exists!")
            
            # Optional: If they exist but aren't admin, upgrade them
            if not existing_user.is_admin:
                existing_user.is_admin = True
                db.session.commit()
                print(f"Updated {existing_user.username} to Admin.")
            return

        # 2. Create new Admin User
        admin = User(
            username="SuperAdmin",
            email=admin_email,
            is_admin=True  # This is the important part!
        )
        
        # 3. Set Password
        admin.set_password("Admin123!") 
        
        # 4. Save to DB
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print("Email: admin@findtheword.com")
        print("Password: Admin123!")

if __name__ == "__main__":
    seed_admin()