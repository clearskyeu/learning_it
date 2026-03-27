import os
import platform 

system_info = platform.uname()
print(f"--- отчет по системе ----")
print(f"Система: {system_info.system}") 
print(f"Ядро: {system_info.release}")

folders = ['scripts', 'notes', 'labs'] 

for folder in folders: 
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"папка '{folder}' создана.")
    else:
        print(f"Папка '{folder}' уже существует.")

print("--- настройка завершена ---")
