import grpc
import currency_converter_pb2
import currency_converter_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = currency_converter_pb2_grpc.CurrencyConverterStub(channel)
    
    print("Chương trình chuyển đổi tiền tệ")
    print("Các loại tiền hỗ trợ: USD, VND, EUR, JPY")
    
    while True:
        try:
            amount = float(input("Nhập số tiền cần chuyển đổi: "))
            from_curr = input("Nhập loại tiền ban đầu (VD: USD): ").upper()
            to_curr = input("Nhập loại tiền muốn chuyển đổi (VD: VND): ").upper()
            
            if from_curr == to_curr:
                print("Không thể chuyển đổi cùng loại tiền tệ!")
                continue
                
            request = currency_converter_pb2.ConversionRequest(
                amount=amount,
                from_currency=from_curr,
                to_currency=to_curr
            )
            
            response = stub.Convert(request)
            
            print(f"\nKết quả chuyển đổi:")
            print(f"{amount} {from_curr} = {response.converted_amount:.2f} {to_curr}")
            print(f"Tỷ giá: 1 {from_curr} = {response.exchange_rate} {to_curr}\n")
            
        except ValueError:
            print("Số tiền phải là giá trị số!")
        except grpc.RpcError as e:
            print(f"Lỗi: {e.details()}")
        except KeyboardInterrupt:
            print("\nKết thúc chương trình")
            break

if __name__ == '__main__':
    run()