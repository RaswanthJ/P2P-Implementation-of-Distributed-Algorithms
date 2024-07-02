import socket

def start_client(server_ip):
    port = 12345                 #Server port is mentioned here

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, port))       #This function establishes connection between client and server
        print("Connected to server at", server_ip)
        
        while True:
            num1 = input("Enter the first number: ")
            num2 = input("Enter the second number: ")
            #The two numbers are inputted here and sent to server.
            message = f"{num1},{num2}"
            #Message is sent as two numbers separated by comma as a string
            client_socket.sendall(message.encode())     #This functin is responsible to send data to server.
            #While sending its important to encode data. At the same time its important to decode the data after you receive it
            data = client_socket.recv(1024)
            print("Received result:", data.decode())

if __name__ == "__main__":
    server_ip = '10.194.18.177'        #Server's ip address is to be given here
    start_client(server_ip)
