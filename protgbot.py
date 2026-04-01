import subprocess
import time
import datetime
import requests
from rich.console import Console
from rich.table import Table
from rich.live import Live
import socket
import logging

logging.basicConfig(
    filename='security_audit.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

SECURITY_PORTS = [22, 80, 443, 3389, 53, 1900]

def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

TOKEN = "your token"
CHAT_ID = "your id"
TARGETS = ["google.com", "192.168.3.1", "github.com", "store.steampowered.com"]

count = len(TARGETS)
logging.info(f"--- start monitoring ({count} targets)---")

console = Console()
last_states = {host: "Unknown" for host in TARGETS}
last_latencies = {host:0 for host in TARGETS}

def get_banner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))

        if port in [80,443]:
            sock.send(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"r\n\r\n")

        data = sock.recv(1024).decode(errors='ignore').strip()
        sock.close()

        if not data:
            return "no banner"

        for line in data.split('\n'):
            if "Server:" in line:
                banner_info = line.replace("Server:", "").strip()[:30]
                break

        return banner_info
    except:
        return "Closed/timeout" 


def send_tg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except:
        pass

def generate_table():
    table = Table(title=f"network monitoring ({datetime.datetime.now().strftime('%H:%M:%S')})")
    table.add_column("resourse", style="cyan", no_wrap=True)
    table.add_column("latency", justify="right", style="yellow")
    table.add_column("status", justify="center")
    table.add_column("last change", justify="right", style="magenta")

    for host, state in last_states.items():
        lat = last_latencies.get(host, 0)
        
        if lat == 0:
            lat_color = "white"
        elif lat < 50:
            lat_color = "bright_green"
        elif lat < 150:
            lat_color = "yellow"
        else:
            lat_color = "bold red"

        color = "green" if "UP" in state else "bold red"

        status_text = f"[{color}]{state}[/]" 
        
        table.add_row(
            host,
            f"[{lat_color}]{lat}ms[/]",
            status_text,
            datetime.datetime.now().strftime('%H:%M:%S')
        )

    return table


console.print("[bold blue] start system....[/bold blue]")

try:
    with Live(generate_table(), refresh_per_second=1) as live:
        while True:
            for host in TARGETS:
                start_ping = time.time()
                try:
                    subprocess.check_call(
                        ["ping", "-c", "1", "-W", "1", host],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                    end_ping =time.time()
                    ping_ok = True
                    latency =round((end_ping - start_ping) * 1000)
                except: 
                    ping_ok = False
                    latency = 0

                open_ports_details = []
                if ping_ok:
                    for port in SECURITY_PORTS:
                        if check_port(host, port):
                            banner = get_banner(host, port)
                            if "closed" not in banner.lower():
                                open_ports_details.append(f"{port}({banner})")

                is_actually_alive = ping_ok or len(open_ports_details) > 0

                if not is_actually_alive:
                    current_status = "down"
                else:
                    details = " | ".join(open_ports_details) if open_ports_details else "ICMP only"
                    current_status = f"UP > {details}"

                last_latencies[host] = latency

        
                if current_status != last_states[host]:
                    lat_info = f"({last_latencies[host]})"

                    if "down" in current_status:
                        log_msg= f"ALLET: {host} is down"
                        logging.error(log_msg)
                        send_tg(f"❌ {log_msg}")
                    else:
                        log_msg = f"CHANGE: {host} is {current_status}"
                        logging.info(log_msg)
                        send_tg(f"✅ {log_msg}")

        
                    last_states[host] = current_status
                    

            live.update(generate_table())
            time.sleep(5)
            
except KeyboardInterrupt:
    up_count = sum(1 for state in last_states.values() if "UP" in state)
    total = len(TARGETS)

    stop_msg = f"stop monitoring.\nStatus: {up_count}/{total} was online"
    logging.info(stop_msg)
    send_tg(stop_msg)
    console.print("\n[bold yellow]Monitoring completed [/bold yellow]")
                       
