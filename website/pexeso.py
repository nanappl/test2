from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from . import db

pexeso = Blueprint('pexeso', __name__)

@pexeso.route('/pexeso', methods=['GET'])
def pexeso_game():
    return render_template('pexeso.html', user=current_user)

@pexeso.route('/get_user_shortest_time', methods=['GET'])
@login_required
def get_user_shortest_time():
    return jsonify({"shortest_time": current_user.shortest if current_user.shortest != 0 else None})

@pexeso.route('/update_shortest_time', methods=['POST'])
@login_required
def update_shortest_time():
    shortest_time = request.json.get('shortest_time')

    if current_user.shortest is None or current_user.shortest == 0 or shortest_time < current_user.shortest:
        current_user.shortest = shortest_time
        db.session.commit()

    return jsonify({"message": "Shortest time updated successfully!", "shortest_time": current_user.shortest}), 200
