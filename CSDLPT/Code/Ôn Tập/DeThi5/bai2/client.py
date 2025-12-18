import logging
import xmlrpc.client

# Cấu hình ghi log cho client
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Kết nối với server XML-RPC
server_url = 'http://localhost:8000'
server = xmlrpc.client.ServerProxy(server_url)

# Nhận chuỗi từ người dùng
input_string = input("Nhập chuỗi cần kiểm tra: ")

# Gửi chuỗi đến server để kiểm tra
logging.info(f"Client gửi chuỗi: {input_string}")
result = server.is_palindrome(input_string)

# In kết quả nhận được từ server
logging.info(f"Kết quả nhận từ server: {'Hợp lệ' if result else 'Không hợp lệ'}")
