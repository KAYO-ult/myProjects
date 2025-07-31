import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

# Define network range (e.g., "192.168.1.0/24")
network = ipaddress.ip_network('192.168.1.0/24')

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((str(ip), port))
            if result == 0:
                print(f"[+] Open port {port} on {ip}")
    except Exception as e:
        pass

def scan_network():
    with ThreadPoolExecutor(max_workers=100) as executor:
        for ip in network.hosts():
            for port in range(20, 1025):  # Scan common ports
                executor.submit(scan_port, ip, port)

scan_network()
