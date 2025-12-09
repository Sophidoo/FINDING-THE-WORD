from flask import request, jsonify
from flask_login import login_required, current_user
from models.game import GameSession
from utils.game_generator import generate_game_grid
from database.db import db
from utils.achievement_checker import check_and_unlock_achievements


def get_levels():
    levels = [
        {'id': 1, 'name': 'Easy', 'grid_size': 8, 'word_count': 5},
        {'id': 2, 'name': 'Medium', 'grid_size': 10, 'word_count': 8},
        {'id': 3, 'name': 'Hard', 'grid_size': 12, 'word_count': 12}
    ]
    return jsonify(levels)


@login_required
def start_game():
    data = request.get_json()
    level_id = data.get('level_id', 1)

    # Generate game grid and words
    game_data = generate_game_grid(level_id)
    total_words = len(game_data['words'])
    time_limit_seconds = total_words * 60

    # Create game session
    game_session = GameSession(
        user_id=current_user.id,
        level=level_id,
        grid_data=game_data['grid'],
        words_to_find=game_data['words'],
        found_words_list=[],
        time_limit=time_limit_seconds

    )

    db.session.add(game_session)
    db.session.commit()

    return jsonify({
        'session_id': game_session.id,
        'grid': game_data['grid'],
        'words': game_data['words'],
        'total_words': len(game_data['words']),
        'time_limit': time_limit_seconds,
        'score': 0
    })


@login_required
def validate_word():
    data = request.get_json()
    session_id = data.get('session_id')
    word = data.get('word', '').upper()

    game_session = GameSession.query.get(session_id)

    if not game_session or game_session.user_id != current_user.id:
        return jsonify({'error': 'Invalid game session'}), 400

    # Check if word is in the word list
    words_list = game_session.words
    is_valid = word in words_list

    # Check if already found
    found_words = game_session.found_words_list or []
    already_found = word in found_words
    if is_valid and not already_found:
        found_words.append(word)
        game_session.found_words_list = found_words
        db.session.commit()

        game_session.calculate_score()
        print(game_session.score)
        print("score", game_session.calculate_score())
    return jsonify({
        'valid': is_valid,
        'already_found': already_found,
        'found_count': len(found_words),
        'total_words': len(words_list),
        'score': game_session.score,
        'time_limit': game_session.time_limit
    })


@login_required
def get_hint():
    data = request.get_json()
    session_id = data.get('session_id')

    game_session = GameSession.query.get(session_id)
    if not game_session:
        return jsonify({'error': 'Game session not found'}), 404

    # Simple hint: return first unfound word's first letter position
    all_words = game_session.words
    found_words = game_session.found_words_list or []
    unfound_words = [w for w in all_words if w not in found_words]

    if not unfound_words:
        return jsonify({'hint': 'All words found!'})
    print(unfound_words)
    print(all_words)
    print(found_words)
    hint_word = unfound_words[0]
    # Logic to find word position in grid would go here

    return jsonify({
        'hint': f"Look for a word starting with '{hint_word[0]}'",
        'word_length': len(hint_word)
    })


@login_required
def end_game():
    data = request.get_json()
    session_id = data.get('session_id')

    game_session = GameSession.query.get(session_id)
    if not game_session or game_session.user_id != current_user.id:
        return jsonify({'error': 'Invalid game session'}), 400

    if game_session.is_completed:
        return jsonify({'error': 'Game already completed'}), 400

    game_session.end_game()  # calls the method
    db.session.commit()
    new_achievements = check_and_unlock_achievements(current_user)


    return jsonify({
        'message': 'Game completed!',
        'final_score': game_session.score,
        'words_found': len(game_session.found_words_list),
        'total_words': len(game_session.words),
        'time_limit': game_session.time_limit,
        'time_taken': game_session.time_taken,
        'time_remaining': max(0, game_session.time_limit - (game_session.time_taken or 0)),
        'new_achievements': new_achievements
    })


@login_required
def get_game_session(session_id):
    game_session = GameSession.query.get(session_id)

    if not game_session or game_session.user_id != current_user.id:
        return jsonify({'error': 'Game session not found'}), 404

    return jsonify(game_session.to_dict())


@login_required
def game_history():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    games = GameSession.query.filter_by(user_id=current_user.id) \
        .order_by(GameSession.start_time.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'games': [game.to_dict() for game in games.items],
        'total': games.total,
        'pages': games.pages,
        'current_page': page
    })