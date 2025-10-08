# automation/database.py
import os
try:
    from supabase import create_client, Client
except Exception:
    create_client = None
    Client = None

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None
if SUPABASE_URL and SUPABASE_KEY and create_client:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_lead(name, phone, note=None):
    if not supabase:
        return {"error": "No supabase configured"}
    data = {"name": name, "phone": phone, "note": note}
    res = supabase.table("leads").insert(data).execute()
    return res.data

def save_message_log(sender, message, reply=None):
    if not supabase:
        return {"error": "No supabase configured"}
    data = {"sender": sender, "message": message, "reply": reply}
    res = supabase.table("messages").insert(data).execute()
    return res.data
