# bot/state/session_manager.py

user_session_state = {}  # key: telegram_id, value: active_feature (e.g. 'quiz', 'ai_chat', etc.)

def set_user_feature(telegram_id: int, feature: str):
    user_session_state[telegram_id] = feature

def get_user_feature(telegram_id: int) -> str:
    return user_session_state.get(telegram_id, "none")

def clear_user_feature(telegram_id: int):
    user_session_state.pop(telegram_id, None)
