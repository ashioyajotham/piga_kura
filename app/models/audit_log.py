from app import db
from datetime import datetime

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ballot_id = db.Column(db.Integer, db.ForeignKey('ballot.id'))
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    details = db.Column(db.Text)
    
    def __repr__(self):
        return f'<AuditLog {self.action} at {self.timestamp}>'
