import grpc
import calculator_pb2
import calculator_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        
        # Danh sách các cặp số cần cộng
        numbers = [
            calculator_pb2.SumRequest(a=1, b=2),
            calculator_pb2.SumRequest(a=3, b=4),
            calculator_pb2.SumRequest(a=5, b=6)
        ]

        response = stub.AddStream(iter(numbers),compression=grpc.Compression.Gzip)
    
    print(f"Tổng các số: {response.result}")

if __name__ == '__main__':
    run()
