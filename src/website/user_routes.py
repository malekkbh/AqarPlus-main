from flask import Blueprint, request, jsonify
from website.models import User
from website.models import db
from website.dataReq import ADMIN_PASSWORD

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users/<string:password>', methods=['POST'])
def create_user(password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}), 401
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400
    
    user = User(username=username)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_json()), 201


@user_bp.route('/users/<string:username>/<string:password>', methods=['GET'])
def get_user(username,password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}), 401
    user = User.query.get_or_404(username)
    return jsonify(user.to_json())

@user_bp.route('/users/<string:username>/<string:password>', methods=['PUT'])
def update_user(username,password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}
        ), 401
    user = User.query.get_or_404(username)
    data = request.json
    new_password = data.get('password')
        
    if new_password:
        user.set_password(new_password)
    
    db.session.commit()
    
    return jsonify(user.to_json())

@user_bp.route('/users/<string:username>/<string:password>', methods=['DELETE'])
def delete_user(username,password):
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid password provided'}), 401
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# Route to return if the user is authenticated  
@user_bp.route('/auth', methods=['POST'])
def auth():
    data = request.json
    
    username = data['username']
    password = data['password']
    
    if not username or not password:
        return jsonify({'message': False}), 401
    
    user:User = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({'message': False}), 401
    
    return jsonify({'message': True}), 200

