from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import update

from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Logged in!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('Email does not exist. Please sign up for an account.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        password = request.form.get('password')
        new_password = request.form.get('newpassword')
        new_password2 = request.form.get('newpassword2')
        if check_password_hash(current_user.password, password):
            password_check(new_password, new_password2)
            stmt = update(User).where(User.id == current_user.id).values(password=generate_password_hash(new_password, method='pbkdf2:sha256'))
            db.session.execute(stmt)
            db.session.commit()
            flash('Changed Password!', category='success')
            login_user(current_user)
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect password!', category='error')

    return render_template("change_password.html", user=current_user)


@auth.route('/delete_account', methods=['DELETE'])
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    flash('Account deleted!', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/account', methods=['GET', 'POST'])
def account():
    return render_template("account.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        password_check(password1, password2)
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category="error")
        elif len(username) < 2:
            flash("Username must be greater than 1 character", category="error")
        else:
            # add new user to database
            new_user = User(email=email, username=username,
                            password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash("Account created", category="success")

        return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


def password_check(password1, password2):
    if password1 != password2:
        flash("Passwords don\'t match", category="error")
    elif len(password1) < 7:
        flash("Password must be at least 7 characters", category="error")
    else:
        return True
    return False
