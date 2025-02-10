from datetime import datetime
from app import db

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

    @property
    def is_ongoing(self):
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date and self.is_active
