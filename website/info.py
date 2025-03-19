from flask import render_template, Blueprint

info = Blueprint('info', __name__)

@info.route('/info')
def info_page():
    return render_template('info.html')
