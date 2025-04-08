from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.ballot import Ballot
from app.models.user import User
from app.models.vote import Vote
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin privileges required', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    ballots = Ballot.query.order_by(Ballot.created_at.desc()).all()
    user_count = User.query.count()
    vote_count = Vote.query.count()
    return render_template('admin/dashboard.html', 
                          ballots=ballots, 
                          user_count=user_count, 
                          vote_count=vote_count)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/ballots')
@login_required
@admin_required
def ballots():
    ballots = Ballot.query.all()
    return render_template('admin/ballots.html', ballots=ballots)
