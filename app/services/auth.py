from flask import current_app
from app.models.user import User
from app import db
import jwt
from datetime import datetime, timedelta

class AuthService:
    @staticmethod
    def register_user(email, voter_id, password, is_official=False):
        if not User.verify_email_domain(email):
            raise ValueError("Invalid email domain. Must be @kabarak.ac.ke")
        
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already registered")
        
        if User.query.filter_by(voter_id=voter_id).first():
            raise ValueError("Voter ID already registered")
            
        user = User(
            email=email, 
            voter_id=voter_id,
            is_official=is_official,
            # Officials start unverified until admin approves
            is_verified=(not is_official)
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def verify_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None
