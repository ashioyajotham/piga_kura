from flask import Blueprint, render_template, redirect, url_for, abort, request, flash
from flask_login import current_user, login_required
from app.models.ballot import Ballot
from app.models.vote import Vote
from datetime import datetime

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
        return redirect(url_for('voter.vote_success', vote_id=existing_vote.id))
    
    # Check if ballot is active
    if not ballot.is_ongoing:
        abort(403, "This ballot is not currently active")
    
    return render_template('voter/vote.html', ballot=ballot)

@voter_bp.route('/my-votes')
@login_required
def my_votes():
    votes = Vote.query.filter_by(voter_id=current_user.id).all()
    return render_template('voter/my_votes.html', votes=votes)

@voter_bp.route('/vote/success')
@login_required
def vote_success():
    vote_id = request.args.get('vote_id')
    vote = Vote.query.filter_by(id=vote_id, voter_id=current_user.id).first_or_404()
    return render_template('voter/vote_success.html', vote=vote)
