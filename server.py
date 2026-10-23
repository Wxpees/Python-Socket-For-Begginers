import socket 
import threading 

port = 9999 
Header = 64 

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
server_ip = "127.0.0.1"  
ADDR = (server_ip, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send_msg(conn, msg):
    # send message length first padded to 64 bytes
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (Header - len(send_length))
    conn.send(send_length)
    conn.send(message)

def handel_client(conn, addr): 
    print(f"[NEW CONNECTION] {addr} connected.") 

    connected = True 
    while connected: 
        try:
            # type a command to send to client
            cmd = input(f"Command to {addr}: ")
            if not cmd.strip():
                continue

            # send command to client
            send_msg(conn, cmd)

            if cmd.lower() == 'quit' or cmd == DISCONNECT_MESSAGE:
                connected = False
                break

            # receive command output from client
            msg_length = conn.recv(Header).decode(FORMAT)
            if not msg_length:
                break

            msg_length = int(msg_length.strip())
            msg = conn.recv(msg_length).decode(FORMAT)

            print(f"\n[OUTPUT FROM {addr}]:\n{msg}")

        except socket.error:
            print(f"[ERROR] Connection lost with {addr}")
            break

    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

def start(): 
    server.listen()
    print(f"[LISTENING] Server is listening on {server_ip}:{port}")
    while True: 
        conn, addr = server.accept() 
        thread = threading.Thread(target=handel_client, args=(conn, addr)) 
        thread.start() 
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()