from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.ballot import Ballot
from app.models.candidate import Candidate
from functools import wraps

official_bp = Blueprint('official', __name__)

def official_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'is_official') or not current_user.is_official:
            flash('Election official privileges required', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@official_bp.route('/dashboard')
@login_required
@official_required
def dashboard():
    ballots = Ballot.query.order_by(Ballot.created_at.desc()).all()
    return render_template('official/dashboard.html', ballots=ballots)

@official_bp.route('/create-ballot', methods=['GET', 'POST'])
@login_required
@official_required
def create_ballot():
    if request.method == 'POST':
        # Process form data here
        flash('Ballot created successfully', 'success')
        return redirect(url_for('official.dashboard'))
    return render_template('official/create_ballot.html')
