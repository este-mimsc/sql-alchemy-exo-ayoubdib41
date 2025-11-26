# Fichier : models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

    # === CORRECTION : On ajoute cette méthode ===
    # Elle définit comment un objet User doit être représenté en chaîne de caractères.
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # === On ajoute aussi une méthode ici pour être complet ===
    def __repr__(self):
        return f'<Post {self.title}>'