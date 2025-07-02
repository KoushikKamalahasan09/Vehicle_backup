from functools import wraps
from flask import session, redirect, url_for, flash
from app.models import User  # Import your models correctly

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            flash("You need to login first")
            return redirect(url_for('auth.login'))
        user = User.query.filter_by(username=session['username']).first()
        if not user:
            session.pop('username')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            flash("You need to login first")
            return redirect(url_for('auth.login'))
        user = User.query.filter_by(username=session['username']).first()
        if not user:
            session.pop('username')
            return redirect(url_for('auth.login'))
        if user.is_admin != True:
            flash("You are not authorized to visit this page")
            return redirect(url_for('user.home'))
        return func(*args, **kwargs)
    return wrapper
