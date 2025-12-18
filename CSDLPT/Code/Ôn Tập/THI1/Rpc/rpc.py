import xmlrpc.client

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
    text = input("Nhập chuỗi văn bản: ")
    longest = proxy.find_longest_word(text)
    print("Từ dài nhất là:", longest)

if __name__ == "__main__":
    main()
