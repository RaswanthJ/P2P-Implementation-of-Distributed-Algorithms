import socket
import pandas as pd
import time
import json
import matplotlib.pyplot as plt
import os
import paramiko

#Before running the sender file make sure to create the files N2.py, N3.py, ... till the number of nodes and make the below changes in the respective files and save all the files in the same folder along with coordinator.py and sender.py

#This file is for node 1. Other nodes has the same code except for the following variables. All the values must match with the values in coordinator file.
#          node_id in to the node id given in coordinator
#          local_ip to the ip of the device that was noted
#          port_num to the port number used for communication
#Unlike the previous sections, here we make the files in the same coordinator. Here the N1.py is already ready. We need to copy this file and make the above changes in order to run the consensus

# When switching from LAN to Internet as a mode of communication the IPs of the coordinator along with the ips in the node is supposed to be changed. There are no other changes other than that
# The node_id in each node is the 1-based index of nodes list in the coordinator file that contains the ip of the particular node.

def send_file(file,ip,user,path):
    #This function uses paramiko module the send a file from the nodes back to the coordinator.
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,username=user,port=22)

        sftp = ssh.open_sftp()
        remote_path = os.path.join(path,os.path.basename(file))
        sftp.put(file,remote_path)
        sftp.close()
        ssh.close()
        print(f"File {file} successfully sent.")
    except Exception as e:
        print(f"File Transfer Failed due to {e}")
#All the variables below are global. These data will be changed once the intiation message from the coordinator arrives.
#The data below are not data that will be used for iteration
u_st = 0            #u_st stores the start time of the process
neighbors=[]        #This list stores the neighbor data
nodes = []          #This list stores IP Address and port numbers 
start_time = 0
node_id = 1
num_nodes = 1
port_num = 12345
val_list = []         #This list stores the node values at each iteration of its own node
neighbor_prev_states=[]   #This stores the value of previous states in this list
sleep_time = 1       #This is global sleeptime variable
local_ip = "169.254.142.206"     #Here the local ip of the nodes are found and entered
user_name = "rasp2"               #This is coordinator's user name and its supposed to be entered as a string here
coor_ip = "169.254.253.114"      #This is coordinator's ip address and its supposed to be entered as a string here
coor_port = 12345

def print_time_taken(description, start_time):
    end_time = time.time()
    print(f"{description} took {end_time - start_time:.6f} seconds")
    #This is the same print_time_taken fucntion as in coordinator.py file

def write_state(node_id, state):
    #This function is responsible to write the state variable in n__{node_id}.txt
    with open(f'n_{node_id}.txt', 'w') as file:
        file.write(str(state))

def send_state_to_neighbors(ip, port, node_id, state):
    #This function sends the state of this node to the neighbor nodes whose ip address and port are the variable ip and port using UDP Protocol
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        #Data is sent and received as a string with node_id and state separated by comma
        message = f"{node_id},{state}"
        s.sendto(message.encode('utf-8'), (ip, port))

def listen_to_neighbors(s,neighbor_states):
    #This function is called when we need to listen to neighbor to get their states.
    s.settimeout(sleep_time*0.9)
    #Time out is set at 90 percent of sleeptime so that the listening process stops and the node can proceed on using previous state values for computation
    try:
        data, _ = s.recvfrom(1024)      #Data is received here
        if data:
            neighbor_id, neighbor_state = data.decode('utf-8').split(',')    #Data is extracted after decode and splitting.
            neighbor_states[int(neighbor_id)] = float(neighbor_state)        #Global neighbor states list is modified to add new states in it for computation
            #print(f"--->Neighbor {neighbor_id} has state value :",neighbor_state)
            #Above line can be uncommented to see what states are received from each neighbor
            
    except socket.timeout:
        pass



