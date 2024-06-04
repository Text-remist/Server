import random
import socket
import threading
import json
import time
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = input("SERVER IP: ")
ADDR = (SERVER, PORT)
global connected
connected = False
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def start():
    try:
        client.connect(ADDR)
        connected = True
    except ConnectionRefusedError:
        print("Server Down")
        connected = False
    print("[CLIENT] CONNECTING TO SERVER")
    print()
    def disconnect():
        global connected
        print()
        print("[CLIENT] DISCONNECTING FROM SERVER\n")
        # Assuming 'client' is the socket object used to connect to the server
        client.send(DISCONNECT_MESSAGE.encode(FORMAT))
        connected = False

    while connected:

        try:
            time.sleep(0.5)
            # Receiving message from the client
            msg = client.recv(40000).decode(FORMAT)
            # Assuming msg includes both address and JSON data separated in some manner
            # Example format: "{address} {json_string}"
            if msg != DISCONNECT_MESSAGE:
                # Parsing the received JSON message
                data = msg.replace("'", '"')
                data = json.loads(data)
                print("[CLIENT] Server Data Received")
                data['age'] = random.randint(0,15)
                data = json.dumps(data)
                data = f"{data}"
                client.send(data.encode(FORMAT))
                print("[CLIENT] Server Data Sent\n")
            else:
                connected = False
                disconnect()
                print("[CLIENT] REASON: BLOCKED")
                return 0
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return 0
        except Exception as e:
            print(f"An error occurred: {e}")
        except KeyboardInterrupt:
            connected = False
            disconnect()
start()