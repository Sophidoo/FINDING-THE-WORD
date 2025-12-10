from flask import Blueprint
from controllers.achievement_controller import get_achievements

achievementBlueprint = Blueprint('achievementBlueprint', __name__)

achievementBlueprint.route('/list', methods=['GET'])(get_achievements)
