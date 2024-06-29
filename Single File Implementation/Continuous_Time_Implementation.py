import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt


def compute_state(L, x0, t):
    exp_Lt = expm(L * t)            #This function performs the continuous time state calculation 
    xt = np.dot(exp_Lt, x0)         #Expm calculates exponents of matrices
    return xt 
#The state space equation x dot = Ax is solved and its simplified solution is used for calculation

num_nodes = 5

#This Array consists of the Initial states of each node
x0=np.array([6,4,7,5,4])       

#This is Adjacency Matrix which consists of the neighbor data for each node
Adj=np.array([[0,1,0,0,0],[1,0,1,0,0],[0,1,0,1,1],[0,0,1,0,1],[0,0,1,1,0]])             

#This is Degree Matrix in which each diagonal element gives the number of degree of each node
D = np.array([[1,0,0,0,0],[0,2,0,0,0],[0,0,3,0,0],[0,0,0,2,0],[0,0,0,0,2]])             

#L is Laplacian which is computed from Degree Matrix and Adjacency Matrix
L = np.subtract(D,Adj)                                                                   

#Inorder to change the number of nodes, the num_nodes, Adj, D are supposed to be changed accordingly
#No other changes are required other than these
#Inorder to change the time of iterations the below function can be modified accordingly

t_values = np.linspace(0, 5, 100)  # Time goes from first value to second value
                                   # Last parameter gives number of steps of iterations

x_values = np.array([compute_state(-L, x0, t) for t in t_values])   
#compute_state function is called to find new values

print(x_values[-1])   
#x_values[-1] returns the last value (value after final iteration) of the whole process              
print("--------------------------")



#The below code is solely for plotting graphs for each state
for i in range(0,num_nodes):
    plt.plot(t_values, x_values[:, i], label=f'x{i+1}(t)')
plt.xlabel('Time (t)')
plt.ylabel('State (x)')
plt.legend()
plt.title('State evolution over time')
plt.grid(True)
plt.show()
