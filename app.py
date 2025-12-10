from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config
from database.db import db

# Initialize extensions first (without app)
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'authBlueprint.login'  # optional but recommended
    login_manager.login_message_category = 'info'

    # Import and register blueprints inside create_app
    from routes.auth_bp import authBlueprint
    from routes.feedback_bp import feedbackBlueprint
    from routes.game_bp import gameBlueprint
    from routes.leaderboard_bp import leaderboardBlueprint
    from routes.main_bp import mainBlueprint
    from routes.words_bp import wordsBlueprint
    from routes.achievement_bp import achievementBlueprint

    app.register_blueprint(mainBlueprint, url_prefix="/")
    app.register_blueprint(authBlueprint, url_prefix="/api/auth")
    app.register_blueprint(feedbackBlueprint, url_prefix="/api/feedback")
    app.register_blueprint(leaderboardBlueprint, url_prefix="/api/leaderboard")  # Fixed typo: url_pefix -> url_prefix
    app.register_blueprint(gameBlueprint, url_prefix="/api/game")  # Fixed typo
    app.register_blueprint(wordsBlueprint, url_prefix="/api/words")  # Fixed typo
    app.register_blueprint(achievementBlueprint, url_prefix="/api/achievements")  # Fixed typo

    @app.cli.command("init-db")
    def init_db_command():
        """Create all database tables."""
        with app.app_context():
            db.create_all()
            print("Database initialized successfully!")
    return app

app = create_app()

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)