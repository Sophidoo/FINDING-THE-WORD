# utils/achievement_checker.py

from models.achievement import Achievement, UserAchievement
from models.game import GameSession
from models.score import Score
from database.db import db
from sqlalchemy import func


def check_and_unlock_achievements(user):
    newly_unlocked = []

    # 1. Get all achievements & existing user unlocks
    all_achievements = Achievement.query.all()
    existing_ids = {ua.achievement_id for ua in user.achievements}

    # 2. PRE-FETCH DATA (Optimization)
    # Get total completed games for each difficulty level
    # Level 1=Easy, 2=Medium, 3=Hard
    easy_count = GameSession.query.filter_by(user_id=user.id, is_completed=True, level=1).count()
    medium_count = GameSession.query.filter_by(user_id=user.id, is_completed=True, level=2).count()
    hard_count = GameSession.query.filter_by(user_id=user.id, is_completed=True, level=3).count()

    # Get total score
    total_score = db.session.query(func.sum(Score.score)).filter_by(user_id=user.id).scalar() or 0

    # Get total generic games
    total_games = easy_count + medium_count + hard_count

    # 3. CHECK LOGIC
    for achievement in all_achievements:
        if achievement.id in existing_ids:
            continue

        unlocked = False

        # --- EXISTING CHECKS ---
        if achievement.category == 'score':
            if total_score >= achievement.threshold:
                unlocked = True

        elif achievement.category == 'games':
            if total_games >= achievement.threshold:
                unlocked = True

        elif achievement.category == 'perfect':
            perfect_games = Score.query.filter_by(user_id=user.id).filter(
                Score.words_found == Score.total_words).count()
            if perfect_games >= achievement.threshold:
                unlocked = True

        # --- NEW DIFFICULTY CHECKS ---
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