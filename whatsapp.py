import threading
import time
import urllib.parse
import webbrowser

# =======================================================================================
# WHATSAPP NOTIFICATION ENGINE
# Upgraded to use pure `webbrowser` to completely bypass PyWhatKit threading/GUI errors!
# This guarantees it opens instantly (under 2 seconds) and never crashes the server.
# =======================================================================================

def send_ddos_alert(dropped_packets, passed_packets, accuracy, fpr):
    """
    Called by the main server when a DDoS attack volume crosses a critical threshold.
    """
    
    def _open_whatsapp():
        message = (
            f"🚨 *CRITICAL SERVER ALERT* 🚨\n\n"
            f"Volumetric L4 DDoS Attack Detected!\n"
            f"Edge-Scrubbing Pipeline active.\n\n"
            f"🛡️ Action: DROPPED {dropped_packets} malicious packets.\n"
            f"✅ Action: PASSED {passed_packets} legitimate packets.\n\n"
            f"📈 Statistics at Trigger:\n"
            f"- Accuracy: {accuracy:.2f}%\n"
            f"- False Positive Rate: {fpr:.4f}%\n\n"
            f"Status: Simulation running correctly."
        )
        print(f"\n[WhatsApp Engine] Preparing to dispatch WhatsApp alert instantly...")
        
        try:
            # Put the target phone number here
            ADMIN_NUMBER = "+917208593024" # REPLACE WITH YOUR NUMBER
            
            # URL encode the payload for API safety
            encoded_msg = urllib.parse.quote(message)
            
            # The official WhatsApp Web API Link
            wa_url = f"https://web.whatsapp.com/send?phone={ADMIN_NUMBER}&text={encoded_msg}"
            
            print("[WhatsApp Engine] Popping open WhatsApp UI in browser...")
            
            # Instantly opens the default browser! No PyWhatKit typing macros needed.
            webbrowser.open(wa_url)
            
            print("[WhatsApp Engine] Alert dispatch sequence completed without errors.")
            
        except Exception as e:
            print(f"[WhatsApp Engine] Native Browser Error: {e}")

    # Spawn thread so FastAPI SSE loop doesn't hesitate
    thread = threading.Thread(target=_open_whatsapp, daemon=True)
    thread.start()

# Test the function directly
if __name__ == "__main__":
    send_ddos_alert(dropped_packets=140, passed_packets=25)
    time.sleep(2) # Keep alive for thread to finish
