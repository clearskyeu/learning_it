import subprocess
import time
import datetime
import requests
from rich.console import Console
from rich.table import Table
from rich.live import Live
import socket

SECURITY_PORTS = [22, 80, 443, 3389]

def check_port(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

TOKEN = "your token"
CHAT_ID = "your id"
TARGETS = ["google.com", "192.168.3.1", "github.com", "store.steampowered.com"]

console = Console()
last_states = {host: "Unknown" for host in TARGETS}

def send_tg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except:
        pass

def generate_table():

    table = Table(title=f"network monitoring ({datetime.datetime.now().strftime('%H:%M:%S')})")
    table.add_column("resourse", style="cyan", no_wrap=True)
    table.add_column("status", justify="center")
    table.add_column("last change", justify="right", style="magenta")

    for host, state in last_states.items():
        color = "green" if state == "OK" else "bold red"
        status_text = f"[{color}]{state}[/{color}]"
        table.add_row(host, status_text, datetime.datetime.now().strftime('%H:%M:%S'))

    return table 


console.print("[bold blue] start system....[/bold blue]")

try:
    with Live(generate_table(), refresh_per_second=1) as live:
        while True:
            for host in TARGETS:
                try:
                    subprocess.check_call(
                        ["ping", "-c", "1", "-W", "1", host],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                    ping_ok = True
                except: 
                    ping_ok = False

                open_ports = []
                if ping_ok:
                    for port in SECURITY_PORTS:
                        if check_port(host, port):
                            open_ports.append(str(port))

                ports_info = ", ".join(open_ports) if open_ports else "None"

                if not ping_ok:
                    current_status = "down"
                else:
                    ports_info = f"UP (Ports: {', '.join(open_ports) if open_ports else 'None'})"
                    current_status = ports_info

                

        
                if current_status != last_states[host]:
                    if current_status == "down":

                        send_tg(f"❌ {host} down")
                    else:
                        send_tg(f"✅ {host} UP: {current_status}")

                    last_states[host] = current_status

            live.update(generate_table())
            time.sleep(5)
            
except KeyboardInterrupt:
    console.print("\n[bold yellow]Monitoring completed [/bold yellow]")
                       
