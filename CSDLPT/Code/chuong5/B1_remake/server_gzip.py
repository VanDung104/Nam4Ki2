from concurrent import futures
import grpc
import calculator_pb2
import calculator_pb2_grpc

class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        result = request.a + request.b
        return calculator_pb2.AddResponse(result=result)

def serve():
    # Tạo server với compression gzip
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        compression=grpc.Compression.Gzip
    )
    
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        CalculatorServicer(), server
    )
    
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server đang chạy trên port 50051 với gzip compression...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
