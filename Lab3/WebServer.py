# python3
# Created by Yonghao Lu, z5125710

from socket import *
import sys

#read port number from terminal
serverPort = int(sys.argv[1])  #reckon using 6000

#creat TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)

#bind the port number to the socket
serverSocket.bind(('localhost',serverPort))

#server gose in the listen state
serverSocket.listen(1)
print("Lab 3 server is listening. Ready to work!")

while 1:
    connectionSocket,addr = serverSocket.accept() #passive accepts TCP client connection 

    buffer = connectionSocket.recv(1024) #receive data from client
    buffer = buffer.decode()
    buffer = str(buffer)

    headInfo = buffer.split(" ")
    # headInfo = ["GET /index.html HTTP/1.1"]
    method = headInfo[0]

    file_name = headInfo[1][1:]

    file_type = file_name.split('.')[1]

    try:
        file_object = open(file_name,"rb")
    except IOError:
        if file_type=="ico":
            continue

        print("file request failed")

        data = "HTTP/1.1 404 File Not Found\r\n".encode()
        contentType = "Content-Type: text/html\r\n\r\n".encode()

        connectionSocket.send(data)                   
        connectionSocket.send(contentType)
        connectionSocket.send("<html><h1><center>404 File Not Found</center><h1></html>".encode())

        connectionSocket.close()   
    else:
        print("file request success")

        file_data = file_object.read()
        content_length = len(file_data)
        file_object.close()

        data = "HTTP/1.1 200 OK \r\n".encode()
        connectionSocket.send(data)
                
        if file_type == "html":
            contentType = "Content-Type: text/html\r\n".encode()
        elif file_type == "png":
            contentType = "Content-Type: image/png\r\n".encode()     
        contentLength = f"Content-Length: {content_length}\r\n\r\n".encode()              
        
        connectionSocket.send(contentType) 
        connectionSocket.send(contentLength)
        connectionSocket.send(file_data)

        connectionSocket.close()







