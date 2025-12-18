import grpc
import newCalc_pb2
import newCalc_pb2_grpc
from concurrent import futures

class CalculatorServicer(newCalc_pb2_grpc.CalculatorServicer):
    """Triển khai các phương thức của gRPC Service"""
    
    def Add(self, request, context):
        return newCalc_pb2.BinaryResponse(result=request.a + request.b)

    def Subtract(self, request, context):
        return newCalc_pb2.BinaryResponse(result=request.a - request.b)

    def Multiply(self, request, context):
        return newCalc_pb2.BinaryResponse(result=request.a * request.b)

    def Divide(self, request, context):
        if request.b == 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Cannot divide by zero")
            return newCalc_pb2.BinaryResponse(result=0)
        return newCalc_pb2.BinaryResponse(result=request.a // request.b)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    newCalc_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server đang chạy trên cổng 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
