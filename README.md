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
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Generate encryption key: `python generate_keys.py`
6. Set environment variables in `.env` file:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   VOTE_ENCRYPTION_KEY=generated_key_from_step_5
   DATABASE_URL=sqlite:///voting.db
   ```
7. Initialize database: `flask db upgrade`
8. Create admin user: `flask create-admin`
9. Run application: `flask run`

## Security Features
- End-to-end encryption of votes using Fernet symmetric encryption
- Role-based access control (voter, official, admin)
- Audit logging for all critical actions
- Vote verification receipts and public verification page
- Secure password hashing with Werkzeug
- Email domain verification

## Project Structure
- `/app` - Main application code
  - `/models` - Database models (User, Ballot, Vote, Candidate, AuditLog)
  - `/routes` - Route handlers for web interface
  - `/api` - API endpoints
  - `/services` - Business logic
  - `/templates` - HTML templates
  - `/static` - CSS, JavaScript, and static assets
- `/config` - Configuration files
- `/migrations` - Database migration scripts