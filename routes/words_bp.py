from flask import Blueprint
from controllers.words_controller import get_categories, get_words, get_word, get_random_words, add_word, update_word, \
    delete_word, get_word_stats, search_word

wordsBlueprint = Blueprint('wordsBlueprint', __name__)


wordsBlueprint.route('/', methods=['GET'])(get_words)
wordsBlueprint.route('/<int:word_id>', methods=['GET'])(get_word)
wordsBlueprint.route('/random', methods=['GET'])(get_random_words)
wordsBlueprint.route('/search', methods=['GET'])(search_word)
wordsBlueprint.route('/', methods=['POST'])(add_word)
wordsBlueprint.route('/<int:word_id>', methods=['PUT'])(update_word)
wordsBlueprint.route('/<int:word_id>', methods=['DELETE'])(delete_word)
wordsBlueprint.route('/categories', methods=['GET'])(get_categories)
wordsBlueprint.route('/stats', methods=['GET'])(get_word_stats)
