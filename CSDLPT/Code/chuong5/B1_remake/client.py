import grpc
import calculator_pb2
import calculator_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = calculator_pb2_grpc.CalculatorStub(channel)
    
    while True:
        try:
            a = int(input("Nhập số thứ nhất: "))
            b = int(input("Nhập số thứ hai: "))
            
            response = stub.Add(calculator_pb2.AddRequest(a=a, b=b))
            print(f"Kết quả: {response.result}\n")
        except ValueError:
            print("Vui lòng nhập số nguyên hợp lệ!")
        except KeyboardInterrupt:
            print("\nKết thúc chương trình")
            break

if __name__ == '__main__':
    run()