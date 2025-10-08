def get_ai_response(user_message):
    """
    Generates a basic AI response.
    Replace this with your OpenAI or custom AI logic later.
    """
    print(f"🤖 Generating AI response for: {user_message}")

    # Simple automated response logic
    if "hi" in user_message.lower():
        return "Hello 👋! I'm BioticBot, your smart assistant from TaskBiotics."
    elif "help" in user_message.lower():
        return "Sure! Tell me what you need help with today 😊."
    elif "bye" in user_message.lower():
        return "Goodbye! It was nice chatting with you 👋."
    else:
        return f"BioticBot says: You said '{user_message}'. How can I assist further?"
