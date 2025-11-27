from flask import request, jsonify
from flask_login import login_required, current_user
from database.db import db
from models.feedback import Feedback


def submit_feedback():
    """Submit feedback form"""
    data = request.get_json()

    # Validate required fields
    if not data.get('email') or not data.get('subject') or not data.get('message'):
        return jsonify({'error': 'Email, subject, and message are required'}), 400

    feedback = Feedback(
        user_id=current_user.id if current_user.is_authenticated else None,
        email=data['email'],
        subject=data['subject'],
        message=data['message'],
        rating=data.get('rating')
    )

    db.session.add(feedback)
    db.session.commit()

    return jsonify({
        'message': 'Feedback submitted successfully',
        'feedback_id': feedback.id
    }), 201


@login_required
def get_my_feedback():
    """Get user's own feedback submissions"""
    if current_user.is_admin:
        # Admins can see all feedback
        feedback_list = Feedback.query.order_by(Feedback.submitted_at.desc()).all()
    else:
        # Regular users see only their own feedback
        feedback_list = Feedback.query.filter_by(user_id=current_user.id) \
            .order_by(Feedback.submitted_at.desc()) \
            .all()

    return jsonify([feedback.to_dict() for feedback in feedback_list])


@login_required
def get_feedback(feedback_id):
    """Get specific feedback details"""
    feedback = Feedback.query.get_or_404(feedback_id)

    # Users can only see their own feedback unless they are admin
    if not current_user.is_admin and feedback.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403

    return jsonify(feedback.to_dict())


def get_contact_info():
    """Get organization contact information"""
    contact_info = {
        'organization': 'Aptech Education',
        'email': 'eprojects@aptech.com',
        'phone': '+1-234-567-8900',
        'address': '123 Education Street, Learning City, LC 12345',
        'support_hours': 'Monday-Friday: 9:00 AM - 6:00 PM'
    }

    return jsonify(contact_info)


@login_required
def update_feedback_status(feedback_id):
    """Update feedback status (Admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    feedback = Feedback.query.get_or_404(feedback_id)
    data = request.get_json()

    if 'status' in data:
        valid_statuses = ['new', 'read', 'responded']
        if data['status'] in valid_statuses:
            feedback.status = data['status']

    db.session.commit()

    return jsonify({
        'message': 'Feedback status updated successfully',
        'feedback': feedback.to_dict()
    })