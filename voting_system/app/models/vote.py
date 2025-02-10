from app import db
from datetime import datetime
from cryptography.fernet import Fernet
import os

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ballot_id = db.Column(db.Integer, db.ForeignKey('ballot.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    encrypted_vote = db.Column(db.Text, nullable=False)
    
    @staticmethod
    def encrypt_vote(vote_data):
        key = os.environ.get('VOTE_ENCRYPTION_KEY').encode()
        f = Fernet(key)
        return f.encrypt(str(vote_data).encode()).decode()
    
    @staticmethod
    def decrypt_vote(encrypted_data):
        key = os.environ.get('VOTE_ENCRYPTION_KEY').encode()
        f = Fernet(key)
        return f.decrypt(encrypted_data.encode()).decode()
