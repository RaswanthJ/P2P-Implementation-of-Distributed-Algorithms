import numpy as np
import subprocess

#This python file is responsible to initiate all the nodes by sending neighbor data, sleep, alpha value, iterations values
#States of a node are directly linked to the text file. Inorder to update the state go directly to text file and change them.

def start_node(node_id, neighbors,iteration_number,alpha,iter):
    node_script = f'node_{node_id}.py'
    subprocess.Popen(['python', node_script, ','.join(map(str, neighbors)),str(iteration_number),str(alpha),str(iter)])
    #Initiates the files node_{node_id} as a subprocess in this file. The nodes then start the read and write operations

def clear_csv(file_path):
    with open(file_path, 'w') as file:
        pass  # Opening in write mode without writing anything truncates the file



if __name__ == "__main__":
    iteration_number = 50        #The number of iterations that happen is here (Number of read and write)
    num_nodes = 5                #num_nodes is to be changed if we add or remove the nodes from the process
    alpha = 0.1                  #Alpha is the fractional change that is brought in every iteration
    iter = 1                     #Number of correction that happen in each iteration is termed to be alpha
    clear_csv('log_1.csv')
    clear_csv('log_2.csv')
    clear_csv('log_3.csv')
    clear_csv('log_4.csv')
    clear_csv('log_5.csv')
    #The above lines clears all the .csv file
    
    neighbors_list = [
        [],         #For 1-base indexing
        [2,5],      # Neighbors of node 1
        [1,3],      # Neighbors of node 2
        [2,4],      # Neighbors of node 3
        [3,5],      # Neighbors of node 4
        [1,4]       #Neighbors of node 5
    ]
    
    for node_id in range(1, num_nodes + 1):
        start_node(node_id, neighbors_list[node_id],iteration_number,alpha,iter)
        #Every node is initiated here.