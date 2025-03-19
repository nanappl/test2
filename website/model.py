from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    password1 = db.Column(db.String(150))
    username = db.Column(db.String(150))
    max_score = db.Column(db.Integer, default=0)
    max_score_memory = db.Column(db.Integer, default=0)
    shortest = db.Column(db.Integer, default=0) 
