import socket
import threading

def receive_messages(client):
    """Luồng để nhận tin nhắn"""
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("Mất kết nối đến server.")
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5000))

    print("Đã kết nối đến server. Nhập tin nhắn để gửi:")

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        message = input()
        if message.lower() == "exit":
            break
        client.send(message.encode())

    client.close()

if __name__ == "__main__":
    main()
