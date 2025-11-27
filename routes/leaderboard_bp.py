from flask import Blueprint

from controllers.leaderboard_controller import get_leaderboard, user_stats

leaderboardBlueprint = Blueprint('leaderboardBlueprint', __name__)


leaderboardBlueprint.route('/leaderboard', methods=['GET'])(get_leaderboard)
leaderboardBlueprint.route('/user-stats', methods=['GET'])(user_stats)
