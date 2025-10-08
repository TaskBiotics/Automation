# automation/ai_engine.py
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You are BioticBot, the friendly and helpful assistant for TaskBiotics. "
    "Answer conversationally, politely, and clearly. If the user asks to book or asks for contact, "
    "prompt to collect name and phone. Keep answers short and actionable."
)

def ask_bioticbot(user_message, max_tokens=400, temperature=0.7):
    if not user_message:
        return "Hi — how can I help you today?"
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return resp.choices[0].message["content"].strip()
    except Exception as e:
        # Log real error in production; keep friendly fallback
        return "Sorry — I'm having trouble connecting to the AI right now. Please try again in a moment."
