from flask import Blueprint
from controllers.admin_controller import admin_dashboard, get_users, get_user, toggle_admin, delete_user, get_all_games, \
    get_all_feedback

adminBlueprint = Blueprint('adminBlueprint', __name__)

adminBlueprint.route('/dashboard', methods=['GET'])(admin_dashboard)
adminBlueprint.route('/users', methods=['GET'])(get_users)
adminBlueprint.route('/users/<int:user_id>', methods=['GET'])(get_user)
adminBlueprint.route('/users/<int:user_id>/toggle-admin', methods=['PUT'])(toggle_admin)
adminBlueprint.route('/users/<int:user_id>', methods=['DELETE'])(delete_user)
adminBlueprint.route('/games', methods=['GET'])(get_all_games)
adminBlueprint.route('/feedback', methods=['GET'])(get_all_feedback)
