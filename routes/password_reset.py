# from flask import Blueprint, request, jsonify, current_app
# from flask_mail import Mail, Message
# from itsdangerous import URLSafeTimedSerializer
# from models.user import User
# from app import db
# import os
#
# password_reset_bp = Blueprint('password_reset', __name__)
#
#
# def generate_reset_token(email):
#     """Generate password reset token"""
#     serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
#     return serializer.dumps(email, salt='password-reset-salt')
#
#
# def verify_reset_token(token, expiration=3600):
#     """Verify password reset token"""
#     serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
#     try:
#         email = serializer.loads(
#             token,
#             salt='password-reset-salt',
#             max_age=expiration
#         )
#     except:
#         return None
#     return email
#
#
# @password_reset_bp.route('/forgot-password', methods=['POST'])
# def forgot_password():
#     """Request password reset"""
#     data = request.get_json()
#     email = data.get('email')
#
#     if not email:
#         return jsonify({'error': 'Email is required'}), 400
#
#     user = User.query.filter_by(email=email).first()
#
#     # Always return success to prevent email enumeration
#     if not user:
#         return jsonify({'message': 'If the email exists, a reset link has been sent'})
#
#     # Generate reset token
#     token = generate_reset_token(user.email)
#
#     # In a real application, you would send an email here
#     # For now, we'll return the token (in development only)
#     reset_link = f"http://localhost:3000/reset-password?token={token}"
#
#     print(f"Password reset link for {user.email}: {reset_link}")
#
#     # TODO: Implement actual email sending
#     # send_password_reset_email(user.email, reset_link)
#
#     return jsonify({
#         'message': 'If the email exists, a reset link has been sent',
#         'debug_token': token  # Remove this in production
#     })
#
#
# @password_reset_bp.route('/reset-password', methods=['POST'])
# def reset_password():
#     """Reset password using token"""
#     data = request.get_json()
#     token = data.get('token')
#     new_password = data.get('new_password')
#
#     if not token or not new_password:
#         return jsonify({'error': 'Token and new password are required'}), 400
#
#     # Verify token
#     email = verify_reset_token(token)
#     if not email:
#         return jsonify({'error': 'Invalid or expired reset token'}), 400
#
#     # Find user by email
#     user = User.query.filter_by(email=email).first()
#     if not user:
#         return jsonify({'error': 'User not found'}), 404
#
#     # Validate new password
#     if len(new_password) < 6:
#         return jsonify({'error': 'Password must be at least 6 characters long'}), 400
#
#     # Update password
#     user.set_password(new_password)
#     db.session.commit()
#
#     return jsonify({'message': 'Password reset successfully'})
#
#
# @password_reset_bp.route('/verify-reset-token', methods=['POST'])
# def verify_reset_token_endpoint():
#     """Verify if a reset token is valid"""
#     data = request.get_json()
#     token = data.get('token')
#
#     if not token:
#         return jsonify({'error': 'Token is required'}), 400
#
#     email = verify_reset_token(token)
#     if not email:
#         return jsonify({'valid': False, 'error': 'Invalid or expired token'}), 400
#
#     return jsonify({'valid': True, 'email': email})