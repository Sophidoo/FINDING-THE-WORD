from flask import Blueprint
from controllers.auth_controller import register, login, logout, profile, update_profile, change_password


authBlueprint = Blueprint('authBlueprint', __name__)


authBlueprint.route('/register', methods=['POST'])(register)
authBlueprint.route('/login', methods=['POST'])(login)
authBlueprint.route('/logout', methods=['POST'])(logout)
authBlueprint.route('/profile', methods=['GET'])(profile)
authBlueprint.route('/profile/update', methods=['PUT'])(update_profile)
authBlueprint.route('/profile/change-password', methods=['PUT'])(change_password)
