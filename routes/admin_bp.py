from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.admin_controller import admin_dashboard, get_users, get_user, toggle_admin, dashboard, delete_user, get_all_games, manage_feedback, manage_users, manage_words,  get_all_feedback, delete_feedback, mark_all_feedback_read

adminBlueprint = Blueprint('adminBlueprint', __name__)

@adminBlueprint.before_request
@login_required
def require_admin():
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash("Access Denied: Admin privileges required.", "danger")
        return redirect(url_for('mainBlueprint.index'))
    
adminBlueprint.route('/dashboard', methods=['GET'])(dashboard)
adminBlueprint.route('/words', methods=['GET'])(manage_words)
adminBlueprint.route('/users', methods=['GET'])(manage_users)
adminBlueprint.route('/feedback', methods=['GET'])(manage_feedback)

adminBlueprint.route('/api/stats', methods=['GET'])(admin_dashboard)
adminBlueprint.route('/api/users', methods=['GET'])(get_users)
adminBlueprint.route('/api/users/<int:user_id>', methods=['GET'])(get_user)
adminBlueprint.route('/api/users/<int:user_id>/toggle-admin', methods=['PUT'])(toggle_admin)
adminBlueprint.route('/api/users/<int:user_id>', methods=['DELETE'])(delete_user)
adminBlueprint.route('/api/games', methods=['GET'])(get_all_games)
adminBlueprint.route('/api/feedback-list', methods=['GET'])(get_all_feedback)
adminBlueprint.route('/api/feedback-list', methods=['GET'])(get_all_feedback)
adminBlueprint.route('/api/feedback/<int:feedback_id>', methods=['DELETE'])(delete_feedback) # New
adminBlueprint.route('/api/feedback/mark-all-read', methods=['POST'])(mark_all_feedback_read)
