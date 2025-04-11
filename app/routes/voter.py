from flask import Blueprint, render_template, redirect, url_for, abort, request, flash, jsonify
from flask_login import current_user, login_required
from app.models.ballot import Ballot
from app.models.vote import Vote
from app.services.voting import VotingService
from app.models.audit_log import AuditLog
from datetime import datetime
from app import db

voter_bp = Blueprint('voter', __name__)

@voter_bp.route('/active-ballots')
@login_required
def active_ballots():
    ballots = Ballot.query.filter(
        Ballot.is_active == True,
        Ballot.start_date <= datetime.utcnow(),
        Ballot.end_date >= datetime.utcnow()
    ).all()
    return render_template('voter/active_ballots.html', ballots=ballots)

@voter_bp.route('/ballot/<int:ballot_id>')
@login_required
def view_ballot(ballot_id):
    ballot = Ballot.query.get_or_404(ballot_id)
    
    # Check if user already voted
    existing_vote = Vote.query.filter_by(voter_id=current_user.id, ballot_id=ballot_id).first()
    if existing_vote:
        flash('You have already voted in this election', 'warning')
        return redirect(url_for('voter.vote_success', vote_id=existing_vote.id))
    
    # Check if ballot is active
    if not ballot.is_ongoing:
        flash('This election is not currently active', 'danger')
        return redirect(url_for('voter.active_ballots'))
    
    return render_template('voter/vote.html', ballot=ballot)

@voter_bp.route('/vote', methods=['POST'])
@login_required
def cast_vote():
    """API endpoint to cast a vote"""
    data = request.get_json()
    
    if not data or 'candidate_id' not in data or 'ballot_id' not in data:
        return jsonify({'error': 'Missing required data'}), 400
    
    try:
        vote = VotingService.cast_vote(
            user_id=current_user.id,
            ballot_id=data['ballot_id'],
            candidate_id=data['candidate_id']
        )
        
        # Log the voting action
        audit = AuditLog(
            action="vote_cast",
            user_id=current_user.id,
            ballot_id=data['ballot_id'],
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            details=f"Vote cast for candidate ID {data['candidate_id']}"
        )
        db.session.add(audit)
        db.session.commit()
        
        return jsonify({
            'message': 'Vote cast successfully',
            'vote_id': vote.id,
            'receipt': vote.encrypted_vote
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Vote error: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your vote'}), 500

@voter_bp.route('/my-votes')
@login_required
def my_votes():
    votes = Vote.query.filter_by(voter_id=current_user.id).all()
    return render_template('voter/my_votes.html', votes=votes)

@voter_bp.route('/vote/success')
@login_required
def vote_success():
    vote_id = request.args.get('vote_id')
    if not vote_id:
        return redirect(url_for('voter.active_ballots'))
        
    vote = Vote.query.filter_by(id=vote_id, voter_id=current_user.id).first_or_404()
    return render_template('voter/vote_success.html', vote=vote)
