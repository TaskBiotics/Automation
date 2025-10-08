messages = []  # In-memory message storage

def save_message(sender, received_text, reply_text):
    """
    Saves chat history for monitoring or debugging.
    """
    record = {
        "sender": sender,
        "message": received_text,
        "reply": reply_text
    }
    messages.append(record)
    print(f"💾 Message saved: {record}")
    return record
