import random
import socket
import threading
import json
import time
import tkinter as tk
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "169.254.158.91"
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

    def disconnect():
        global connected
        print()
        print("[CLIENT] DISCONNECTING FROM SERVER")
        print()
        # Assuming 'client' is the socket object used to connect to the server
        client.send(DISCONNECT_MESSAGE.encode(FORMAT))
        connected = False

    def gui():
        r = tk.Tk()
        r.title('Counting Seconds')
        button = tk.Button(r, text='Disconnect From Server', width=25, command=lambda: [disconnect(), r.destroy()])
        button.pack()
        r.mainloop()

    def start_gui_thread():
        gui_thread = threading.Thread(target=gui)
        gui_thread.start()

    # Start the GUI thread
    start_gui_thread()
    while connected:

        try:
            time.sleep(0.5)
            # Receiving message from the client
            msg = client.recv(40000).decode(FORMAT)
            # Assuming msg includes both address and JSON data separated in some manner
            # Example format: "{address} {json_string}"

            # Parsing the received JSON message
            data = msg.replace("'", '"')
            data = json.loads(data)
            print("[CLIENT] Server Data Received")
            data['age'] = random.randint(0,15)
            data = json.dumps(data)
            data = f"{data}"
            client.send(data.encode(FORMAT))
            print("[CLIENT] Server Data Sent")
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
        except WindowsError as e:
            print("Server closed")
            return 0
        except Exception as e:
            print(f"An error occurred: {e}")
start()