# #!/usr/bin/env python3

# from scapy.all import sniff, IP

# def process_packet(packet):
#     if packet.haslayer(IP):
#         ip_layer = packet[IP]
#         print("="*60)
#         print(f"[+] Source IP      : {ip_layer.src}")
#         print(f"[+] Destination IP : {ip_layer.dst}")
#         print(f"[+] Protocol       : {ip_layer.proto}")
#         print(f"[+] Payload (raw)  : {bytes(packet.payload)[:50]}")
#         print("="*60)

# def main():
#     print("[*] Network Packet Sniffer using Scapy")
#     try:
#         packet_count = int(input("Enter number of packets to capture (e.g., 10): "))
#         protocol_filter = input("Enter protocol filter (default 'ip', e.g., 'tcp', 'udp', 'icmp'): ") or "ip"
#         print(f"[*] Capturing {packet_count} packets with filter '{protocol_filter}'...\n")
#         sniff(filter=protocol_filter, prn=process_packet, count=packet_count)
#     except KeyboardInterrupt:
#         print("\n[!] Capture stopped by user.")
#     except Exception as e:
#         print(f"[!] Error: {e}")

# if __name__ == "__main__":
#     main()




#user_input
#!/usr/bin/env python3

import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((str(ip), port))
            if result == 0:
                print(f"[+] Open port {port} on {ip}")
    except:
        pass  # Suppress any socket error

def scan_network(network_cidr, start_port, end_port):
    try:
        network = ipaddress.ip_network(network_cidr, strict=False)
    except ValueError:
        print("[!] Invalid CIDR network address.")
        return

    print(f"[*] Scanning network: {network}")
    print(f"[*] Port range: {start_port} to {end_port}\n")

    with ThreadPoolExecutor(max_workers=100) as executor:
        for ip in network.hosts():
            for port in range(start_port, end_port + 1):
                executor.submit(scan_port, ip, port)

if __name__ == "__main__":
    print("[*] Network Port Scanner")

    try:
        net_input = input("Enter CIDR network range (e.g., 192.168.1.0/24): ").strip()
        port_start = int(input("Enter start port (e.g., 20): ").strip())
        port_end = int(input("Enter end port (e.g., 1024): ").strip())

        if not (0 <= port_start <= 65535 and 0 <= port_end <= 65535 and port_start <= port_end):
            print("[!] Invalid port range. Ports must be between 0 and 65535.")
        else:
            scan_network(net_input, port_start, port_end)

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
    except Exception as e:
        print(f"[!] Error: {e}")