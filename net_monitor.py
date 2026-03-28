import os
import datetime
import time 

targets = ["google.com","github.com", "192.168.0.3"]

print("--- start ---")

try:
    while True:
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"\n[ check in {now}]") 

        for host in targets:
            response = os.system(f"ping -c 1 -W 2 {host} > /dev/null 2>&1")
            status = "OK"if response == 0 else "FAIL"
            print(f" {host:15} : {status}")

        print(" we're waiting 10 second.....")    

except KeyboardInterrupt:
    print("\n--- stop monitoring ---")        
