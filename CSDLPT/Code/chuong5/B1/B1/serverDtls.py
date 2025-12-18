import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

# Load chứng chỉ TLS
with open("D:/Nam4Ki2/CSDLPT/Code/chuong5/B1/B1/server.crt", "rb") as f:
    certificate = f.read()
with open("D:/Nam4Ki2/CSDLPT/Code/chuong5/B1/B1/server.key", "rb") as f:
    private_key = f.read()

credentials = grpc.ssl_server_credentials([(private_key, certificate)])

class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def AddStream(self, request_iterator, context):
        total = sum(request.a + request.b for request in request_iterator)
        return calculator_pb2.SumResponse(result=total)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    
    # Bật TLS
    server.add_secure_port('[::]:50051', credentials)
    
    print("Server đang chạy với TLS trên cổng 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
