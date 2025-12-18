from xmlrpc.server import SimpleXMLRPCServer

def find_longest_word(text):
    words = text.split()
    if not words:
        return ""
    return max(words, key=len)

def main():
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Server đang chạy trên cổng 8000...")
    server.register_function(find_longest_word, "find_longest_word")
    server.serve_forever()

if __name__ == "__main__":
    main()
