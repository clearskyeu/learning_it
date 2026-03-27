import os
import platform 

system_info = platform.uname()
print(f"--- отчет по системе ----")
print(f"Система: {system_info.system}") 
print(f"Ядро: {system_info.release}")

folders = ['scripts', 'notes', 'labs', 'backup'] 

for folder in folders: 
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"папка '{folder}' создана.")
    else:
        print(f"Папка '{folder}' уже существует.")

print("--- настройка завершена ---")

report_path ="backup/report.txt"
with open(report_path, "w") as f:
     f.write("Project initialized successfully!\n")
     f.write(f"System: {system_info.system} {system_info.release}")

print(f"файл {report_path} успешно создан")
