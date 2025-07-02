from flask import Blueprint,flash,render_template,redirect,url_for,session
from app.utils.decorators import login_required, admin_required
from app.models import User

bp = Blueprint('user', __name__)

@bp.route('/<username>/dashboard')
@login_required
def user_dashboard(username):
    if session.get('username') != username:
        flash("Access denied.")
        return redirect(url_for('auth.login'))

    flash(f"Welcome to your dashboard, {username}!")
    return render_template('user/user_dashboard.html')


@bp.route('/<username>/profile')
@login_required
def user_profile():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.")
        return redirect(url_for('auth.login'))
    
    return render_template('user/user_profile.html', user=user)

@bp.route('/<username>/profile/update')
@login_required
def update_profile():
    username = session['username']
    user = User.query.filter_by(username=username).first()    
    return render_template('user/edit_profile.html',user=user) 