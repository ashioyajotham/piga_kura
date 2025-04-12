from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app.services.voting import VotingService

voter_bp = Blueprint('voter_api', __name__)

@voter_bp.route('/vote', methods=['POST'])
@login_required
def cast_vote():
    data = request.get_json()
    try:
        vote = VotingService.cast_vote(
            user_id=current_user.id,
            ballot_id=data['ballot_id'],
            candidate_id=data['candidate_id']
        )
        return jsonify({'message': 'Vote cast successfully', 'receipt': vote.encrypted_vote}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing your vote'}), 500

@voter_bp.route('/ballots', methods=['GET'])
@login_required
def get_active_ballots():
    from app.models.ballot import Ballot
    from datetime import datetime
    
    active_ballots = Ballot.query.filter(
        Ballot.is_active == True,
        Ballot.start_date <= datetime.utcnow(),
        Ballot.end_date >= datetime.utcnow()
    ).all()
    
    return jsonify({
        'ballots': [ballot.to_dict() for ballot in active_ballots]
    })
