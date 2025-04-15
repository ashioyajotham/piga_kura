# Contributing to Piga Kura

Thank you for your interest in contributing to Piga Kura! This document provides guidelines and instructions for contributing to this secure electronic voting system.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Environment](#development-environment)
4. [Project Structure](#project-structure)
5. [Coding Standards](#coding-standards)
6. [Submitting Changes](#submitting-changes)
7. [Testing](#testing)
8. [Documentation](#documentation)
9. [Security Considerations](#security-considerations)
10. [Issue Reporting](#issue-reporting)

## Code of Conduct

Our project adheres to a Code of Conduct that we expect all contributors to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Fork and Clone the Repository

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/piga_kura.git
   cd piga_kura
   ```
3. Add the original repository as an upstream remote:
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/piga_kura.git
   ```

### Set Up Development Environment

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Generate encryption key:
   ```bash
   python generate_keys.py
   ```
4. Create a `.env` file with the required environment variables:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   VOTE_ENCRYPTION_KEY=generated_key_from_previous_step
   DATABASE_URL=sqlite:///voting.db
   ```
5. Initialize the database:
   ```bash
   flask db upgrade
   ```
6. Create an admin user:
   ```bash
   flask create-admin
   ```
7. Run the application:
   ```bash
   flask run
   ```

## Development Environment

The project uses:
- Flask (Python web framework)
- SQLAlchemy for database models
- Flask-Login for authentication
- Cryptography for secure vote encryption
- Bootstrap for frontend styling

### Recommended Tools

- Visual Studio Code with Python extension
- SQLite browser for database inspection
- Git for version control
- Python 3.8+ (required)

## Project Structure

The project follows a standard Flask application structure:

```
piga_kura/
├── app/                  # Main application code
│   ├── api/              # API endpoints
│   ├── models/           # Database models
│   ├── routes/           # Route handlers
│   ├── services/         # Business logic
│   ├── static/           # Static assets
│   ├── templates/        # HTML templates
│   ├── cli.py            # CLI commands
│   └── __init__.py       # App factory
├── config/               # Configuration
├── migrations/           # Database migrations
├── scripts/              # Utility scripts
├── tests/                # Test directory
├── .env                  # Environment variables (not committed)
├── generate_keys.py      # Key generation script
├── requirements.txt      # Dependencies
└── run.py                # Application entry point
```

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding style
- Use 4 spaces for indentation (not tabs)
- Maximum line length of 88 characters
- Include docstrings for all functions, classes, and modules
- Add type hints where appropriate

### JavaScript Code Style

- Use ESLint for JavaScript linting
- Use 2 spaces for indentation
- Use camelCase for variable and function names
- Add comments for complex logic

### HTML/CSS Style

- Follow consistent indentation (2 spaces)
- Use semantic HTML elements
- Keep CSS classes meaningful and consistent

### Naming Conventions

- **Python**: snake_case for variables and functions, PascalCase for classes
- **JavaScript**: camelCase for variables and functions
- **HTML/CSS**: kebab-case for class names and IDs

## Submitting Changes

### Branching Strategy

1. Create a new branch for each feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```

2. Make your changes and commit with clear, descriptive messages:
   ```bash
   git commit -m "Feature: Add [feature description]"
   git commit -m "Fix: Resolve [issue description] (#issue-number)"
   ```

### Pull Request Process

1. Update your branch with the latest changes from upstream:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Open a Pull Request (PR) on GitHub with:
   - Clear title and description
   - Reference to any related issues
   - Screenshots for UI changes
   - List of changes made

4. Respond to any feedback during code review

## Testing

### Running Tests

We use pytest for testing:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_module.py

# Run tests with coverage
pytest --cov=app tests/
```

### Writing Tests

- Write tests for new features and bug fixes
- Aim for high code coverage (minimum 80%)
- Test both success and failure paths
- Mock external services when needed

## Documentation

- Keep documentation up-to-date with code changes
- Document all API endpoints and parameters
- Update README.md with new features or changes
- Add comments for complex or non-obvious code

## Security Considerations

Since Piga Kura is a voting system, security is critical:

- Always encrypt sensitive data
- Never commit credentials or secrets
- Follow the principle of least privilege
- Input validation for all user inputs
- Protect against common web vulnerabilities (CSRF, XSS, SQL injection)
- Report security issues privately, not through public issues

## Issue Reporting

When reporting issues, include:

1. Clear and descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Screenshots (if applicable)
6. Environment details:
   - Browser and version
   - Operating system
   - Python version
   - Any relevant logs

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

---

Thank you for contributing to Piga Kura! Your efforts help make electronic voting more secure and transparent.
