import socket
import threading
import json
data =  '{ "name":"John", "age":30, "city":"New York"}'
json_data = json.loads(data)
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    print()

    connected = True
    while connected:
            data = f"{json_data}"
            conn.send(data.encode(FORMAT))
            msg = conn.recv(40000).decode(FORMAT)
            if msg != DISCONNECT_MESSAGE:
            # Assuming msg includes both address and JSON data separated in some manner
            # Example format: "{address} {json_string}"

            # Parsing the received JSON message
                data = json.loads(msg)
            else:
                print(f"[SERVER] {addr} has disconnected")
                connected = False
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
print("[STARTING] server is starting...")
start()