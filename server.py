import socket
import threading
import json

data =  '{ "name":"John", "age":30, "city":"New York"}'
json_data = json.loads(data)
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
BLOCKEDLST = json.load(open("blocked.json"))
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
global running
def handle_client(conn, addr):
    connected = True
    blocked = False
    for blocked_address in BLOCKEDLST:
        if addr[0] == blocked_address:
            blocked = True
            break
    if connected and not blocked:
        print(f"[NEW CONNECTION] {addr}\n")
        while connected:
            try:
                sent = f"{json_data}"
                conn.send(sent.encode(FORMAT))
                received = conn.recv(500000).decode(FORMAT)
                if received != DISCONNECT_MESSAGE:
                    received = json.loads(received)
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
    global running
    print("\n[SERVER] DISCONNECTING CLIENT FROM SERVER\n")
    running = False
    server.close()  # Close the server socket

def start():
    running = True
    server.listen()
    print(f"[SERVER] SERVER RUNNING ON {SERVER}")
    while running:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[SERVER] SERVER IS STARTING")
start()