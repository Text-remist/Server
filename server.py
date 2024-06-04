import socket
import threading
import json
import time
from pyfiglet import Figlet
data = '{"name":"John", "age":30, "city":"New York"}'
HEADER = 64
PORT = 5050
SERVER = "192.165.145.1"
ADDR = (SERVER, PORT)
BLOCKEDLST = json.load(open("blocked.json"))
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    global data
    json_data = json.loads(data)
    connected = True
    blocked = False
    for blocked_address in BLOCKEDLST:
        if addr[0] == blocked_address:
            blocked = True
            break
    if connected and not blocked:
        print(f"[NEW CONNECTION] {addr}\n")
        while connected:
            time.sleep(0.01)
            try:
                sent = json.dumps(json_data)
                conn.send(sent.encode(FORMAT))
                received = conn.recv(HEADER).decode(FORMAT)
                if received != DISCONNECT_MESSAGE:
                    received = json.loads(received)
                    if 'age_update' in received:
                        age = received['age_update']
                        json_data["age"] = int(age)
                else:
                    print(f"[CLIENT] {addr} DISCONNECTED")
                    connected = False
            except WindowsError as e:
                print("[CLIENT] HAS INCORRECTLY DISCONNECTED")
                connected = False
        conn.close()
    else:
        print(f"[SERVER] CLIENT ({addr[0]}) IS ON BLOCKLIST\n[SERVER] DISCONNECTING BLOCKED CLIENT")
        conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
        connected = False
        conn.close()

def shutdown():
    print("\n[SERVER] DISCONNECTING CLIENT FROM SERVER\n")
    server.close()

def start():
    server.listen()
    print(f"[SERVER] SERVER RUNNING ON {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

f = Figlet(font='slant')
print(f.renderText('Game Server'))
print("[SERVER] SERVER IS STARTING")
start()
