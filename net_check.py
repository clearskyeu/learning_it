import os
import datetime

targets = ["google.com", "github.com", "127.0.0.1"]

print("--- чекаем сеть шо с ней ---")

with open("backup/network_log.txt", "a") as log:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    log.write(f"\n---проверка {now} ---\n")

    for host in targets:
        
        response = os.system(f"ping -c 1 -W 2 {host} > /dev/null 2>&1") 

        
        if response == 0:
            status = "Доступен"
        else:
            status = "недоступен"

        
        print(f"Хост {host:15} : [{status}]")

        
        log.write(f"{host:15} : {status}\n")
