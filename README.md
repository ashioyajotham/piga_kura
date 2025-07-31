# Piga Kura - Secure Electronic Voting System

A robust, secure, and transparent electronic voting system built with Flask, designed for university and institutional elections with comprehensive administrative controls and real-time analytics.

## Overview

Piga Kura ("cast a vote" in Swahili) provides a complete solution for conducting electronic elections with enhanced security features, role-based access control, and transparent verification mechanisms. The system features a modern admin dashboard with interactive data visualizations, comprehensive user management, and advanced ballot configuration options.

```mermaid
graph TD
    A[User Access] --> B{Authentication & Role Check}
    B -->|Voter| C[Voter Dashboard]
    B -->|Official| D[Election Management]
    B -->|Admin| E[System Administration]
    
    C --> F[View Active Ballots]
    F --> G[Cast Encrypted Vote]
    G --> H[Receive Vote Receipt]
    C --> I[Vote History]
    C --> J[Verify Previous Votes]
    
    D --> K[Create Ballots]
    D --> L[Manage Candidates] 
    D --> M[Monitor Elections]
    D --> N[Generate Reports]
    
    E --> O[User Management]
    E --> P[Ballot Administration]
    E --> Q[System Analytics]
    E --> R[Audit Logs]
    
    O --> S[Create/Edit/Delete Users]
    O --> T[Role Assignment]
    O --> U[User Verification]
    
    P --> V[Full Ballot Control]
    P --> W[Candidate Management]
    P --> X[Election Results]
    P --> Y[Data Visualization]
    
    Q --> Z[Interactive Charts]
    Q --> AA[Real-time Statistics]
    Q --> BB[Export Functionality]
    
    H --> CC[Public Vote Verification]
    G --> DD[Encrypted Storage]
    DD --> CC
```

## Features

### Core Voting System
- **Secure voter authentication** with institutional email verification
- **Role-based access control** with distinct, visually different interfaces for each user type
- **Real-time vote counting** and dynamic result display
- **Multiple concurrent ballot support** with different election types
- **Tamper-proof vote recording** through Fernet symmetric encryption
- **Vote verification system** with encrypted receipts and public verification page
- **Election customization** with flexible positions, candidates, and ballot configurations

### Advanced Administration
- **Comprehensive User Management**: Create, edit, delete users with role assignment and verification controls
- **Full Ballot Administration**: Complete CRUD operations for ballots, candidates, and election settings
- **Interactive Data Visualizations**: Bar charts, pie charts, doughnut charts, line graphs, and radar charts
- **Real-time Analytics Dashboard**: Live election statistics, voter turnout tracking, and competition analysis
- **Export Functionality**: Download charts as PNG and election data as CSV
- **Audit Trail**: Comprehensive logging of all system activities and election events

### User Experience
- **Responsive Design**: Modern Bootstrap-based UI that works on all devices
- **Modal-based Workflows**: Streamlined user interactions without page refreshes
- **Dynamic Content Updates**: AJAX-powered real-time data updates
- **Filterable Visualizations**: Switch between vote counts, percentages, and comparative views
- **Professional Reporting**: Automated result generation with rankings and statistics

## Tech Stack

- **Backend**: Flask/Python with SQLAlchemy ORM
- **Database**: SQLite (development) / PostgreSQL (production recommended)
- **Frontend**: Bootstrap 5, JavaScript ES6, Chart.js for visualizations
- **Security**: Flask-Login, Werkzeug password hashing, Fernet encryption
- **API Architecture**: RESTful endpoints with JSON responses
- **Development Tools**: Flask-Migrate for database versioning, CLI commands for administration

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ashioyajotham/piga_kura.git
   cd piga_kura
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate encryption keys**
   ```bash
   python generate_keys.py
   ```

5. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   VOTE_ENCRYPTION_KEY=generated_key_from_step_4
   DATABASE_URL=sqlite:///instance/voting.db
   ```

6. **Initialize the database**
   ```bash
   flask db upgrade
   ```

7. **Create an administrator account**
   ```bash
   flask create-admin
   ```

8. **Run the application**
   ```bash
   flask run
   ```

9. **Access the system**
   - Open your browser to `http://localhost:5000`
   - Login with your admin credentials
   - Start creating elections and managing users!

## Security Features

- End-to-end encryption of votes using Fernet symmetric encryption
- Role-based access control (voter, official, admin) with visually distinct UIs
- Domain-restricted registration (example: kabarak.ac.ke)
- Audit logging for all critical actions including vote casting and election management
- Vote verification receipts and public verification page
- Secure password hashing with Werkzeug
- Protection against common web vulnerabilities

