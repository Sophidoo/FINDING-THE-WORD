from flask import Blueprint
from controllers.feedback_controller import submit_feedback, get_my_feedback, get_feedback, get_contact_info, \
    update_feedback_status

feedbackBlueprint = Blueprint('feedbackBlueprint', __name__)



feedbackBlueprint.route('/feedback', methods=['POST'])(submit_feedback)
feedbackBlueprint.route('/feedback', methods=['GET'])(get_my_feedback)
feedbackBlueprint.route('/feedback/<int:feedback_id>', methods=['GET'])(get_feedback)
feedbackBlueprint.route('/contact', methods=['GET'])(get_contact_info)
feedbackBlueprint.route('/feedback/<int:feedback_id>/status', methods=['PUT'])(update_feedback_status)
