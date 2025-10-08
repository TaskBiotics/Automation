# automation/whatsapp.py
from twilio.twiml.messaging_response import MessagingResponse
from automation.tasks import ai_reply_and_log, create_lead_from_message

def handle_incoming_whatsapp(form):
    """
    form: dict from Twilio webhook (keys: From, Body, ProfileName)
    Returns TwiML string response.
    """
    sender = form.get("From")  # e.g. 'whatsapp:+2767xxxxxxx'
    body = form.get("Body", "")
    phone = sender.replace("whatsapp:", "") if sender else None

    # Simple heuristics: capture leads on keywords
    if any(k in body.lower() for k in ["call me", "contact me", "call back", "book", "i want to hire", "quote"]):
        create_lead_from_message(name=None, phone=phone, note="auto-captured from whatsapp")

    result = ai_reply_and_log(phone, body)

    # Immediate TwiML response so Twilio returns a message instantly
    resp = MessagingResponse()
    resp.message(result["reply"])
    return str(resp)
