import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from flask_socketio import SocketIO

app = create_app()
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app, debug=True)
