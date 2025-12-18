import grpc
import newCalc_pb2
import newCalc_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = newCalc_pb2_grpc.CalculatorStub(channel)

        a, b = 10, 5  # Số cần tính toán

        # Gọi các phương thức từ Server
        add_response = stub.Add(newCalc_pb2.BinaryRequest(a=a, b=b))
        sub_response = stub.Subtract(newCalc_pb2.BinaryRequest(a=a, b=b))
        mul_response = stub.Multiply(newCalc_pb2.BinaryRequest(a=a, b=b))
        div_response = stub.Divide(newCalc_pb2.BinaryRequest(a=a, b=b))

        print(f"➕ {a} + {b} = {add_response.result}")
        print(f"➖ {a} - {b} = {sub_response.result}")
        print(f"✖️ {a} * {b} = {mul_response.result}")
        print(f"➗ {a} / {b} = {div_response.result}")

if __name__ == '__main__':
    run()
