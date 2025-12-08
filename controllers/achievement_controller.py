# controllers/achievement_controller.py
from flask_login import current_user
from models.user_achievement import user_achievement
from database.db import db

# Define all achievements (you can move to DB later)
ACHIEVEMENTS = [
    {'name': 'First Steps',        'description': 'Play your first game',           'icon': 'First place medal', 'type': 'total_games',       'value': 1},
    {'name': 'Getting Started',    'description': 'Complete 5 games',               'icon': 'Trophy', 'type': 'completed_games',   'value': 5},
    {'name': 'Word Hunter',        'description': 'Complete 20 games',              'icon': 'Cross mark', 'type': 'completed_games',   'value': 20},
    {'name': 'Score Rookie',       'description': 'Reach 1000 points',              'icon': 'Star', 'type': 'best_score',         'value': 1000},
    {'name': 'Score Master',       'description': 'Reach 2000 points',              'icon': 'Gem stone', 'type': 'best_score',         'value': 2000},
    {'name': 'Speed Demon',        'description': 'Finish a game under 2 minutes',  'icon': 'Rocket', 'type': 'fast_game',          'value': 120},
    {'name': 'Perfectionist',      'description': 'Find all words in a game',       'icon': 'Hundred points', 'type': 'perfect_game',       'value': 1},
    {'name': 'Easy Champion',      'description': 'Best Easy score 800+',           'icon': 'Green circle', 'type': 'best_easy',          'value': 800},
    {'name': 'Hard Mode Hero',     'description': 'Best Hard score 1800+',          'icon': 'Red circle', 'type': 'best_hard',          'value': 1800},
]

def check_and_unlock_achievements(stats, game_result=None):
    """
    Called after every game end
    stats: from /api/leaderboard/user-stats
    game_result: the result from end_game() → has time_taken, words_found, etc.
    """
    newly_unlocked = []

    for ach in ACHIEVEMENTS:
        ach_type = ach['type']
        value = ach['value']

        # Skip if already unlocked
        existing = db.session.query(user_achievement).filter_by(
            user_id=current_user.id,
            achievement_id=ach['id'] if 'id' in ach else None  # we'll assign IDs
        ).first()
        if existing:
            continue

        unlocked = False

        if ach_type == 'total_games' and (stats.get('total_games', 0) >= value):
            unlocked = True
        elif ach_type == 'completed_games' and (stats.get('completed_games', 0) >= value):
            unlocked = True
        elif ach_type == 'best_score':
            best = max([s.get('score', 0) for s in stats.get('best_scores', {}).values()] or [0])
            if best >= value:
                unlocked = True
        elif ach_type == 'best_easy' and stats.get('best_scores', {}).get(1, {}).get('score', 0) >= value:
            unlocked = True
        elif ach_type == 'best_hard' and stats.get('best_scores', {}).get(3, {}).get('score', 0) >= value:
            unlocked = True
        elif ach_type == 'perfect_game' and game_result and game_result.get('words_found') == game_result.get('total_words'):
            unlocked = True
        elif ach_type == 'fast_game' and game_result and game_result.get('time_taken', 999) <= value:
            unlocked = True

        if unlocked:
            # Save to DB
            db.session.execute(
                user_achievement.insert().values(
                    user_id=current_user.id,
                    achievement_id=ach['id']  # we'll set this
                )
            )
            newly_unlocked.append({
                'name': ach['name'],
                'description': ach['description'],
                'icon': ach['icon']
            })

    if newly_unlocked:
        db.session.commit()

    return newly_unlocked