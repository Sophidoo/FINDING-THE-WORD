from flask import Blueprint
from controllers.game_controller import get_game_session, get_levels, start_game, validate_word, get_hint, end_game, \
    game_history

gameBlueprint = Blueprint('gameBlueprint', __name__)

gameBlueprint.route('/levels', methods=['GET'])(get_levels)
gameBlueprint.route('/start', methods=['POST'])(start_game)
gameBlueprint.route('/validate', methods=['POST'])(validate_word)
gameBlueprint.route('/hint', methods=['POST'])(get_hint)
gameBlueprint.route('/end', methods=['POST'])(end_game)
gameBlueprint.route('/session/<int:session_id>', methods=['GET'])(get_game_session)
gameBlueprint.route('/history', methods=['GET'])(game_history)
