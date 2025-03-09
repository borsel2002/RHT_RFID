"""CLI commands for RHT RFID system"""
import click
import csv
from flask.cli import with_appcontext
from .models import User, Assoc_info, School_info
from . import db

@click.group()
def rht():
    """RHT RFID management commands."""
    pass

@rht.command()
@click.option('--output', default='access_db.txt', help='Output file name')
@with_appcontext
def export_access(output):
    """Export access permissions to a file."""
    try:
        # Using SQLAlchemy models instead of raw SQL
        access_data = db.session.query(
            School_info.UID,
            Assoc_info.Assoc_main_Accs,
            Assoc_info.Assoc_office_Accs,
            Assoc_info.Assoc_djroom_Accs
        ).join(
            Assoc_info,
            School_info.UID == Assoc_info.UID
        ).all()

        with open(output, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(access_data)
            
        click.echo(f"Successfully exported access data to {output}")
        
    except Exception as e:
        click.echo(f"Error exporting access data: {e}", err=True)

@rht.command()
@with_appcontext
def init_db():
    """Initialize the database."""
    try:
        db.create_all()
        click.echo("Database tables created successfully")
    except Exception as e:
        click.echo(f"Error creating database tables: {e}", err=True)

@rht.command()
@click.option('--username', prompt=True, help='Admin username')
@click.option('--email', prompt=True, help='Admin email')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Admin password')
@with_appcontext
def create_admin(username, email, password):
    """Create an admin user."""
    try:
        user = User(
            username=username,
            email=email.lower(),
            role='admin',
            is_active=True
        )
        user.password = password
        db.session.add(user)
        db.session.commit()
        click.echo(f"Admin user {username} created successfully")
    except Exception as e:
        click.echo(f"Error creating admin user: {e}", err=True)
        db.session.rollback()
