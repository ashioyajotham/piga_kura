from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.services.auth import AuthService
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    role = request.args.get('role', 'voter')
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = AuthService.verify_user(email, password)
        
        if user:
            # Check if the user has the appropriate role
            if (role == 'admin' and not user.is_admin) or \
               (role == 'official' and not user.is_official):
                flash('You do not have permission to access this area', 'danger')
                return redirect(url_for('auth.login', role=role))
            
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Invalid email or password', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    role = request.args.get('role', 'voter')
    
    # Only allow voter and official registrations
    if role not in ['voter', 'official']:
        role = 'voter'
        
    if request.method == 'POST':
        try:
            is_official = (role == 'official')
            
            user = AuthService.register_user(
                email=request.form.get('email'),
                voter_id=request.form.get('voter_id'),
                password=request.form.get('password'),
                is_official=is_official
            )
            
            if is_official:
                flash('Registration submitted. Official accounts require approval.', 'info')
            else:
                flash('Registration successful! Please login.', 'success')
                
            return redirect(url_for('auth.login', role=role))
            
        except ValueError as e:
            flash(str(e), 'danger')
            
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))
