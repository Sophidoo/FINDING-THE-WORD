# utils/achievement_checker.py

from models.achievement import Achievement, UserAchievement
from models.game import GameSession
from models.score import Score
from database.db import db
from sqlalchemy import func


def check_and_unlock_achievements(user, current_session=None):
    newly_unlocked = []

    # 1. Get all achievements & existing user unlocks
    all_achievements = Achievement.query.all()
    existing_ids = {ua.achievement_id for ua in user.achievements}

    # 2. PRE-FETCH DATA (Historical from DB)
    
    # Historical counts (Completed games only)
    easy_count = GameSession.query.filter_by(user_id=user.id, is_completed=True, level=1).count()
    medium_count = GameSession.query.filter_by(user_id=user.id, is_completed=True, level=2).count()
    hard_count = GameSession.query.filter_by(user_id=user.id, is_completed=True, level=3).count()
    
    total_games = easy_count + medium_count + hard_count

    # Historical Score
    historical_score = db.session.query(func.sum(Score.score)).filter_by(user_id=user.id).scalar() or 0
    
    # Historical Perfect Games
    historical_perfect = Score.query.filter_by(user_id=user.id).filter(
        Score.words_found == Score.total_words).count()

    # 3. ADD LIVE DATA (If currently playing)
    # This bridges the gap so you unlock stuff while playing!
    current_game_score = 0
    is_current_perfect = False
    
    if current_session:
        # Add the points you JUST earned
        current_game_score = current_session.score
        
        # Check if this specific game just became perfect
        found_count = len(current_session.found_words_list)
        total_count = len(current_session.words)
        if total_count > 0 and found_count == total_count:
            is_current_perfect = True

    # Combine History + Live
    total_score_live = historical_score + current_game_score
    total_perfect_live = historical_perfect + (1 if is_current_perfect else 0)

    # 4. CHECK LOGIC
    for achievement in all_achievements:
        if achievement.id in existing_ids:
            continue

        unlocked = False

        # --- SCORE CHECKS (Uses Live Data) ---
        if achievement.category == 'score':
            if total_score_live >= achievement.threshold:
                unlocked = True

        # --- GAME COUNT CHECKS (Usually keeps strictly to completed, but we use the totals calculated above) ---
        elif achievement.category == 'games':
            if total_games >= achievement.threshold:
                unlocked = True

        # --- PERFECT GAME CHECKS (Uses Live Data) ---
        elif achievement.category == 'perfect':
            if total_perfect_live >= achievement.threshold:
                unlocked = True

        # --- DIFFICULTY CHECKS (Keeps to completed games) ---
        elif achievement.category == 'completion_easy':
            if easy_count >= achievement.threshold:
                unlocked = True

        elif achievement.category == 'completion_medium':
            if medium_count >= achievement.threshold:
                unlocked = True

        elif achievement.category == 'completion_hard':
            if hard_count >= achievement.threshold:
                unlocked = True

        # --- UNLOCK EVENT ---
        if unlocked:
            ua = UserAchievement(user_id=user.id, achievement_id=achievement.id)
            db.session.add(ua)
            newly_unlocked.append(achievement.to_dict())

    if newly_unlocked:
        db.session.commit()

    return newly_unlocked