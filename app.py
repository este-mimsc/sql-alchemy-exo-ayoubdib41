# Fichier : app.py
from flask import Flask, request, jsonify
from models import db, User, Post

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        users_list = [{'id': user.id, 'username': user.username} for user in users]
        return jsonify(users_list), 200

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        new_user = User(username=data['username'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'id': new_user.id, 'username': new_user.username}), 201

    @app.route('/posts', methods=['GET'])
    def get_posts():
        posts = Post.query.all()
        posts_list = []
        for post in posts:
            posts_list.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                # === CORRECTION 1 : On ajoute le username directement comme attendu par le test ===
                'username': post.user.username 
            })
        return jsonify(posts_list), 200

    @app.route('/posts', methods=['POST'])
    def create_post():
        data = request.get_json()
        user_id = data.get('user_id')
        
        # On utilise db.session.get() qui est la méthode moderne
        user = db.session.get(User, user_id)
        if not user:
            # === CORRECTION 2 : On retourne 400 comme attendu par le test ===
            return jsonify({'error': 'User not found'}), 400

        new_post = Post(title=data['title'], content=data['content'], user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'id': new_post.id, 'title': new_post.title}), 201
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)