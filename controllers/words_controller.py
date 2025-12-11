from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.word import Word
from database.db import db


def get_words():
    """Get all words with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    difficulty = request.args.get('difficulty')
    category = request.args.get('category')

    query = Word.query

    # Apply filters
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if category:
        query = query.filter_by(category=category)

    words = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'words': [word.to_dict() for word in words.items],
        'total': words.total,
        'pages': words.pages,
        'current_page': page
    })


def get_word(word_id):
    """Get specific word details"""
    word = Word.query.get_or_404(word_id)
    return jsonify(word.to_dict())

def search_word():
    word_name = request.args.get('word')  # ?q=ELEPHANT
    if not word_name:
        return jsonify({'error': 'Query parameter "word" is required'}), 400

    # Search exact match, case-insensitive
    word = Word.query.filter(
        db.func.upper(Word.word) == word_name.strip().upper()
    ).first()

    if not word:
        return jsonify({'error': 'Word not found'}), 404

    return jsonify(word.to_dict())


def get_random_words():
    """Get random words for the game"""
    count = request.args.get('count', 10, type=int)
    difficulty = request.args.get('difficulty', 'easy')

    words = Word.query.filter_by(difficulty=difficulty) \
        .order_by(db.func.random()) \
        .limit(count) \
        .all()

    return jsonify([word.to_dict() for word in words])


@login_required
def add_word():
    """Add a new word to database (Admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()

    # Validate required fields
    if not data.get('word'):
        return jsonify({'error': 'Word is required'}), 400

    # Check if word already exists
    existing_word = Word.query.filter_by(word=data['word'].upper()).first()
    if existing_word:
        return jsonify({'error': 'Word already exists'}), 400

    word = Word(
        word=data['word'].strip().upper(),
        definition=data.get('definition', ''),
        example=data.get('example', ''),
        trivia=data.get('trivia', ''),
        difficulty=data.get('difficulty', 'easy'),
        length=len(data['word']),
        category=data.get('category', 'general').strip().lower()
    )

    db.session.add(word)
    db.session.commit()

    return jsonify({
        'message': 'Word added successfully',
        'word': word.to_dict()
    }), 201


@login_required
def update_word(word_id):
    """Update word details (Admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    word = Word.query.get_or_404(word_id)
    data = request.get_json()

    if 'word' in data:
        word.word = data['word'].strip().upper()
        word.length = len(data['word'])
    if 'definition' in data:
        word.definition = data['definition']
    if 'difficulty' in data:
        word.difficulty = data['difficulty']
    if 'category' in data:
        word.category = data['category'].strip().lower()
    if 'example' in data:
        word.example = data['example']
    if 'trivia' in data:
        word.trivia = data['trivia']

    db.session.commit()

    return jsonify({
        'message': 'Word updated successfully',
        'word': word.to_dict()
    })


@login_required
def delete_word(word_id):
    """Delete a word from database (Admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    word = Word.query.get_or_404(word_id)

    db.session.delete(word)
    db.session.commit()

    return jsonify({'message': 'Word deleted successfully'})


def get_categories():
    """Get all available word categories"""
    categories = db.session.query(Word.category).distinct().all()
    category_list = [cat[0] for cat in categories if cat[0]]

    return jsonify({'categories': category_list})


def get_word_stats():
    """Get word database statistics"""
    total_words = Word.query.count()
    easy_words = Word.query.filter_by(difficulty='easy').count()
    medium_words = Word.query.filter_by(difficulty='medium').count()
    hard_words = Word.query.filter_by(difficulty='hard').count()

    return jsonify({
        'total_words': total_words,
        'by_difficulty': {
            'easy': easy_words,
            'medium': medium_words,
            'hard': hard_words
        }
    })