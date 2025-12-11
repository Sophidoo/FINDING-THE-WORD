from flask import Blueprint
from controllers.main_controller import contact, index as mainIndex, game, leaderboard, login, register, profile


mainBlueprint = Blueprint('mainBlueprint', __name__)

mainBlueprint.route('/', methods=['GET'])(mainIndex)
mainBlueprint.route('/contact', methods=['GET'])(contact)
mainBlueprint.route('/game', methods=['GET'])(game)
mainBlueprint.route('/leaderboard', methods=['GET'])(leaderboard)
mainBlueprint.route('/login', methods=['GET'])(login)
mainBlueprint.route('/register', methods=['GET'])(register)
mainBlueprint.route('/profile', methods=['GET'])(profile)

