import subprocess
import time 
import requests

TOKEN = "your token"
CHAT_ID = "your id"

TARGETS = ["google.com", "192.168.3.1", "github.com", "store.steampowered.com"]

last_states = {host: "OK" for host in TARGETS}

def send_tg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=10)
    except Exception as e:
        print(f" sending error: {e}")
        

    
   
print("--- monitoring start ---")


try:
    while True:
        for host in TARGETS:
            try:
                subprocess.check_call(
                    ["ping", "-c", "1", "-W", "1", host],
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL
                )
                current_status = "OK"
            except subprocess.CalledProcessError:
                current_status = "ERROR"

            if current_status != last_states[host]:
                if current_status == "ERROR":
                    msg = f"❌ error: {host}"
                else:
                    msg = f"✅ OK: {host}"
                
                print(f" sending tg: {msg}")
                send_tg(msg)

                last_states[host] = current_status

        print(".", end="", flush=True)
        time.sleep(10)

except KeyboardInterrupt:
    print("\n stop")


            

