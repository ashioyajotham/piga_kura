from datetime import datetime
from app import db
import hashlib

class Ballot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    candidates = db.relationship('Candidate', backref='ballot', lazy=True)
    votes = db.relationship('Vote', backref='ballot', lazy=True)
    ballot_type = db.Column(db.String(50), nullable=False)  # national, county, special
    verification_key = db.Column(db.String(64), unique=True)
    min_voters = db.Column(db.Integer, default=0)
    max_voters = db.Column(db.Integer)
    requires_verification = db.Column(db.Boolean, default=True)
    verification_method = db.Column(db.String(50))  # id, biometric, token
    audit_trail = db.relationship('AuditLog', backref='ballot', lazy=True)

    @property
    def is_ongoing(self):
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date and self.is_active

    def generate_verification_hash(self):
        """Generate a unique verification hash for the ballot"""
        timestamp = datetime.utcnow().isoformat()
        data = f"{self.id}{self.title}{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()

    @property
    def vote_count(self):
        return sum(c.vote_count for c in self.candidates)

    @property
    def is_quorum_reached(self):
        return self.vote_count >= self.min_voters if self.min_voters > 0 else True

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'is_active': self.is_active,
            'is_ongoing': self.is_ongoing,
            'candidates': [c.to_dict() for c in self.candidates],
            'ballot_type': self.ballot_type,
            'verification_required': self.requires_verification,
            'verification_method': self.verification_method,
            'vote_count': self.vote_count,
            'quorum_reached': self.is_quorum_reached,
            'remaining_time': (self.end_date - datetime.utcnow()).total_seconds() if self.is_ongoing else 0
        }
