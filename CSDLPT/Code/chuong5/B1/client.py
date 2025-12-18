import grpc
import calculator_pb2
import calculator_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        response = stub.Add(calculator_pb2.SumRequest(a=5, b=3))
    print(f"Tổng: {response.result}")

if __name__ == '__main__':
    run()
