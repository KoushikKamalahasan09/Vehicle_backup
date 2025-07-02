from flask import Blueprint,render_template,flash,session,redirect,url_for
from app.utils.decorators import login_required, admin_required
from app.models import User
from app import db


bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@admin_required
def admin_dashboard():
    username = session.get('username')
    user= User.query.filter_by(username=username).first()
    return render_template('admin/admin_dashboard.html',user=user)

@bp.route('/users')
@admin_required
def list_users():
    users = User.query.all()
    return render_template('admin/users_data.html', users=users,is_admin=User.is_admin)

@bp.route('/profile')
@login_required
@admin_required
def admin_profile():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.")
        return redirect(url_for('auth.login'))
    
    return render_template('admin/admin_profile.html', user=user)

@bp.route('/profile/update')
@login_required
@admin_required
def update_profile():
    username = session['username']
    user = User.query.filter_by(username=username).first()    
    return render_template('admin/edit_profile.html',user=user) 

@bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    if user_to_delete.is_admin == True:
        flash('Admin accounts cannot be deleted.', 'danger')
        return redirect(url_for('admin.list_users'))
    db.session.delete(user_to_delete)
    db.session.commit()
    flash('User has been deleted.', 'success')
    return redirect(url_for('admin.list_users'))