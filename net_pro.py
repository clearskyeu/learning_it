import subprocess
import datetime
import time
import os


targets = ["google.com", "github.com", "8.8.8.8"]

if not os.path.exists("logs"):
    os.makedirs("logs")

print("--- МОНИТОРИНГ 2.0  ---")

try:
    while True:
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        log_filename = f"logs/log_{today}.txt"

        now_time = datetime.datetime.now().strftime("%H:%M:%S")

        with open(log_filename, "a") as log:
            log.write(f"\n--- check {now_time} ---\n")

        
            for host in targets:
                try:
                   subprocess.check_call(
                    ["ping", "-c", "1", "-W", "1", host],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                   )
                   result = "OK"
                except subprocess.CalledProcessError:
                   result = "Eror"

                output = f"  {host:15} : [ {result} ]"
                print(output)
                log.write(output + "\n")    
        
             
    time.sleep(8)

except KeyboardInterrupt:
    
    print("\n[!] stop!")