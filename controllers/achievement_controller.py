from flask import jsonify
from flask_login import login_required, current_user
from models.achievement import Achievement, UserAchievement


@login_required
def get_achievements():
    all_achievements = Achievement.query.all()
    user_unlocks = {ua.achievement_id for ua in current_user.achievements}

    result = []
    for ach in all_achievements:
        ach_dict = ach.to_dict()
        ach_dict['unlocked'] = ach.id in user_unlocks
        result.append(ach_dict)

    return jsonify(result)