from db_module import get_all_chat_ids, get_messages, delete_chat

def load_chat(chat_id):
    return get_messages(chat_id)

def delete_chat_history(chat_id):
    delete_chat(chat_id)

def list_chats():
    return get_all_chat_ids()
    