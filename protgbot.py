import subprocess
import time
import datetime
import requests
from rich.console import Console
from rich.table import Table
from rich.live import Live

TOKEN = "your token"
CHAT_ID = "your id"
TARGETS = ["google.com", "192.168.3.1", "github.com", "store.steampowered.com"]

console = Console()
last_states = {host: "OK" for host in TARGETS}

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
                    current_status = "OK"
                except subprocess.CalledProcessError:
                    current_status = "ERROR"

                if current_status!= last_states[host]:
                    if current_status == "ERROR":
                        send_tg(f"❌ {host} down")
                    else:
                        send_tg(f"✅ {host} UP")
                    last_states[host] = current_status

            live.update(generate_table())
            time.sleep(5)
            
except KeyboardInterrupt:
    console.print("\n[bold yellow]Monitoring completed [/bold yellow]")
                       
