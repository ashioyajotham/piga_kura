from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.api.auth import auth_bp as auth_api_bp
    from app.api.voter import voter_bp
    from app.api.admin import admin_bp
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp as auth_web_bp
    
    app.register_blueprint(auth_api_bp, url_prefix='/api/auth', name='auth_api')
    app.register_blueprint(voter_bp, url_prefix='/api/voter')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_web_bp, url_prefix='/auth')
    
    # Register CLI commands
    from app import cli
    cli.init_app(app)
    
    return app
