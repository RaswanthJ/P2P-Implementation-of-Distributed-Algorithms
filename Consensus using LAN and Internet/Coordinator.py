import socket
import json
import threading 
import time

def print_time_taken(description, start_time):
    end_time = time.time()
    print(f"{description} took {end_time - start_time:.6f} seconds")
    #This function is used to print the time taken from start of each step when the start_time inputted in the function is the time recorded at the start
    #Currently in this code all the print_time_functions are removed. If necessary the user can use this to get an idea of execution time

def send_init_message(ip, port,iteration_number,neighbors,alpha,iter,nodes):
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
        "sleep_time" : sleep_time
    }
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(message).encode('utf-8'), (ip, port))   #This line sends all the above data in message to the ip of the node and its port.
        #ip and port in the above statement denotes the ip and port in which the destination nodes listens

def send_messages_to_node(ip, port, neighbors, nodes,iteration_number,alpha,iter):
    send_init_message(ip, port, iteration_number,neighbors,alpha,iter,nodes)

if __name__ == "__main__":
    nodes = [("127.0.0.1",12345), ("127.0.0.1",12346), ("127.0.0.1",12347), ("127.0.0.1",12348), ("127.0.0.1",12349)]   #Node information is stored in this list
    #The nodes list contains every nodes ip address along with the port which the node listens. The above line is to changed while changing the order and number of nodes.
    #The tuple at index 0 represents node 1 and index 1 represents node 2 and so on.
    #Its important to make sure the node numbers match with their ip addresses in both coordinator and node.py file
    iteration_number = 100   #Its upto the user to decide the number of iterations. More the iterations accurate are the results
    sleep_time = 0.01        #Sleep time has some constraints
    # For LAN connection sleep time can not be less than 0.0033 seconds for good results
    # For WiFi connection sleep time can not go lesser than 0.1 seconds for accurate results
    neighbors = [
        [],
        [2,3,4,5],
        [1,3,4,5],
        [1,2,4,5],
        [1,2,3,5],
        [1,2,3,4]
    ]
    # Neighbor list is supposed to be modified to change the edges of the graph which is then responsible for change in communication
    num_nodes = 5     #Change this when there is a change in number of nodes
    alpha = 0.1       
    iter = 1
    start_time = time.time()  #This measures the time taken for each step for our use. These can be removed to make the code run faster
    threads = []
    #This portion of the code is responsible to perform threading so that all the messages sent to the nodes are sent simultaneously.
    #The threads list initially stores all the threads that are to be started. Its then initiated in the loop below for messages to be sent simultaneously
    for node in nodes:
        thread = threading.Thread(target=send_messages_to_node, args=(node[0], node[1], neighbors, nodes,iteration_number,alpha,iter))
        threads.append(thread)
    time.sleep(1)
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Initialization messages sent to all nodes.")