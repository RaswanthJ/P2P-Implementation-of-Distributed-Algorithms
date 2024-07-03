# In this section we will be implementing consensus using multiple Raspberry Pi
The WiFi connection or LAN connection does not affect the code. The only change that will be made is the IP Addresses of each nodes. So in the actual node.py code the changes of local ips are made and in coordinator code the ips of all devices are changed. Other aspects of the code remain the same.
For LAN connected consensus the miminum sleeptime can go around 0.0033s for accuratie results whereas for WiFi we can go upto 0.1s for accurate results.
In other words one can do a maximum iterations of 250-200 in LAN and 1-10 in on internet consensus.
The same code of N1.py is supposed to be copied and pasted for other nodes with the name N{node_id}.py and the node_id in the code must be changed along with the ip_address
For LAN and Internet consensus the changes comes only in IP. We must make sure to use the correct IP for the type of consensus. Zero tier ip is to be used for Internet consensus and eth0 IP for ethernet based LAN consensus.
IP are obtained by giving the command ifconfig in terminal.
