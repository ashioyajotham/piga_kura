from app import db

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    manifesto = db.Column(db.Text)
    photo_url = db.Column(db.String(200))
    ballot_id = db.Column(db.Integer, db.ForeignKey('ballot.id'), nullable=False)
    votes = db.relationship('Vote', backref='candidate', lazy=True)

    @property
    def vote_count(self):
        """Get the number of votes for this candidate"""
        return len(self.votes)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'manifesto': self.manifesto,
            'photo_url': self.photo_url,
            'vote_count': self.vote_count
        }
