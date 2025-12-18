import socket
import threading

class Peer:
    def __init__(self, username, host, port):
        self.username = username
        self.host = host
        self.port = port
        self.peers = {}
        self.running = True
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        threading.Thread(target=self.listen_for_peers, daemon=True).start()
        
    def listen_for_peers(self):
        print(f"[{self.username}] Listening for connections on {self.host}:{self.port}...")
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                threading.Thread(target=self.handle_peer, args=(client_socket, addr), daemon=True).start()
            except Exception as e:
                print(f"Error accepting connection: {e}")
                break
        
    def handle_peer(self, client_socket, addr):
        print(f"[{self.username}] Connected to peer {addr}")
        while self.running:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"{message}")
                else:
                    break
            except Exception as e:
                print(f"Error handling peer {addr}: {e}")
                break
        client_socket.close()
        if addr in self.peers:
            del self.peers[addr]
        
    def connect_to_peer(self, peer_host, peer_port):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            peer_socket.connect((peer_host, peer_port))
            self.peers[(peer_host, peer_port)] = peer_socket
            print(f"[{self.username}] Connected to {peer_host}:{peer_port}")
            threading.Thread(target=self.listen_to_peer, args=(peer_socket, (peer_host, peer_port)), daemon=True).start()
        except Exception as e:
            print(f"Failed to connect to {peer_host}:{peer_port} - {e}")
        
    def listen_to_peer(self, peer_socket, addr):
        while self.running:
            try:
                message = peer_socket.recv(1024).decode()
                if message:
                    print(f"{message}")
                else:
                    break
            except Exception as e:
                print(f"Error receiving from peer {addr}: {e}")
                break
        peer_socket.close()
        if addr in self.peers:
            del self.peers[addr]
        
    def send_message(self, message):
        formatted_message = f"[{self.username}] {message}"
        for addr, peer_socket in list(self.peers.items()):
            try:
                peer_socket.sendall(formatted_message.encode())
            except Exception as e:
                print(f"Failed to send message to {addr} - {e}")
                peer_socket.close()
                del self.peers[addr]
        
    def leave_network(self):
        print(f"[{self.username}] Leaving network...")
        self.running = False
        self.server_socket.close()
        for addr, peer_socket in list(self.peers.items()):
            peer_socket.close()
        self.peers.clear()
        
if __name__ == "__main__":
    username = input("Enter your username: ")
    host = input("Enter host IP: ")
    port = int(input("Enter port: "))
    peer = Peer(username, host, port)
    
    while True:
        command = input("Enter command (connect/send/leave): ")
        if command == "connect":
            peer_host = input("Enter peer host: ")
            peer_port = int(input("Enter peer port: "))
            peer.connect_to_peer(peer_host, peer_port)
        elif command == "send":
            message = input("Enter message: ")
            peer.send_message(message)
        elif command == "leave":
            peer.leave_network()
            break
