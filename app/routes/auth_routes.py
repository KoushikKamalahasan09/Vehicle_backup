from flask import Blueprint,flash,render_template,session,redirect,url_for,request
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.utils.decorators import login_required, admin_required
from app.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/register')
def register():
    if 'username' in session:
        flash("You're already logged in.")
        if session.get('role') == True:
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return redirect(url_for('user.user_dashboard', username=session['username']))
    return render_template('auth/register.html')


@bp.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash("You have been logged out successfully.")
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.passhash, password):
        flash("Username or password is incorrect", "danger")
        return redirect(url_for('auth.login'))
    session['username'] = username
    session['role']=user.is_admin
    if user.is_admin:
        flash("Welcome back, Admin!")
        return redirect(url_for('admin.admin_dashboard'))
    else:
        flash(f"Welcome back, {username}!")
        return redirect(url_for('user.user_dashboard',username=username))
    

@bp.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    # all not nullable inputs are not empty
    if not username or not password or not confirm or not email:
        flash("Please fill all the mandatory fields")
        return redirect(url_for('auth.register'))

    # confirm and password should be same
    if not password == confirm:
        flash("Confirm and Password are not same")
        return redirect(url_for('auth.register'))

    # username should be unique
    user = User.query.filter_by(username=username).first()
    if user:
        flash("Please choose another username, selected username is taken")
        return redirect(url_for('auth.register'))
    email_user = User.query.filter_by(email=email).first()
    if email_user:
        flash("Please choose another email, selected email is already registered")
        return redirect(url_for('auth.register'))


    passhash = generate_password_hash(password)

    user = User(email=email, username=username, passhash=passhash,is_admin=False)
    db.session.add(user)
    db.session.commit()
    flash("Registration Successful, Please login to continue")
    return redirect(url_for('auth.login'))