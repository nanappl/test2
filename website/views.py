from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
def home():
    if not current_user.is_authenticated:
        return render_template('start.html', user=current_user)
    return render_template('home.html', user=current_user)


