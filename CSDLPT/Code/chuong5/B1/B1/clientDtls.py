
import grpc
import calculator_pb2
import calculator_pb2_grpc

def run():
    # Load chứng chỉ
    with open("D:/Nam4Ki2/CSDLPT/Code/chuong5/B1/B1/server.crt", "rb") as f:
        credentials = grpc.ssl_channel_credentials(f.read())

    # Kết nối an toàn qua TLS
    with grpc.secure_channel('localhost:50051', credentials) as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        
        # Danh sách số cần cộng
        numbers = [
            calculator_pb2.SumRequest(a=1, b=2),
            calculator_pb2.SumRequest(a=3, b=4),
            calculator_pb2.SumRequest(a=5, b=6)
        ]

        response = stub.AddStream(iter(numbers))
    
    print(f"Tổng các số: {response.result}")

if __name__ == '__main__':
    run()
