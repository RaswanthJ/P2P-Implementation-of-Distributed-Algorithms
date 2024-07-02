import time
import sys
import matplotlib.pyplot as plt
import csv

def read_state(node_id):
    #This function is used to read the file n_{node_id}.txt file
    try:
        with open(f'n_{node_id}.txt', 'r') as file:
            return float(file.read().strip())
    except FileNotFoundError:
        return None

def write_state(node_id, state):
    #This function is used to write in the file n_{node_id}.txt file for updating states after iterations
    with open(f'n_{node_id}.txt', 'w') as file:
        file.write(str(state))

def log_state(node_id, iteration, state):
    #This function is used to append the current state values at every iteration for storing them and plotting them
    with open(f'log_{node_id}.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([iteration, state])

def node_process(node_id, neighbors,x, alpha=0.1, max_iterations=1):
    #We first read the file to get node data
    st = read_state(node_id)
    state = st
    global ii
    
    for iteration in range(max_iterations):
        new_state = state
        
        # To Receive states from all neighbors
        received_states = []
        for neighbor_id in neighbors:
            neighbor_state = read_state(neighbor_id)   #Neighbor states are read here
            if neighbor_state is not None:
                received_states.append(neighbor_state) #If neighbor is not empty we add in the received states list
            else:
                #If neighbor data is not present we come to this section
                #The values stored in the csv file then are used to determine the previous state values
                #These previous state values are then used as current state.
                #There will be deviations doing this but since this scenario is rare we just do this to make sure that program doesnt crash
                req = 0    
                with open(f'log_{neighbor_id}.csv', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        req = row[1]
                received_states.append(float(req))
        
        if received_states:
            #The algorithm part of the consensus comes here.
            #The algorithm used here is for average consensus
            state_update = sum([(neighbor_state - state) for neighbor_state in received_states])
            new_state = state + alpha * state_update
        
        state = new_state
        time.sleep(0.05)
        #Sleep time is added for synchronising all nodes so that no nodes get faster or slower in reading and writing the data
        
    #Now the changes are then written into the text file and then also added to the csv file
    write_state(node_id,state)   #Writing changes in file
    val_list.append(state)       #Storing the previous values
    print(f"Node {node_id} in {x}th iteration: {state}")
    log_state(node_id, ii, state) #This line adds the values to csv file
    ii+=1                        #ii counts the iterations that are to be done

ii = 1
node_id = 1
#The following four lines will have the inputs that will be received from the coordinator.py file
neighbors = [int(n) for n in sys.argv[1].split(',')]   
iteration_number = int(sys.argv[2])
alpha = float(sys.argv[3])
iter = int(sys.argv[4])
t_list = []
val_list = []

for i in range(0,iteration_number):
    t_list.append(i+1)   
    node_process(node_id, neighbors,i+1,alpha,iter)
    #We give a initial sleep time of 1second to give time for synchronisation
    time.sleep(1)
    print("-----------------------")
    