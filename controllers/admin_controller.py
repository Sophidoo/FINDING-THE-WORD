from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from models.user import User
from models.word import Word
from models.game import GameSession
from models.score import Score
from database.db import db
from models.achievement import UserAchievement
from models.feedback import Feedback


def admin_required(f):
    """Decorator to require admin access"""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)

    return decorated_function


@login_required
@admin_required
@login_required
@admin_required
def admin_dashboard():
    """Get admin dashboard statistics"""
    # User statistics
    total_users = User.query.count()
    total_admins = User.query.filter_by(is_admin=True).count()

    # Game statistics
    total_games = GameSession.query.count()
    completed_games = GameSession.query.filter_by(is_completed=True).count()

    # Word statistics
    total_words = Word.query.count()
    # --- NEW: Get counts by difficulty ---
    easy_count = Word.query.filter_by(difficulty='easy').count()
    medium_count = Word.query.filter_by(difficulty='medium').count()
    hard_count = Word.query.filter_by(difficulty='hard').count()

    # Score statistics
    total_scores = Score.query.count()
    avg_score = db.session.query(db.func.avg(Score.score)).scalar() or 0

    total_feedback = Feedback.query.count()
    unread_feedback = Feedback.query.filter((Feedback.status == 'new') | (Feedback.status == 'unread')).count()
    read_feedback = Feedback.query.filter_by(status='read').count()

    return jsonify({
        'users': {
            'total': total_users,
            'admins': total_admins,
            'regular_users': total_users - total_admins
        },
        'games': {
            'total': total_games,
            'completed': completed_games,
            'completion_rate': f"{(completed_games / total_games) * 100:.1f}%" if total_games > 0 else "0%"
        },
        'words': {
            'total': total_words,
            'easy': easy_count,     # Added
            'medium': medium_count, # Added
            'hard': hard_count      # Added
        },
        'scores': {
            'total': total_scores,
            'average_score': round(avg_score, 2)
        },
        'feedback': {
            'total': total_feedback,
            'unread': unread_feedback,
            'read': read_feedback
        }
    })

def dashboard():
    # In the future, we will fetch words here: words = Word.query.all()
    return render_template('admin/dashboard.html')

def manage_words():
    # In the future, we will fetch words here: words = Word.query.all()
    return render_template('admin/words.html')

def manage_users():
    # In the future, we will fetch users here: users = User.query.all()
    return render_template('admin/users.html')

def manage_feedback():
    # In the future: feedback = Feedback.query.all()
    return render_template('admin/feedback.html')

@login_required
@admin_required
def get_users():
    """Get all users with pagination, filtering, and search"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    role = request.args.get('role')
    search = request.args.get('search')

    query = User.query

    # 1. Filter by Role
    if role == 'admin':
        query = query.filter_by(is_admin=True)
    elif role == 'user':
        query = query.filter_by(is_admin=False)

    # 2. Filter by Search (Username or Email)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (User.username.ilike(search_term)) | 
            (User.email.ilike(search_term))
        )

    # 3. Sort by Newest First
    query = query.order_by(User.created_at.desc())

    users = query.paginate(page=page, per_page=per_page, error_out=False)

    user_list = []
    for user in users.items:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'games_played': len(user.games),
            'total_score': sum(score.score for score in user.scores) if user.scores else 0
        }
        user_list.append(user_data)

    return jsonify({
        'users': user_list,
        'total': users.total,
        'pages': users.pages,
        'current_page': page
    })

@login_required
@admin_required
def get_user(user_id):
    """Get specific user details"""
    user = User.query.get_or_404(user_id)

    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'created_at': user.created_at.isoformat(),
        'games_played': len(user.games),
        'completed_games': len([game for game in user.games if game.is_completed]),
        'total_score': sum(score.score for score in user.scores) if user.scores else 0,
        'average_score': db.session.query(db.func.avg(Score.score)).filter(Score.user_id == user_id).scalar() or 0
    }

    return jsonify(user_data)


@login_required
@admin_required
def toggle_admin(user_id):
    """Toggle admin status for a user"""
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot modify your own admin status'}), 400

    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin

    db.session.commit()

    action = "granted" if user.is_admin else "revoked"
    return jsonify({'message': f'Admin privileges {action} for user {user.username}'})


@login_required
@admin_required
def delete_user(user_id):
    """Delete a user account"""
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot delete your own account'}), 400

    user = User.query.get_or_404(user_id)

    # Delete user's scores and games first (due to foreign key constraints)
    Score.query.filter_by(user_id=user_id).delete()
    GameSession.query.filter_by(user_id=user_id).delete()
    UserAchievement.query.filter_by(user_id=user_id).delete()

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User {user.username} deleted successfully'})


@login_required
@admin_required
def get_all_games():
    """Get all game sessions with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    games = GameSession.query.order_by(GameSession.start_time.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'games': [game.to_dict() for game in games.items],
        'total': games.total,
        'pages': games.pages,
        'current_page': page
    })


@login_required
@admin_required
def get_all_feedback():
    """Get all feedback with pagination, filtering, and search"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    search = request.args.get('search')

    query = Feedback.query

    # 1. Filter by Status
    # Note: Your model default is 'new', but UI uses 'unread'. We handle both.
    if status:
        if status == 'unread':
            query = query.filter((Feedback.status == 'new') | (Feedback.status == 'unread'))
        else:
            query = query.filter_by(status=status)

    # 2. Filter by Search (Name, Email, Subject, Message)
    if search:
        search_term = f"%{search}%"
        # We join User to search by username if needed, or just search feedback fields
        query = query.filter(
            (Feedback.email.ilike(search_term)) |
            (Feedback.subject.ilike(search_term)) |
            (Feedback.message.ilike(search_term))
        )

    # 3. Sort by Newest First
    query = query.order_by(Feedback.submitted_at.desc())

    feedback_list = query.paginate(page=page, per_page=per_page, error_out=False)

    feedback_data = []
    for fb in feedback_list.items:
        # Fetch user details if they exist
        user = User.query.get(fb.user_id) if fb.user_id else None
        feedback_data.append({
            'id': fb.id,
            'name': user.username if user else 'Guest',
            'email': fb.email,
            'subject': fb.subject,
            'message': fb.message,
            'status': fb.status,
            'submitted_at': fb.submitted_at.strftime('%Y-%m-%d'),
            'rating': fb.rating
        })

    return jsonify({
        'feedback': feedback_data,
        'total': feedback_list.total,
        'pages': feedback_list.pages,
        'current_page': page
    })

@login_required
@admin_required
def delete_feedback(feedback_id):
    """Delete a feedback entry"""
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback deleted successfully'})

@login_required
@admin_required
def mark_all_feedback_read():
    """Mark all unread/new feedback as read"""
    # Update both 'new' and 'unread' statuses to 'read'
    Feedback.query.filter(
        (Feedback.status == 'new') | (Feedback.status == 'unread')
    ).update({'status': 'read'})
    
    db.session.commit()
    return jsonify({'message': 'All feedback marked as read'})