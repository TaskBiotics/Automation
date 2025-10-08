# Biotic Automation (BioticBot) - Connected to Website + WhatsApp

## Overview
- Web chat endpoint: POST /api/respond  { "message": "...", "sender": "optional phone" }
- Twilio WhatsApp webhook: /webhook/whatsapp
- Lead creation endpoint: POST /api/leads

## Deploy (Render)
1. Create new Web Service on https://render.com
2. Upload repo or ZIP or connect GitHub
3. Start command: `gunicorn app:app`
4. Add environment variables (OPENAI_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, SUPABASE_URL, SUPABASE_KEY)

## Connect Website (Netlify)
- Embed the provided web widget snippet (below) into your site where you want the chat button.
- The widget will POST to `https://<your-render-app>.onrender.com/api/respond`

## Twilio
- For testing use Twilio WhatsApp Sandbox and set:
  `When a message comes in` -> `https://<your-render-app>.onrender.com/webhook/whatsapp`

## Supabase tables
- Create `leads` (id, name, phone, note, created_at)
- Create `messages` (id, sender, message, reply, created_at)

## Notes
- Model: gpt-3.5-turbo (change in ai_engine.py if desired)
- Monitor OpenAI usage to control costs
