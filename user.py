from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import User
from . import bp
from .auth import token_auth
from .errors import bad_request

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    
    data = User.query.all()
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(
        User.query, 
        page, 
        per_page, 
        'api.get_users'
    )

    return jsonify(data)

@bp.route('/users/<int:id>/article', methods=['GET'])
@token_auth.login_required
def get_user_articles(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(
        user.articles, 
        page, 
        per_page, 
        'api.get_user_articles', 
        id=id
    )

    return jsonify(data)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'name' not in data or 'mail' not in data or 'password_hash' not in data:
        return bad_request("Doit inclure les champs nom d'utilisateur, email et mot de passe")
    if User.query.filter_by(name=data['name']).first():
        return bad_request("Veuillez utiliser un nom d'utilisateur différent")
    if User.query.filter_by(mail=data['mail']).first():
        return bad_request("Veuillez utiliser une autre adresse e-mail")
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if g.current_user.id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != user.name and \
            User.query.filter_by(name=data['name']).first():
        return bad_request("Veuillez utiliser un nom d'utilisateur différent")
    if 'mail' in data and data['mail'] != user.mail and \
            User.query.filter_by(mail=data['mail']).first():
        return bad_request("Veuillez utiliser une autre adresse e-mail")
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())