def run_consensus(s,alpha,iter,x):
    global neighbor_prev_states,sleep_time,start_time
    state = 0
    neighbor_states = [-1]*(num_nodes+1)      #Neighbor states are made -1 initially for us to identify whether data has been recieved from a node
    validity = [1]*(num_nodes+1)              #Validity gives the authenticity of data like neighbor states
    with open(state_file, 'r') as f:
        state = float(f.read().strip())
    for iteration in range(iter):
        # Send state to all neighbors
        for neighbor in neighbors[node_id]:
            ip = nodes[neighbor-1][0]
            port = nodes[neighbor-1][1]
            send_state_to_neighbors(ip, port, node_id, state)

        # This loop listens to neighbors
        for neighbor in neighbors[node_id]:
            listen_to_neighbors(s,neighbor_states)
        neighbor_prev_states.append(neighbor_states)   #All these values are appended to previous states list for later use
        
        for neighbor in neighbors[node_id]:
            #We check whether the data has arrived or not in this loop and then make use of previous state if the data from neighbor has not been arrived
            if(neighbor_states[neighbor]==-1 and x!=1):
                if(neighbor_prev_states[-2][neighbor]!=-1):
                    #print("Prev state used: " ,neighbor_prev_states[-2][neighbor]," of neighbor:",neighbor)
                    #Use the above commented statement to identify whether there were any use of prev states
                    neighbor_states[neighbor] = neighbor_prev_states[-2][neighbor]
                else:
                    validity[neighbor]=0
        #state_update = sum( neighbor_states[neighbor] - state for neighbor in neighbors[node_id])
        state_update = 0
        
        #The algorithm part of the distributed consensus goes here.
        #--------------------------------------------------------
        #The below loop is used for average consensus
        for neighbor in neighbors[node_id]:
            if validity[neighbor]==1:
                state_update += (neighbor_states[neighbor] - state)
        state += alpha * state_update
        #--------------------------------------------------------
        
        #The below line is responsible to add the value from each iteration into the csv file.
        pd.DataFrame([[x, state]], columns=["Iteration", "State"]).to_csv(csv_file, mode='a', header=False, index=False)
        # print(f"Node {node_id} Iteration {x}: State = {state}")
        # print_time_taken(f"Iteration {x}:",u_st)
        # Sleep to synchronize with other nodes
        sle = max(0,sleep_time - (time.time()-u_st-sleep_time*(x-1)))
        time.sleep(sle)     #This makes our program sleep for the required time
        write_state(node_id,state)   #Writes the new computed state in the text file
        val_list.append(state)

def clear_csv(file_path):
    #Used to clear the csv file
    with open(file_path, 'w') as file:
        pass

if __name__ == "__main__":
    #Actual code starts here
    iterations = 50
    alpha = 0.1
    iter = 1
    clear_csv(f"node{node_id}_state.csv")
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((local_ip, port_num))
        #Our program waits for data to arrive from the coordinator node.
        #The below while loop breaks when the initiation message reaches this node and the actual computation starts after that
        while True:
            data, _ = s.recvfrom(1024)
            if data:
                message = json.loads(data.decode('utf-8'))
                #If message has INIT value the remaining part of the message is then broken down to extract the vales
                if message.get("init") == "INIT":
                    print("INITIATED")
                    #All other values like neighbors, neighbor ips, ports , sleep time are extracted from the message
                    nodes = message["nodes"]
                    neighbors = message["neighbors"]
                    iterations = message["inum"]
                    iter = message["iter"]
                    alpha = message["alpha"]
                    num_nodes = message["num_nodes"]
                    sleep_time = message["sleep_time"]
                    state_sent = message["state"]
                    
                    #State file and csv file paths are saved in a variable as a string
                    state_file = f"n_{node_id}.txt"
                    csv_file = f"node{node_id}_state.csv"
                    num_iterations = 50
                    alpha = 0.1  # Step size

                    #The state received from coordinator is initially written in the text file
                    #Text file does not exist in the first time implementation. Hence the write fucntion creates a text file and stores the value.
                    write_state(node_id,state_sent)
                    state = state_sent
                    time_list =[0]
                    val_list.append(state_sent)
                    time.sleep(3)
                    #Intial sleep time of 3 seconds ensures that all the program have optimal time to do the preprocessing and also helps in synchronisation
                    u_st = time.time()
                    for i in range(1,iterations+1):
                        #The consensus iterations happen here.
                        run_consensus(s,alpha,iter,i)
                        time_list.append(i)
                        
                    
                    # The below three lines are responsible to send done message back to the coordinator for it to conclude the process by plotting the graph
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                        message = f"{node_id},done"
                        s.sendto(message.encode('utf-8'), (coor_ip,coor_port))
                    
                    #The two lines below are responsible to send the .csv file back to the coordinator
                    path = f"/home/{user_name}/Desktop/Single_Pi_Control/"
                    send_file(csv_file,coor_ip,user_name,path)
                    
                    #The below lines are for plotting. Since these data are sent back to the coordinator there is no necessity to have these lines in our code.
                    # plt.plot(time_list, val_list , label='x(t)')
                    # plt.xlabel('Time')
                    # plt.ylabel('State')
                    # plt.title(f'State Evolution of Node {node_id}')
                    # plt.legend()
                    # plt.grid(True)
                    # plt.show()
                    # break