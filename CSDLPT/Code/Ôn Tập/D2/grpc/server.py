from concurrent import futures
import grpc
import currency_converter_pb2
import currency_converter_pb2_grpc

# Tỷ giá giả lập
EXCHANGE_RATES = {
    "USD": {"VND": 23000, "EUR": 0.85, "JPY": 110},
    "VND": {"USD": 1/23000, "EUR": 0.85/23000, "JPY": 110/23000},
    "EUR": {"USD": 1/0.85, "VND": 23000/0.85, "JPY": 110/0.85},
    "JPY": {"USD": 1/110, "VND": 23000/110, "EUR": 0.85/110}
}

class CurrencyConverterServicer(currency_converter_pb2_grpc.CurrencyConverterServicer):
    def Convert(self, request, context):
        from_curr = request.from_currency.upper()
        to_curr = request.to_currency.upper()
        
        if from_curr not in EXCHANGE_RATES:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Currency {from_curr} not supported")
            return currency_converter_pb2.ConversionResponse()
            
        if to_curr not in EXCHANGE_RATES[from_curr]:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Conversion from {from_curr} to {to_curr} not supported")
            return currency_converter_pb2.ConversionResponse()
        
        rate = EXCHANGE_RATES[from_curr][to_curr]
        converted_amount = request.amount * rate
        
        return currency_converter_pb2.ConversionResponse(
            converted_amount=converted_amount,
            from_currency=from_curr,
            to_currency=to_curr,
            exchange_rate=rate
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    currency_converter_pb2_grpc.add_CurrencyConverterServicer_to_server(
        CurrencyConverterServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server đang chạy trên port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()