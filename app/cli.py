import click
from flask.cli import with_appcontext
from app import db
from app.models.user import User

@click.command('create-admin')
@click.option('--email', prompt=True, help='Admin email address')
@click.option('--voter-id', prompt=True, help='Admin voter ID')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Admin password')
@with_appcontext
def create_admin_command(email, voter_id, password):
    """Create a new admin user."""
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_admin = True
            click.echo(f'Existing user {email} promoted to admin')
        else:
            user = User(email=email, voter_id=voter_id, is_admin=True)
            user.set_password(password)
            db.session.add(user)
            click.echo(f'Admin user {email} created successfully')
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error creating admin user: {e}', err=True)

def init_app(app):
    app.cli.add_command(create_admin_command)
