# app/__init__.py

from flask import Flask
from .models import db, User
from werkzeug.security import generate_password_hash

def setup_database(app):
    with app.app_context():
        db.create_all()
        # Create an admin user if it doesn't exist
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            passhash = generate_password_hash('admin')
            admin = User(username='admin', passhash=passhash, email='admin@example.com', is_admin=True)
            db.session.add(admin)
            db.session.commit()