import os
import datetime

targets = ["google.com", "github.com", "127.0.0.1"]

up_count = 0
down_count = 0

print("--- чекаем сеть шо с ней ---")

with open("backup/network_log.txt", "a") as log:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    log.write(f"\n---проверка {now} ---\n")

    for host in targets:
        
         response = os.system(f"ping -c 1 -W 2 {host} > /dev/null 2>&1") 

        
         if response == 0:
            status = "Доступен"
            print(f"[+]{host:15} : stably")
            up_count += 1

         else:
            status = "недоступен"
            print(f"[!] {host:15} : {status}! Check connection")
            down_count += 1

        
         print(f"Хост {host:15} : {status}")

        
         log.write(f"{host:15} : {status}\n")

    summary = f"\nin total: okey: {up_count}, error: {down_count}"


    print("-" * 30)
    print(summary)        
 
    log.write(f"{'-' * 20}{summary}\n")

