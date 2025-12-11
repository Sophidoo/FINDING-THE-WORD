from flask import Blueprint, jsonify, request
from flask_login import current_user
from models.game import GameSession
from models.score import Score
from models.user import User
from sqlalchemy import func, desc
from database.db import db



def get_leaderboard():
    level = request.args.get('level', type=int)  # Optional level filter
    limit = request.args.get('limit', 20, type=int)  # Default to 20 for your page

    # Base query: Group by user, get max score, total games, avg time
    query = db.session.query(
        User.id.label('user_id'),
        User.username,
        func.sum(Score.score).label('total_score'),
        func.count(Score.id).label('total_games'),  # Or use GameSession if separate
        func.avg(Score.time_taken).label('avg_time')  # Assuming Score has 'time_taken' in seconds
    ).join(Score, Score.user_id == User.id)  # Join Score to User

    if level:
        query = query.filter(Score.level == level)

    # Group by user, order by best_score DESC, limit
    top_users = query.group_by(User.id, User.username) \
                     .order_by(desc('total_score')) \
                     .limit(limit) \
                     .all()

    # Format response
    leaderboard = []
    for row in top_users:
        leaderboard.append({
            'user_id': row.user_id,
            'username': row.username or 'Guest',
            'score': row.total_score or 0,
            'total_games': row.total_games or 0,
            'avg_time': row.avg_time or 0,  # In seconds; format in JS
            'is_current_user': current_user.is_authenticated and row.user_id == current_user.id
        })

    return jsonify({
        'leaderboard': leaderboard,
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

    total_score = db.session.query(func.sum(Score.score)) \
                        .filter(Score.user_id == user_id) \
                        .scalar() or 0
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
        'total_score': total_score,
        'best_scores': best_scores,
        'average_score': round(avg_score, 2),
        'completion_rate': f"{(completed_games / total_games) * 100:.1f}%" if total_games > 0 else "0%"
    })