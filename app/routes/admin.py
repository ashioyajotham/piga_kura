from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.ballot import Ballot
from app.models.user import User
from app.models.vote import Vote
from functools import wraps
import json

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

@admin_bp.route('/api/users/<int:user_id>')
@login_required
@admin_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    vote_count = Vote.query.filter_by(voter_id=user_id).count()
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'voter_id': user.voter_id,
        'is_admin': user.is_admin,
        'is_official': user.is_official,
        'is_verified': user.is_verified,
        'created_at': user.created_at.isoformat() if user.created_at else None,
        'vote_count': vote_count
    })

@admin_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@login_required
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    try:
        user.voter_id = data.get('voter_id', user.voter_id)
        user.is_verified = data.get('is_verified', user.is_verified)
        
        # Handle role updates
        role = data.get('role')
        if role:
            user.is_admin = (role == 'admin')
            user.is_official = (role == 'official')
        
        db.session.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/api/users', methods=['POST'])
@login_required
@admin_required
def create_user():
    data = request.get_json()
    
    try:
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        
        if User.query.filter_by(voter_id=data['voter_id']).first():
            return jsonify({'success': False, 'error': 'Voter ID already exists'}), 400
        
        role = data.get('role', 'voter')
        user = User(
            email=data['email'],
            voter_id=data['voter_id'],
            is_admin=(role == 'admin'),
            is_official=(role == 'official'),
            is_verified=data.get('is_verified', True)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'id': user.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting the last admin
    if user.is_admin:
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1:
            return jsonify({'success': False, 'error': 'Cannot delete the last admin'}), 400
    
    try:
        # Note: In production, you might want to soft delete or handle vote references
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/api/users/<int:user_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_official(user_id):
    user = User.query.get_or_404(user_id)
    
    try:
        user.is_verified = True
        db.session.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/api/users/<int:user_id>/verify', methods=['POST'])
@login_required
@admin_required
def toggle_user_verification(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    try:
        user.is_verified = data.get('verified', not user.is_verified)
        db.session.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/api/ballots/<int:ballot_id>')
@login_required
@admin_required
def get_ballot(ballot_id):
    ballot = Ballot.query.get_or_404(ballot_id)
    
    # Calculate vote count safely
    total_votes = Vote.query.filter_by(ballot_id=ballot_id).count()
    
    return jsonify({
        'id': ballot.id,
        'title': ballot.title,
        'description': ballot.description,
        'ballot_type': ballot.ballot_type,
        'start_date': ballot.start_date.isoformat(),
        'end_date': ballot.end_date.isoformat(),
        'is_active': ballot.is_active,
        'is_ongoing': ballot.is_ongoing,
        'vote_count': total_votes,  # Use calculated value instead of ballot.vote_count
        'candidates': [{'id': c.id, 'name': c.name, 'position': c.position} for c in ballot.candidates]
    })

@admin_bp.route('/api/ballots', methods=['POST'])
@login_required
@admin_required
def create_ballot():
    data = request.get_json()
    
    try:
        from datetime import datetime
        ballot = Ballot(
            title=data['title'],
            description=data.get('description', ''),
            ballot_type=data['ballot_type'],
            start_date=datetime.fromisoformat(data['start_date'].replace('T', ' ')),
            end_date=datetime.fromisoformat(data['end_date'].replace('T', ' ')),
            is_active=data.get('is_active', True),
            min_voters=data.get('min_voters', 0),
            max_voters=data.get('max_voters'),
            requires_verification=data.get('requires_verification', True)
        )
        
        db.session.add(ballot)
        db.session.commit()
        
        return jsonify({'success': True, 'id': ballot.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/api/ballots/<int:ballot_id>', methods=['PUT'])
@login_required
@admin_required
def update_ballot(ballot_id):
    ballot = Ballot.query.get_or_404(ballot_id)
    data = request.get_json()
    
    try:
        from datetime import datetime
        ballot.title = data.get('title', ballot.title)
        ballot.description = data.get('description', ballot.description)
        ballot.ballot_type = data.get('ballot_type', ballot.ballot_type)
        ballot.is_active = data.get('is_active', ballot.is_active)
        
        if 'start_date' in data:
            ballot.start_date = datetime.fromisoformat(data['start_date'].replace('T', ' '))
        if 'end_date' in data:
            ballot.end_date = datetime.fromisoformat(data['end_date'].replace('T', ' '))
        
        db.session.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/api/ballots/<int:ballot_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_ballot(ballot_id):
    ballot = Ballot.query.get_or_404(ballot_id)
    
    try:
        # Delete associated votes and candidates
        Vote.query.filter_by(ballot_id=ballot_id).delete()
        db.session.delete(ballot)
        db.session.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/api/ballots/<int:ballot_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_ballot_status(ballot_id):
    ballot = Ballot.query.get_or_404(ballot_id)
    data = request.get_json()
    
    try:
        ballot.is_active = data.get('is_active', not ballot.is_active)
        db.session.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/api/ballots/<int:ballot_id>/results')
@login_required
@admin_required
def get_ballot_results(ballot_id):
    ballot = Ballot.query.get_or_404(ballot_id)
    
    results = []
    total_votes = Vote.query.filter_by(ballot_id=ballot_id).count()
    
    for candidate in ballot.candidates:
        vote_count = Vote.query.filter_by(candidate_id=candidate.id).count()
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        
        results.append({
            'id': candidate.id,
            'name': candidate.name,
            'position': candidate.position,
            'votes': vote_count,
            'percentage': round(percentage, 2)
        })
    
    # Sort by votes descending
    results.sort(key=lambda x: x['votes'], reverse=True)
    
    return jsonify({
        'total_votes': total_votes,
        'candidates': results,
        'ballot_info': {
            'title': ballot.title,
            'type': ballot.ballot_type,
            'start_date': ballot.start_date.isoformat(),
            'end_date': ballot.end_date.isoformat(),
            'is_active': ballot.is_active
        }
    })

@admin_bp.route('/api/ballots/<int:ballot_id>/analytics')
@login_required
@admin_required
def get_ballot_analytics(ballot_id):
    """Get detailed analytics for a ballot"""
    from sqlalchemy import func
    from datetime import datetime, timedelta
    
    ballot = Ballot.query.get_or_404(ballot_id)
    
    # Vote trend over time (if you want to add timestamps to votes)
    vote_trend = db.session.query(
        func.date(Vote.created_at).label('date'),
        func.count(Vote.id).label('count')
    ).filter_by(ballot_id=ballot_id).group_by(
        func.date(Vote.created_at)
    ).all()
    
    # Voter demographics (if you have user profiles)
    # This would depend on your User model structure
    
    analytics_data = {
        'vote_trend': [{'date': str(v.date), 'votes': v.count} for v in vote_trend],
        'total_votes': len(ballot.votes) if hasattr(ballot, 'votes') else 0,
        'candidates_count': len(ballot.candidates),
        'voter_turnout': {
            'percentage': 75.5,  # Calculate based on eligible voters
            'total_eligible': 1000,  # From your user base
            'votes_cast': len(ballot.votes) if hasattr(ballot, 'votes') else 0
        }
    }
    
    return jsonify(analytics_data)

@admin_bp.route('/api/ballots/<int:ballot_id>/candidates')
@login_required
@admin_required
def get_ballot_candidates(ballot_id):
    ballot = Ballot.query.get_or_404(ballot_id)
    candidates = [{'id': c.id, 'name': c.name, 'position': c.position, 'manifesto': c.manifesto} for c in ballot.candidates]
    return jsonify(candidates)

@admin_bp.route('/api/ballots/<int:ballot_id>/duplicate', methods=['POST'])
@login_required
@admin_required
def duplicate_ballot(ballot_id):
    original_ballot = Ballot.query.get_or_404(ballot_id)
    
    try:
        from datetime import datetime, timedelta
        new_ballot = Ballot(
            title=f"{original_ballot.title} (Copy)",
            description=original_ballot.description,
            ballot_type=original_ballot.ballot_type,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=7),
            is_active=False,
            min_voters=original_ballot.min_voters,
            max_voters=original_ballot.max_voters,
            requires_verification=original_ballot.requires_verification
        )
        
        db.session.add(new_ballot)
        db.session.flush()  # To get the new ballot ID
        
        # Copy candidates
        from app.models.candidate import Candidate
        for candidate in original_ballot.candidates:
            new_candidate = Candidate(
                name=candidate.name,
                position=candidate.position,
                manifesto=candidate.manifesto,
                ballot_id=new_ballot.id
            )
            db.session.add(new_candidate)
        
        db.session.commit()
        return jsonify({'success': True, 'id': new_ballot.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/api/candidates/<int:candidate_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_candidate(candidate_id):
    from app.models.candidate import Candidate
    candidate = Candidate.query.get_or_404(candidate_id)
    
    try:
        # Delete associated votes
        Vote.query.filter_by(candidate_id=candidate_id).delete()
        db.session.delete(candidate)
        db.session.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/api/ballots/<int:ballot_id>/export')
@login_required
@admin_required
def export_ballot_results(ballot_id):
    """Export ballot results as CSV"""
    from flask import Response
    import csv
    import io
    
    ballot = Ballot.query.get_or_404(ballot_id)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Candidate Name', 'Position', 'Votes', 'Percentage'])
    
    total_votes = Vote.query.filter_by(ballot_id=ballot_id).count()
    
    # Write data
    for candidate in ballot.candidates:
        vote_count = Vote.query.filter_by(candidate_id=candidate.id).count()
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        
        writer.writerow([
            candidate.name,
            candidate.position,
            vote_count,
            f"{percentage:.2f}%"
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={ballot.title}_results.csv'}
    )

@admin_bp.route('/api/ballots/<int:ballot_id>/candidates', methods=['POST'])
@login_required
@admin_required
def add_candidate(ballot_id):
    """Add a new candidate to a ballot"""
    ballot = Ballot.query.get_or_404(ballot_id)
    data = request.get_json()
    
    try:
        from app.models.candidate import Candidate
        
        candidate = Candidate(
            name=data['name'],
            position=data['position'],
            manifesto=data.get('manifesto', ''),
            photo_url=data.get('photo_url', ''),
            ballot_id=ballot_id
        )
        
        db.session.add(candidate)
        db.session.commit()
        
        return jsonify({'success': True, 'id': candidate.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400
