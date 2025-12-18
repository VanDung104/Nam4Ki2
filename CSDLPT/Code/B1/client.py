from socket import*
HOST = "127.0.0.1"
PORT =12345
s=socket(AF_INET,SOCK_STREAM)
s.connect((HOST,PORT))#connecttoserver(blockuntilaccepted)
msg="HelloWorld-Nhóm2" #composeamessage
s.send(msg.encode()) #sendthemessage
data=s.recv(1024) #receivetheresponse
print(data.decode()) #printtheresult
s.close() #closetheconnection