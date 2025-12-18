import grpc
from concurrent import futures  # Đúng cách để tạo ThreadPoolExecutor
import calculator_pb2
import calculator_pb2_grpc

# Token hợp lệ để xác thực
VALID_TOKEN = "Naruto104"

class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def AddStream(self, request_iterator, context):
        # Lấy token từ metadata
        token = None
        for key, value in context.invocation_metadata():
            if key == 'authorization':
                token = value

        # Kiểm tra token
        if token != f'Bearer {VALID_TOKEN}':
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token không hợp lệ!")

        total = sum(req.a + req.b for req in request_iterator)
        return calculator_pb2.SumResponse(result=total)

def serve():
    #  Đúng cách để tạo ThreadPoolExecutor
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server đang chạy trên cổng 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
