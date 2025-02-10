from app import db
from app.models.vote import Vote
from app.models.ballot import Ballot
from app.models.candidate import Candidate
from datetime import datetime

class VotingService:
    @staticmethod
    def cast_vote(user_id, ballot_id, candidate_id):
        ballot = Ballot.query.get_or_404(ballot_id)
        if not ballot.is_ongoing:
            raise ValueError("Voting is not active for this ballot")
            
        existing_vote = Vote.query.filter_by(
            voter_id=user_id,
            ballot_id=ballot_id
        ).first()
        
        if existing_vote:
            raise ValueError("User has already voted in this ballot")
            
        vote_data = {
            'voter_id': user_id,
            'candidate_id': candidate_id,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        encrypted_vote = Vote.encrypt_vote(vote_data)
        vote = Vote(
            voter_id=user_id,
            ballot_id=ballot_id,
            candidate_id=candidate_id,
            encrypted_vote=encrypted_vote
        )
        
        db.session.add(vote)
        db.session.commit()
        return vote

    @staticmethod
    def get_results(ballot_id):
        results = db.session.query(
            Candidate.name,
            db.func.count(Vote.id).label('vote_count')
        ).join(Vote).filter(Vote.ballot_id == ballot_id)\
         .group_by(Candidate.id).all()
        
        return [{'candidate': r[0], 'votes': r[1]} for r in results]
