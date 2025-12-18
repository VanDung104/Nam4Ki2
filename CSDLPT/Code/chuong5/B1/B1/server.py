import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def AddStream(self, request_iterator, context):
        total = sum(req.a + req.b for req in request_iterator)
        return calculator_pb2.SumResponse(result=total)

def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        compression=grpc.Compression.Gzip  # Bật compression cho phản hồi
    )
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server đang chạy trên cổng 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
