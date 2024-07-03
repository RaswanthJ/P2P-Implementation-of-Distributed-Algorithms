# In this section we will be implementing consensus using multiple Raspberry Pi
The WiFi connection or LAN connection does not affect the code. The only change that will be made is the IP Addresses of each nodes. So in the actual node.py code the changes of local ips are made and in coordinator code the ips of all devices are changed. Other aspects of the code remain the same.
For LAN connected consensus the miminum sleeptime can go around 0.0033s for accuratie results whereas for WiFi we can go upto 0.1s for accurate results.
In other words one can do a maximum iterations of 250-200 in LAN and 1-10 in on internet consensus.
