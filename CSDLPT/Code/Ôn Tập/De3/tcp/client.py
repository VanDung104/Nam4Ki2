import socket
import os

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5001
LOG_FILE = 'D://Nam4Ki2//CSDLPT//Code//Ôn Tập//De3//tcp//client_log.txt'

def log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(message + '\n')
    print(message)

def send_file(filepath):
    if not os.path.isfile(filepath):
        log(f"File {filepath} does not exist.")
        return

    filename = os.path.basename(filepath)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        s.sendall((filename + '\n').encode('utf-8'))

        with open(filepath, 'rb') as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                s.sendall(bytes_read)

        log(f"File {filename} sent successfully.")

if __name__ == '__main__':
    file_path = input("Enter the path of the file to send: ")
    send_file(file_path)
