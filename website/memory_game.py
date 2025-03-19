

from flask import Blueprint, render_template, session, jsonify, request
from flask_login import current_user
from . import db
import random

memory = Blueprint('memory', __name__)

@memory.route('/memory', methods=['GET'])
def memory_game():
    return render_template('memory_game.html', user=current_user)


@memory.route('/memory/update_score', methods=['POST'])
def update_max_score():
    data = request.get_json()
    new_score = data.get('max_score', 0)

    if current_user.max_score_memory < new_score:
        current_user.max_score_memory = new_score
        db.session.commit()

    return jsonify({"success": True, "max_score_memory": current_user.max_score_memory})
