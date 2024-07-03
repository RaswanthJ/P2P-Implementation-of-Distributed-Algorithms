import socket
import json
import threading 
import time
import os
import subprocess
import csv
import pandas as pd
import matplotlib.pyplot as plt

#The sender.py code must be run befor the coordinator.py code. Coordinator.py is responsible to start the consensus in the node and collect back the csv from the nodes and plot them.
#Sender.py is responsible to send every node details, files to every node and run them.


#The below dictionary contains ip address, port number for ssh communication and user name
#Make sure to only use port number as 22 as its the port allotted by default for ssh and scp communication
#If any nodes are added their ip and ports and username are to be added to the dictionary in the same format with the correct node ids
ns = {
    1: {"ip": "169.254.142.206", "port": 22, "user": "rasp3"},
    2: {"ip": "169.254.71.146", "port": 22, "user": "rasp1"},
}

#The bottom two lines are to be filled with the ip address and port number of coordinator for udp communication. This is a one time step
local_ip = "169.254.253.114"
local_port = 12345

def print_time_taken(description, start_time):
    end_time = time.time()
    print(f"{description} took {end_time - start_time:.6f} seconds")
    #This function is used to print the time taken from start of each step when the start_time inputted in the function is the time recorded at the start
    #Currently in this code all the print_time_functions are removed. If necessary the user can use this to get an idea of execution time

def send_init_message(ip, port,iteration_number,neighbors,alpha,iter,nodes,state):
    #This function is responsible to send initialisation message of all the nodes when the coordinator iteration starts.
    #Along with the initialisation message things like iteration number, alpha, sleeptime,etc.. are sent.
    message = {
        "init": "INIT",
        "inum": iteration_number,
        "alpha": alpha,
        "iter": iter,
        "neighbors": neighbors,
        "nodes": nodes,
        "num_nodes": num_nodes,
        "sleep_time" : sleep_time,
        "state" : state
    }
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(message).encode('utf-8'), (ip, port))       #This line sends all the above data in message to the ip of the node and its port.
        #ip and port in the above statement denotes the ip and port in which the destination nodes listens

def send_messages_to_node(ip, port, neighbors, nodes,iteration_number,alpha,iter,state):
    send_init_message(ip, port, iteration_number,neighbors,alpha,iter,nodes,state)
    
def data_extractor(fl,d):
    #This function is responsible to take all the data from the csv files received from the nodes and collect the data in them and store them in the data list for plotting
    data = []
    with open(f"node{fl}_state.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader: 
            data.append(float(row[1]))
    d.append(data)


if __name__ == "__main__":
    #The nodes list contains every nodes ip address along with the port which the node listens. The above line is to changed while changing the order and number of nodes.
    #The tuple at index 0 represents node 1 and index 1 represents node 2 and so on.
    #Its important to make sure the node numbers match with their ip addresses in both coordinator and node.py file
    nodes = [("169.254.142.206",12345), ("169.254.71.146",12345)]
    #In this program even the initial states are sent from the coordinator file. The state list contains the initial states.
    #These intial states are sent to their respective nodes before the code is run
    states = [5,10]
    iteration_number = 100
    sleep_time = 0.01
    # For LAN connection sleep time can not be less than 0.0033 seconds for good results
    # For WiFi connection sleep time can not go lesser than 0.1 seconds for accurate results
    neighbors = [
        [],
        [2],
        [1]
    ]
    # Neighbor list is supposed to be modified to change the edges of the graph which is then responsible for change in communication
    num_nodes = 2    #Change this when there is a change in number of nodes
    alpha = 0.1
    iter = 1
    start_time = time.time()       #This measures the time taken for each step for our use. These can be removed to make the code run faster
    print(start_time)
    #This portion of the code is responsible to perform threading so that all the messages sent to the nodes are sent simultaneously.
    #The threads list initially stores all the threads that are to be started. Its then initiated in the loop below for messages to be sent simultaneously
    threads = []
    counter = 0
    for node in nodes:
        thread = threading.Thread(target=send_messages_to_node, args=(node[0], node[1], neighbors, nodes,iteration_number,alpha,iter,states[counter]))
        threads.append(thread)
        counter+=1
    time.sleep(1)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    #The below function waits for done messages to come from nodes so that it can plot the graphs for the data that is received
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((local_ip,local_port))
        cnt = 0
        while(cnt<num_nodes):
            s.settimeout(sleep_time)
            try:
                data, _ = s.recvfrom(1024)
                if data:
                    node_id, msg = data.decode('utf-8').split(',')
                    if(msg=="done"):
                        cnt+=1
                    
            except socket.timeout:
                pass
            
    #The below part of the code is completely for extracting data from csv and plotting them
    d_list = []
    time = []
    for i in range(0,num_nodes):
        data_extractor(i+1,d_list)
    for i in range(1,iteration_number+1):
        time.append(i)
    for i in range(0,num_nodes):
        plt.plot(time,d_list[i], label=f'x{i+1}(t)')
    plt.xlabel('Time')
    plt.ylabel('State')
    plt.title('State Evolution of Nodes')
    plt.legend()
    plt.grid(True)
    plt.show()