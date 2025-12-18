import socket
import os

HOST = '0.0.0.0'
PORT = 5001
RECEIVE_FOLDER = 'D://Nam4Ki2//CSDLPT//Code//Ôn Tập//De3//tcp//receive'
LOG_FILE = 'D://Nam4Ki2//CSDLPT//Code//Ôn Tập//De3//tcp//server_log.txt'

os.makedirs(RECEIVE_FOLDER, exist_ok=True)
def recv_until_newline(conn):
    data = b''
    while not data.endswith(b'\n'):
        part = conn.recv(1)
        if not part:
            break
        data += part
    return data.decode('utf-8').strip()

def log(message):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')
    print(message)

def receive_file():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        log(f"Server listening on {HOST}:{PORT}...")
        
        conn, addr = s.accept()
        with conn:
            log(f"Connected by {addr}")

            filename = recv_until_newline(conn)
            log(f"Receiving file: {filename}")
            filepath = os.path.join(RECEIVE_FOLDER, filename)

            with open(filepath, 'wb') as f:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    f.write(data)

            log(f"File received and saved to {filepath}")

if __name__ == '__main__':
    receive_file()
