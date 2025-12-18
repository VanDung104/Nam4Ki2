import socket
import threading
import queue

HOST = 'localhost'
PORT = 65432

lock_holder = None
waiting_queue = queue.Queue()
clients = {}
lock = threading.Lock()

def handle_client(conn, addr):
    global lock_holder
    client_id = conn.recv(1024).decode()
    clients[client_id] = conn
    print(f"[SERVER] Client {client_id} connected from {addr}")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode()

            with lock:
                if msg == 'acquire':
                    if lock_holder is None:
                        lock_holder = client_id
                        conn.sendall(b'lock_granted')
                        print(f"[SERVER] Lock granted to {client_id}")
                    else:
                        waiting_queue.put(client_id)
                        print(f"[SERVER] {client_id} added to waiting queue")

                elif msg == 'release':
                    if client_id == lock_holder:
                        print(f"[SERVER] {client_id} released lock")
                        lock_holder = None
                        if not waiting_queue.empty():
                            next_client = waiting_queue.get()
                            lock_holder = next_client
                            clients[next_client].sendall(b'lock_granted')
                            print(f"[SERVER] Lock granted to {next_client}")
        except:
            break

    conn.close()
    print(f"[SERVER] Client {client_id} disconnected")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] Lock Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
