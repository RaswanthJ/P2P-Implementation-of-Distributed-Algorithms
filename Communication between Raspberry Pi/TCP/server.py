import socket
import threading

#Run this code first before running client. Server should be in ready state to receive data before the client.

def handle_client(conn, addr):
    print('Connected by', addr)
    with conn:
        while True:
            data = conn.recv(1024)                  #Data is received here
            if not data:
                break
            numbers = data.decode().split(',')      #Client sends the data as two numbers. Our job as of now is to get is and add it and send it back 
            num1, num2 = int(numbers[0]), int(numbers[1])    #numbers contain list of data as string as we split the data with ,
            result = num1 + num2                             #In previous line we converted the string to int and here we are performing add operation
            print(f"Received numbers: {num1} and {num2}, sending result: {result}")
            conn.sendall(str(result).encode())          #Data is sent back again to client

def start_server():
    host = '0.0.0.0'         #Enter the ip address of the client that you want to receive data from
    port = 12345             #Enter the port you want to listen on. It can be anything greater than 2000 and a max of five digit number

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)                     #The argument 5 is the backlog parameter,
        print("Server listening on port", port)     # which specifies the maximum number of queued connections. 
                                                    #If the queue is full, additional clients attempting to connect may be
                                                    # refused or receive an error until the server can accept more connections.

        while True:
            conn, addr = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(conn, addr))     #Threading is done to handle multiple clients at the same time
            client_handler.start()

if __name__ == "__main__":
    start_server()
