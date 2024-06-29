# P2P-Implementation-of-Distributed-Algorithms
The objective of this project is to design and implement a distributed consensus al-
gorithm using a network of Raspberry Pi devices. The project specifically focuses on
achieving consensus among multiple nodes through a coordinated approach, where a cen-
tral coordinator initiates the process. The primary aim is to enable each node to reach
an average consensus value through iterative communication with its neighbors.
The consensus algorithm implemented in this project is a fundamental problem in
distributed computing, where the goal is to have all nodes in a distributed system agree
on a certain value or state. This is particularly important in systems where reliability,
fault tolerance, and consistency are critical. By using Raspberry Pi devices, this project
demonstrates a practical approach to solving the consensus problem in a distributed
network.

Distributed Algorithms are a class of algorithms specifically designed to operate in
distributed computing environments. In such environments, multiple computing nodes
(which can be physically separated) communicate and coordinate with each other to
achieve a common goal. These algorithms are integral to distributed systems, where the
nodes work collectively to solve problems that are beyond the capabilities of a single
machine.


Key Characteristics of Distributed Algorithms:
1. Concurrency: Multiple nodes perform computations simultaneously.
2. Communication: Nodes exchange messages to coordinate actions and share infor-
mation.
3. Fault Tolerance: The system can continue to function even if some nodes fail.
4. Scalability: The system can handle an increasing number of nodes without signifi-
cant performance degradation.
5. Decentralization: No single node has complete control; instead, control and data
are distributed across nodes.

Goals
1. Single File Implementation: Implementing the Distributed Consensus Algorithm in a single file where all data is available in the same file.
2. Multi File Implementation: Implementing the Distributed Consensus Algorithm in a same device where all data are in different files.
3. Communication between Raspberry Pi: Establishing connection between two raspberry pi and Communicating between each other using different networking Protocols like UDP,TCP.
4. Consensus using LAN connection: Implementing the Consensus Algorithm for raspberry pi by setting up each raspberry pi as a node. Every nodes are connected through each other using ethernet (LAN).
5. Consensus using WiFi connection: Implementing the Consensus Algorithm for raspberry pi by setting up each raspberry pi as a node. Every nodes are connected through each other using internet. All raspberry pi are not required to be in the same network or LAN in this case.
6. Single Raspberry Pi Control: The above algorithms are then implemented by only activating the coordinator node. The coordinator node sends the files to the nodes, runs them there, stores data for each iteration and sends them back to the coordinator.
