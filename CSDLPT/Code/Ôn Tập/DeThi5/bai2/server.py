import logging
from xmlrpc.server import SimpleXMLRPCServer
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_palindrome(s):
    logging.info(f"Server nhận chuỗi: {s}")
    time.sleep(1) 
    result = s == s[::-1]
    logging.info(f"Kết quả kiểm tra palindrome: {result}")
    return result

# Tạo server
server = SimpleXMLRPCServer(('localhost', 8000), logRequests=True)
server.register_function(is_palindrome, 'is_palindrome')

logging.info("Server đang chạy tại localhost:8000...")
server.serve_forever()
