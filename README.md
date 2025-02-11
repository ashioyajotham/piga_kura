# Piga Kura - Secure Electronic Voting System

A robust, secure, and transparent electronic voting system built with Flask.

## Features
- Secure voter authentication and verification
- Real-time vote counting and result display
- Multiple concurrent ballot support
- Tamper-proof vote recording
- Role-based access control (Voters, Officials, Admins)
- Audit trail and vote verification

## Tech Stack
- Backend: Flask/Python
- Database: SQLAlchemy
- Frontend: Bootstrap, JavaScript
- Security: JWT, Flask-Login, Bcrypt

## Getting Started
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Set environment variables:
    - `FLASK_APP=app.py`
    - `FLASK_ENV=development`
    - `SECRET_KEY=your_secret_key`
5. Initialize database: `flask db upgrade`
6. Run application: `flask run`

## Security Features
- End-to-end encryption
- One-time voting tokens
- Vote verification receipts
- Audit logging
- DDoS protection