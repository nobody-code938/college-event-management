from flask import session
from models.user import User

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

def format_date_str(date_obj):
    if not date_obj:
        return ''
    return date_obj.strftime('%b %d, %Y')

def format_time_str(time_obj):
    if not time_obj:
        return ''
    return time_obj.strftime('%I:%M %p')