## User Roles

### Voters

- **Register** with institutional email (@kabarak.ac.ke domain)
- **Browse active elections** with real-time status updates
- **Participate in elections** with secure, encrypted voting
- **Receive vote receipts** with unique verification codes
- **Verify cast votes** using the public verification system
- **View voting history** and track participation across elections

### Election Officials

- **Create new elections** with customizable ballot types (national, county, institutional, special)
- **Add and manage candidates** with position details and manifestos
- **Configure election parameters** including start/end dates, voter requirements, and verification methods
- **Monitor ongoing elections** with real-time participation tracking
- **Generate comprehensive results** with automated rankings and statistics
- **Export election data** in multiple formats (CSV, reports)

### System Administrators

- **Complete user management**: Create, edit, delete, and verify user accounts
- **Role assignment and control**: Manage voter, official, and admin permissions
- **Full ballot administration**: Comprehensive control over all elections and candidates
- **Interactive analytics dashboard**: View election data through multiple chart types
- **System monitoring**: Access audit logs and track all system activities
- **Data visualization tools**: Bar charts, pie charts, trend analysis, and comparative views
- **Export capabilities**: Download visualizations and comprehensive election reports

## Project Structure

```plaintext
piga_kura/
├── app/
│   ├── __init__.py           # Application factory with blueprint registration
│   ├── cli.py                # Custom CLI commands for admin tasks
│   ├── api/                  # RESTful API endpoints
│   │   ├── admin.py          # Admin management APIs (users, ballots, analytics)
│   │   ├── auth.py           # Authentication APIs
│   │   └── voter.py          # Voter-specific APIs
│   ├── models/               # SQLAlchemy database models
│   │   ├── audit_log.py      # System activity tracking
│   │   ├── ballot.py         # Election/ballot model with verification
│   │   ├── candidate.py      # Candidate model with vote counting
│   │   ├── user.py           # User model with role management
│   │   └── vote.py           # Encrypted vote storage model
│   ├── routes/               # Web interface route handlers
│   │   ├── admin.py          # Admin dashboard and management pages
│   │   ├── auth.py           # Login, registration, password reset
│   │   ├── main.py           # Landing page, vote verification
│   │   ├── official.py       # Election official dashboard
│   │   └── voter.py          # Voter dashboard and voting interface
│   ├── services/             # Business logic layer
│   │   ├── auth.py           # Authentication and authorization logic
│   │   └── voting.py         # Vote processing and encryption services
│   ├── static/               # Frontend assets
│   │   ├── css/
│   │   │   └── style.css     # Custom styling for role-based interfaces
│   │   ├── js/
│   │   │   ├── main.js       # Global JavaScript functionality
│   │   │   ├── admin-users.js    # User management interface
│   │   │   ├── admin-ballots.js  # Ballot management with charts
│   │   │   ├── dashboard.js      # Dashboard interactions
│   │   │   └── voting.js         # Voting interface logic
│   │   └── images/
│   │       ├── logo.png      # Application branding
│   │       ├── favicon.ico   # Browser icon
│   │       └── apple-touch-icon.png
│   └── templates/            # Jinja2 HTML templates
│       ├── base.html         # Base template with navigation
│       ├── index.html        # Role-based dashboard
│       ├── landing.html      # Public landing page
│       ├── verify_vote.html  # Public vote verification
│       ├── admin/            # Administrator interface templates
│       │   ├── dashboard.html    # Admin analytics dashboard
│       │   ├── users.html        # User management interface
│       │   └── ballots.html      # Ballot management with visualizations
│       ├── auth/             # Authentication templates
│       │   ├── login.html    # Login form
│       │   └── register.html # Registration with role selection
│       ├── official/         # Election official templates
│       │   └── dashboard.html    # Official management dashboard
│       └── voter/            # Voter interface templates
│           ├── active_ballots.html   # Available elections
│           ├── vote.html             # Voting interface
│           ├── vote_success.html     # Post-vote confirmation
│           └── my_votes.html         # Voting history
├── config/
│   └── config.py             # Application configuration settings
├── migrations/               # Database migration scripts (Flask-Migrate)
├── scripts/                  # Utility and setup scripts
│   ├── create_favicon.py     # Generate favicons
│   └── create_sample_election.py    # Sample data creation
├── instance/                 # Instance-specific files (created at runtime)
│   └── voting.db            # SQLite database file
├── .env                      # Environment variables (not in version control)
├── .gitignore               # Git ignore patterns
├── generate_keys.py         # Encryption key generation utility
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md               # Project documentation
```

