from flask import Blueprint, request, jsonify
from models import db, User

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    """Endpoint to create a new user account"""
    data = request.get_json()
    new_user = User(
        first_name=data['firstName'],
        last_name=data['lastName'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'status': 201,
        'message': 'User created successfully',
        'data': {
            'firstName': new_user.first_name,
            'lastName': new_user.last_name,
            'email': new_user.email
        }
    })

@auth_blueprint.route('/signin', methods=['POST'])
def signin():
    """Endpoint to login a user"""
    data = request.get_json()
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        return jsonify({
            'status': 200,
            'data': {
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email
            }
        })
    return jsonify({
        'status': 401,
        'error': 'Invalid email or password'
    })
