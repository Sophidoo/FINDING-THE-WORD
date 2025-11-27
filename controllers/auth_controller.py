from flask import request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from database.db import db# Import db from app
from models.user import User  # Import User model


def register():
    data = request.get_json()

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    # Create new user
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 201


def login():
    data = request.get_json()

    # Try to find user by username
    user = User.query.filter_by(username=data['username']).first()

    # If not found by username, try by email
    if not user:
        user = User.query.filter_by(email=data['username']).first()

    # Check if user exists and password is correct
    if user and user.check_password(data['password']):
        login_user(user, remember=True)
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin
            }
        })

    return jsonify({'error': 'Invalid username/email or password'}), 401


@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})


@login_required
def profile():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'is_admin': current_user.is_admin,
        'created_at': current_user.created_at.isoformat() if current_user.created_at else None
    })


@login_required
def update_profile():
    data = request.get_json()

    # Check if username is being changed and if it's available
    if 'username' in data and data['username'] != current_user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        current_user.username = data['username']

    # Check if email is being changed and if it's available
    if 'email' in data and data['email'] != current_user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        current_user.email = data['email']

    db.session.commit()

    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'is_admin': current_user.is_admin
        }
    })


@login_required
def change_password():
    data = request.get_json()

    # Validate required fields
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current password and new password are required'}), 400

    # Verify current password
    if not current_user.check_password(data['current_password']):
        return jsonify({'error': 'Current password is incorrect'}), 400

    # Validate new password strength
    new_password = data['new_password']
    if len(new_password) < 6:
        return jsonify({'error': 'New password must be at least 6 characters long'}), 400

    # Set new password
    current_user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password changed successfully'})