## Database Schema

```mermaid
erDiagram
    User {
        int id PK
        string email
        string voter_id
        string password_hash
        bool is_admin
        bool is_official
        bool is_verified
        datetime created_at
    }
    
    Ballot {
        int id PK
        string title
        text description
        datetime start_date
        datetime end_date
        bool is_active
        datetime created_at
        string ballot_type
        string verification_key
        int min_voters
        int max_voters
        bool requires_verification
        string verification_method
    }
    
    Candidate {
        int id PK
        string name
        string position
        text manifesto
        string photo_url
        int ballot_id FK
    }
    
    Vote {
        int id PK
        int voter_id FK
        int ballot_id FK
        int candidate_id FK
        datetime timestamp
        text encrypted_vote
    }
    
    AuditLog {
        int id PK
        string action
        datetime timestamp
        int user_id FK
        int ballot_id FK
        string ip_address
        string user_agent
        text details
    }
    
    User ||--o{ Vote : "casts"
    User ||--o{ AuditLog : "generates"
    Ballot ||--o{ Candidate : "has"
    Ballot ||--o{ Vote : "contains"
    Ballot ||--o{ AuditLog : "tracks"
    Candidate ||--o{ Vote : "receives"
```

## Deployment

### Production Deployment Recommendations

For production deployment, implement the following:

1. **Application Server**
   ```bash
   # Use Gunicorn as WSGI server
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 run:app
   ```

2. **Reverse Proxy**
   - Configure Nginx as reverse proxy for static file serving and SSL termination
   - Enable gzip compression and caching

3. **Database**
   - Migrate from SQLite to PostgreSQL for better performance and concurrent access
   - Set up regular database backups
   - Configure connection pooling

4. **Security**
   - Enable HTTPS with Let's Encrypt or commercial SSL certificates
   - Configure proper firewall rules
   - Set secure session cookies and CSRF protection
   - Regular security updates and monitoring

5. **Environment Configuration**
   ```env
   FLASK_ENV=production
   DATABASE_URL=postgresql://user:password@localhost/voting_db
   SECRET_KEY=strong_production_secret_key
   VOTE_ENCRYPTION_KEY=production_encryption_key
   ```

6. **Monitoring and Logging**
   - Set up application logging with rotation
   - Configure system monitoring (CPU, memory, disk)
   - Implement backup strategies for critical data

### Docker Deployment (Optional)

```dockerfile
# Dockerfile example for containerized deployment
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
```

## API Documentation

The system provides RESTful APIs for all major operations:

### Authentication APIs
- `POST /api/auth/login` - User authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Admin APIs
- `GET /admin/api/users` - List all users
- `POST /admin/api/users` - Create new user
- `PUT /admin/api/users/{id}` - Update user details
- `DELETE /admin/api/users/{id}` - Delete user
- `GET /admin/api/ballots/{id}` - Get ballot details
- `POST /admin/api/ballots` - Create new ballot
- `GET /admin/api/ballots/{id}/results` - Get election results with analytics
- `GET /admin/api/ballots/{id}/export` - Export results as CSV

### Voter APIs
- `GET /api/voter/ballots` - Get active ballots for voter
- `POST /api/voter/vote` - Cast encrypted vote
- `GET /api/voter/history` - Get voting history

All APIs return JSON responses and require appropriate authentication and authorization.

## Screenshots

### Admin Dashboard with Analytics
![Admin Dashboard showing interactive charts and election statistics](/images/dashboard.jpeg)

### User Management Interface  
![Comprehensive user management with role controls and verification](/images/user_management.jpeg)

### Ballot Management
![Ballot administration and candidate management](/images/ballot.jpeg)

### Voter Interface
![Clean, intuitive voting interface with election details and candidate information](/images/voter_dashboard.jpeg)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Check the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

### v2.0.0 (Current)
- ✅ Complete admin dashboard with user and ballot management
- ✅ Interactive data visualizations (Chart.js integration)
- ✅ Enhanced UI with Bootstrap 5 and modern design
- ✅ RESTful API architecture
- ✅ Comprehensive role-based access control
- ✅ Real-time election analytics and reporting

### v1.0.0 (Initial Release)
- ✅ Basic voting system with encryption
- ✅ User authentication and authorization
- ✅ Vote verification system
- ✅ Audit logging

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
