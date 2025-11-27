from flask import Blueprint, jsonify, request

from models.game import GameSession
from models.score import Score
from sqlalchemy import func
from database.db import db



def get_leaderboard():
    level = request.args.get('level', type=int)  # Optional level filter
    limit = request.args.get('limit', 10, type=int)

    query = Score.query

    if level:
        query = query.filter_by(level=level)

    # Get top scores
    top_scores = query.order_by(Score.score.desc()) \
        .limit(limit) \
        .all()

    return jsonify({
        'leaderboard': [score.to_dict() for score in top_scores],
        'level': level,
        'limit': limit
    })


def user_stats():
    from flask_login import current_user
    from models.user import User

    user_id = request.args.get('user_id', current_user.id if current_user.is_authenticated else None)

    if not user_id:
        return jsonify({'error': 'User ID required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Calculate user statistics
    total_games = GameSession.query.filter_by(user_id=user_id).count()
    completed_games = GameSession.query.filter_by(user_id=user_id, is_completed=True).count()

    # Best scores per level
    best_scores = {}
    for level in [1, 2, 3]:
        best_score = Score.query.filter_by(user_id=user_id, level=level) \
            .order_by(Score.score.desc()) \
            .first()
        if best_score:
            best_scores[level] = best_score.to_dict()

    # Average score
    avg_score = db.session.query(func.avg(Score.score)) \
                    .filter(Score.user_id == user_id) \
                    .scalar() or 0

    return jsonify({
        'user_id': user_id,
        'username': user.username,
        'total_games': total_games,
        'completed_games': completed_games,
        'best_scores': best_scores,
        'average_score': round(avg_score, 2),
        'completion_rate': f"{(completed_games / total_games) * 100:.1f}%" if total_games > 0 else "0%"
    })