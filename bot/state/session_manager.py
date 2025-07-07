from datetime import datetime

user_session_state = {}

async def set_user_session(user_id: int, feature: str):
    user_session_state[user_id] = {
        "active_feature": feature,
        "last_active": datetime.now()
    }

async def clear_user_session(user_id: int):
    if user_id in user_session_state:
        del user_session_state[user_id]

def get_user_session(user_id: int):
    return user_session_state.get(user_id)
