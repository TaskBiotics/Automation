# automation/tasks.py
import os
from twilio.rest import Client
from automation.database import save_lead, save_message_log
from automation.ai_engine import ask_bioticbot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import atexit

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")  # e.g. "whatsapp:+1415xxxxxxx"

twilio_client = None
if TWILIO_SID and TWILIO_TOKEN:
    twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=False))

def send_whatsapp_message(to_phone, body):
    if not twilio_client:
        return {"error": "Twilio not configured"}
    message = twilio_client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=body,
        to=f"whatsapp:{to_phone}"
    )
    return message.sid

def create_lead_from_message(name=None, phone=None, note=None):
    saved = save_lead(name=name or "Unknown", phone=phone, note=note)
    return saved

def schedule_followup(phone, message, when_seconds=60):
    run_date = datetime.utcnow() + timedelta(seconds=int(when_seconds))
    job = scheduler.add_job(send_whatsapp_message, 'date', run_date=run_date, args=[phone, message])
    return job

def ai_reply_and_log(sender_phone, user_message):
    reply = ask_bioticbot(user_message)
    # send reply via Twilio if configured
    send_result = None
    if sender_phone:
        send_result = send_whatsapp_message(sender_phone, reply)
    # save log (safe to call even if supabase missing)
    save_message_log(sender_phone, user_message, reply)
    return {"sent": send_result, "reply": reply}
