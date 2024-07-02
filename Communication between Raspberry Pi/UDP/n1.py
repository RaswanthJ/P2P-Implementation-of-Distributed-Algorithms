import socket

#This program just inputs a number from user and sends it to the other node. Other node does the same.
#Any nodes code can be run first as both nodes have exact same code except for the ips

local_ip = "127.0.0.1"    #Give the local(The ip of raspberrypi where the code is being run) ip
local_port = 12345        #local port number
remote_port = 12345       #Give the port number that the other raspberrypi listens and sends data on

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((local_ip, local_port))  #This binds the local ip and port for UDP Communication
sock.settimeout(0.01)  # Set a timeout to avoid blocking indefinitely
                       # Time out is set to make the program listen for input and break after the time limit

def udp_communicate():
    while True:
        # Sending part
        message = input("Enter message to send: ")
        sock.sendto(message.encode(), (local_ip, remote_port))
        print(f'Sent message to {local_ip}:{remote_port}')

        # Receiving part
        try:
            data, address = sock.recvfrom(4096)
            print(f'Received message from {address}: {data.decode()}')
        except socket.timeout:
            # Timeout occurred, no data received
            pass

if __name__ == "__main__":
    udp_communicate()
