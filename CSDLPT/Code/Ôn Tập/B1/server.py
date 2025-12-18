import socket
import threading
import sys
import time

clients = []
server_running = True

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                if client in clients:
                    clients.remove(client)

def handle_client(client_socket):
    while server_running:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Nhận được: {message.decode()}*")
            broadcast(message, client_socket)
        except:
            break
    client_socket.close()
    if client_socket in clients:
        clients.remove(client_socket)

def accept_clients(server_socket):
    while server_running:
        try:
            server_socket.settimeout(1.0)  # mỗi 1 giây kiểm tra lại để thoát
            client_socket, addr = server_socket.accept()
            print(f"Kết nối từ {addr}")
            clients.append(client_socket)
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.daemon = True
            thread.start()
        except socket.timeout:
            continue
        except OSError:
            break

def main():
    global server_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen()

    print("TCP Server đang chạy trên cổng 5000. Nhấn Ctrl+C để thoát.")

    accept_thread = threading.Thread(target=accept_clients, args=(server,))
    accept_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nĐang tắt server...")

        server_running = False
        server.close()

        # Đóng tất cả client
        for client in clients:
            try:
                client.shutdown(socket.SHUT_RDWR)
                client.close()
            except:
                pass

        accept_thread.join()
        print(" Đã đóng tất cả kết nối. Thoát.")
        sys.exit(0)

if __name__ == "__main__":
    main()
