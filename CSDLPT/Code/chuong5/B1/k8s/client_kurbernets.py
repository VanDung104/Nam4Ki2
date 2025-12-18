import grpc
import calculator_pb2
import calculator_pb2_grpc

def run():
    # Kết nối đến gRPC Server thông qua port-forward
    server_address = '192.168.57.130:50051'  # Sử dụng localhost và cổng 50051
    with grpc.insecure_channel(server_address) as channel:
        # Tạo stub để gọi các phương thức từ Server
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        
        # Tạo yêu cầu (request) để gọi phương thức Sum
        request = calculator_pb2.SumRequest(a=5, b=10)
        
        # Gọi phương thức Sum từ Server
        response = stub.Sum(request)
        
        # In kết quả
        print("Sum result:", response.result)

if __name__ == '__main__':
    run()