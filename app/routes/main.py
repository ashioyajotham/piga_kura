from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app.models.ballot import Ballot
from app.models.vote import Vote
from app.models.user import User
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        user_role = 'admin' if current_user.is_admin else 'official' if current_user.is_official else 'voter'
        active_ballots_count = Ballot.query.filter_by(is_active=True).count()
        
        # Add admin-specific data
        if current_user.is_admin:
            user_count = User.query.count()
            vote_count = Vote.query.count()
            return render_template('index.html', 
                                 user_role=user_role, 
                                 active_ballots_count=active_ballots_count,
                                 user_count=user_count,
                                 vote_count=vote_count)
        
        return render_template('index.html', 
                             user_role=user_role, 
                             active_ballots_count=active_ballots_count)
    else:
        return render_template('landing.html')

def get_user_role():
    """Helper function to determine user role for UI customization"""
    if not current_user.is_authenticated:
        return "guest"
    if current_user.is_admin:
        return "admin"
    if current_user.is_official:
        return "official"
    return "voter"

@main_bp.route('/verify-vote')
def verify_vote():
    return render_template('verify_vote.html')

@main_bp.route('/verify-vote/check', methods=['POST'])
def check_vote():
    vote_id = request.form.get('vote_id')
    receipt = request.form.get('receipt')
    
    if not vote_id or not receipt:
        flash('Please provide all required information', 'danger')
        return redirect(url_for('main.verify_vote'))
    
    vote = Vote.query.get(vote_id)
    if not vote:
        flash('Vote not found', 'danger')
        return redirect(url_for('main.verify_vote'))
        
    if vote.encrypted_vote == receipt:
        return render_template('vote_verified.html', vote=vote)
    else:
        flash('Invalid receipt', 'danger')
        return redirect(url_for('main.verify_vote'))

@main_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main_bp.route('/security')
def security():
    return render_template('security.html')

@main_bp.route('/help')
def help():
    return render_template('help.html')
