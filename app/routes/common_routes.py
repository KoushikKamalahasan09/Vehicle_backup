# app/routes/common_routes.py

from flask import Blueprint, session, redirect, url_for, flash
from app.utils.decorators import login_required

bp = Blueprint('common', __name__)

@bp.route('/')
def index():

    if 'username' in session:
        if session.get('role') == True:  # Admin
            return redirect(url_for('admin.admin_dashboard'))
        else:  # Regular user
            return redirect(url_for('user.user_dashboard', username=session['username']))
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard_redirect():
    username = session.get('username')
    is_admin = session.get('is_admin')  

    if not username:
        flash("Please log in first.")
        return redirect(url_for('auth.login'))

    if is_admin:
        return redirect(url_for('admin.admin_dashboard'))
    else:
        return redirect(url_for('user.user_dashboard',username=username))
    
@bp.route('/summary')
@login_required
def summary_redirect():
    username = session.get('username')
    is_admin = session.get('is_admin')

    if not username:
        flash("Please log in first.")
        return redirect(url_for('auth.login'))

    if is_admin:
        return redirect(url_for('admin.list_users'))
    else:
        return redirect(url_for('user.user_profile',username=username))  #Needs to add summary routes before this can be used
    
    
@bp.route('/profile')
@login_required
def profile_redirect():
    username = session.get('username')
    is_admin = session.get('is_admin')

    if not username:
        flash("Please log in first.")
        return redirect(url_for('auth.login'))

    if is_admin:
        return redirect(url_for('admin.admin_profile'))
    else:
        return redirect(url_for('user.user_profile',username=username))
