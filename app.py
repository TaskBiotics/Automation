from flask import Flask, request, jsonify
import os
from automation.ai_engine import get_ai_response
from automation.whatsapp import send_whatsapp_message
from automation.database import save_message

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Root route — confirms the backend is running."""
    return jsonify({
        "status": "✅ BioticBot AI Automation running successfully!",
        "author": "TaskBiotics",
        "routes": {
            "/": "Status check",
            "/webhook/whatsapp": "Handles WhatsApp messages"
        }
    }), 200

@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """
    Webhook that receives messages from WhatsApp (via Twilio)
    and responds with an AI-generated message.
    """
    try:
        data = request.form
        user_message = data.get('Body')
        sender = data.get('From')

        if not user_message or not sender:
            return jsonify({"error": "Missing required fields"}), 400

        print(f"📩 New message from {sender}: {user_message}")

        # Get AI reply
        ai_reply = get_ai_response(user_message)

        # Send AI response via WhatsApp
        send_whatsapp_message(sender, ai_reply)

        # Log to database
        save_message(sender, user_message, ai_reply)

        print(f"✅ Replied to {sender}: {ai_reply}")
        return "Message processed", 200

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Use port from environment variable for Railway or local 5000
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
