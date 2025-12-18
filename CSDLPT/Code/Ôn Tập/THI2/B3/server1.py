from xmlrpc.server import SimpleXMLRPCServer

def is_palindrome(s):
    return s == s[::-1]

def filter_palindromes(strings):
    print(f"[SERVER 0] Nhận {len(strings)} chuỗi. Đang kiểm tra...")
    return [s for s in strings if is_palindrome(s)]

server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
server.register_function(filter_palindromes, "filter_palindromes")
print("[SERVER 0] Đang chạy tại cổng 8000...")
server.serve_forever()
