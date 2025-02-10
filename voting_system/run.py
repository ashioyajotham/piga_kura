from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from config.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    
    from app.api.auth import auth_bp
    from app.api.voter import voter_bp
    from app.api.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(voter_bp, url_prefix='/voter')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True)
