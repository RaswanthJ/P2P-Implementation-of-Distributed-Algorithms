import numpy as np
import matplotlib.pyplot as plt

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

x=np.array(x0)
x=x.reshape(1,num_nodes)
#Initial states are converted into np arrays for computation and is reshaped for matrix and vector calculations
t_values = [0]
#t_values are a list of time values which is recorded for plotting
h = 0.1
#h is the fraction at which changes are done in every iteration
for i in range(1,100):
    t_values.append(i)
    xnew = x[i-1]+h*np.matmul(-L,x[i-1])   
    #xnew = x[i-1]+h*np.matmul(-L,x[i-1]) this is the step of average consensus algorithm
    #xnew now contains the new state after every iteration
    xnew = xnew.reshape(1,num_nodes)
    x = np.append(x,xnew)
    #new state is added to the x array
    x=x.reshape(i+1,num_nodes)

print(x[-1])
#x[-1] returns the last value (value after final iteration) of the whole process

#The below code is solely for plotting graphs for each state
for i in range(0,num_nodes):
    plt.plot(t_values, x[:, i], label=f'x{i+1}(t)')
plt.xlabel('Time (t)')
plt.ylabel('State (x)')
plt.legend()
plt.title('State evolution over time')
plt.grid(True)
plt.show()
