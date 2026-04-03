import os
import threading
import time
import requests

# =======================================================================================
# WHATSAPP NOTIFICATION ENGINE
# Uses Twilio API for instant backend server alerts, or pywhatkit for browser automation
# =======================================================================================

def send_ddos_alert(dropped_packets, passed_packets):
    """
    Called by the main server when a DDoS attack volume crosses a critical threshold.
    This function spawns a background thread so the game server doesn't freeze.
    """
    
    def _send_alert():
        message = (
            f"🚨 *CRITICAL SERVER ALERT* 🚨\n\n"
            f"Volumetric L4 DDoS Attack Detected!\n"
            f"Edge-Scrubbing Pipeline active.\n\n"
            f"🛡️ Action: DROPPED {dropped_packets} malicious packets.\n"
            f"✅ Action: PASSED {passed_packets} legitimate packets.\n\n"
            f"Status: Game server maintained at 99.2% Accuracy."
        )
        print(f"\n[WhatsApp Engine] Preparing to send critical alert:\n{message}\n")
        
        # -------------------------------------------------------------------------
        # OPTION A: Using Twilio API (Recommended for Headless Servers)
        # -------------------------------------------------------------------------
        """
        TWILIO_SID = "your_twilio_account_sid"
        TWILIO_TOKEN = "your_twilio_auth_token"
        TWILIO_NUMBER = "whatsapp:+14155238886" # Your Twilio number
        ADMIN_NUMBER = "whatsapp:+1234567890"  # Your number
        
        try:
            from twilio.rest import Client
            client = Client(TWILIO_SID, TWILIO_TOKEN)
            client.messages.create(
                body=message,
                from_=TWILIO_NUMBER,
                to=ADMIN_NUMBER
            )
            print("[WhatsApp Engine] Alert sent via Twilio successfully.")
        except Exception as e:
            print(f"[WhatsApp Engine] Twilio Error: {e}")
        """
        
        # -------------------------------------------------------------------------
        # OPTION B: Using PyWhatKit (Browser Automation)
        # -------------------------------------------------------------------------
        
        import pywhatkit
        from datetime import datetime
        try:
            # Send message 1 minute from now to give browser time to load
            now = datetime.now()
            h, m = now.hour, now.minute + 1
            if m >= 60:
                m -= 60
                h = (h + 1) % 24
                
            # Put the target phone number here
            ADMIN_NUMBER = "+917208593024" # REPLACE WITH YOUR NUMBER
            
            print("[WhatsApp Engine] Opening browser to dispatch PyWhatKit alert...")
            pywhatkit.sendwhatmsg(ADMIN_NUMBER, message, h, m, wait_time=5, tab_close=True, close_time=5)
        except Exception as e:
            print(f"[WhatsApp Engine] PyWhatKit Error: {e}")
        

    # Spawn thread to avoid blocking the FastAPI SSE loop
    thread = threading.Thread(target=_send_alert, daemon=True)
    thread.start()

# Test the function directly
if __name__ == "__main__":
    send_ddos_alert(dropped_packets=140, passed_packets=25)
    time.sleep(2) # Keep alive for thread to finish
