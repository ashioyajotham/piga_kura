from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.models.ballot import Ballot
from app.models.candidate import Candidate
from app.models.vote import Vote
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin_api', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/ballots', methods=['POST'])
@login_required
@admin_required
def create_ballot():
    data = request.get_json()
    
    try:
        ballot = Ballot(
            title=data['title'],
            description=data['description'],
            start_date=datetime.fromisoformat(data['start_date']),
            end_date=datetime.fromisoformat(data['end_date']),
            ballot_type=data['ballot_type'],
            min_voters=data.get('min_voters', 0),
            max_voters=data.get('max_voters'),
            requires_verification=data.get('requires_verification', True),
            verification_method=data.get('verification_method', 'id')
        )
        
        ballot.verification_key = ballot.generate_verification_hash()
        
        db.session.add(ballot)
        db.session.commit()
        
        return jsonify({'message': 'Ballot created', 'id': ballot.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/ballots/<int:ballot_id>/candidates', methods=['POST'])
@login_required
@admin_required
def add_candidate(ballot_id):
    data = request.get_json()
    
    try:
        candidate = Candidate(
            name=data['name'],
            position=data['position'],
            manifesto=data.get('manifesto', ''),
            photo_url=data.get('photo_url', ''),
            ballot_id=ballot_id
        )
        
        db.session.add(candidate)
        db.session.commit()
        
        return jsonify({'message': 'Candidate added', 'id': candidate.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/votes/count', methods=['GET'])
@login_required
@admin_required
def get_vote_count():
    ballot_id = request.args.get('ballot_id')
    
    if ballot_id:
        results = db.session.query(
            Vote.candidate_id, 
            db.func.count(Vote.id)
        ).filter(Vote.ballot_id == ballot_id).group_by(Vote.candidate_id).all()
        
        votes = {str(candidate_id): count for candidate_id, count in results}
        return jsonify({'votes': votes})
    else:
        return jsonify({'error': 'Ballot ID required'}), 400
