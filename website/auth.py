from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Úspešne ste sa prihlásili!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Nesprávne heslo, skúste to znova.', category='error')
        else:
            flash('Email neexistuje.', category='error')

    return render_template("login.html", user=current_user)

    

@auth.route('/singin', methods=['GET', 'POST'])
def singin():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password1 = request.form.get('password1')

        user = User.query.filter_by(email=email).first()

    
        if user:
            flash('Email already exists.', category='error')
        else:
            user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Účet bol úspešne vytvorený! Teraz sa môžete prihlásiť.', category='success')
            return redirect(url_for('views.home'))


    return render_template("singin.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('start.html', user=current_user)


@auth.route('/cleardb')
def reset_db_route():
    db.drop_all()
    db.create_all()
    flash('dbs cleared successfully')
    
    return redirect(url_for('auth.singin'))
