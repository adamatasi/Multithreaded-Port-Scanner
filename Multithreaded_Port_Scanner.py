# Multithreaded Port Scanner

#pip install pyfiglet OR pip3 install pyfiglet

''' First of all, we will need to import some libraries: '''
import pyfiglet #This used for the banner
from queue import Queue
import socket
import threading

#Nice banner using your name
my_name = pyfiglet.figlet_format("Adam Atasi", font = "slant")
print(my_name)

'''
Socket will be used for our connection attempts to the host at a specific port.
Threading will allow us to run multiple scanning functions simultaneously.
Queue is a data structure that will help us to manage the access of multiple threads on a single
resource, which in our case will be the port numbers. Since our threads run simultaneously and scan
the ports, we use queues to make sure that every port is only scanned once.
'''



'''Then, we will also define three global variables that we will use throughout the various functions: '''
target = "127.0.0.1" # OR could be your router or a domain name
queue = Queue()
open_ports = []

'''
Target is obviously the IP-Address or domain of the host we are trying to scan.
The queue is now empty and will later be filled with the ports we want to scan.
And last but not least we have an empty list, which will store the open port numbers at the end.
'''



#We start by implementing the portscan function.
def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False
'''
Here you can see a basic try-except block, in which we try to connect to our target on a specific port.
If it works, we return True, which means that the port is open. Otherwise, we return False, which
means that there was an error and we assume that the port is closed.
'''



def get_ports(mode):
    if mode == 1:
        for port in range(1, 1024):  #standardized ports (reseved for http, ssh, ftp, telnet, and so on)
        							  #You can change the range to (1, 65535) to scan all ports
            queue.put(port)
    elif mode == 2:
        for port in range(1, 49152):
            queue.put(port)
    elif mode == 3:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            queue.put(port)
    elif mode == 4:
        ports = input("Enter your ports (seperate by blank):")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)
'''
In this function we have defined four possible modes. The first mode scans the 1023 standardized
ports. With the second mode we add the 48,128 reserved ports. By using the third mode we focus on
some of the most important ports only. And finally, the fourth mode gives us the possibility to
choose our ports manually. After that we add all our ports to the queue.
'''
'''
Notice that when we enter the ports in mode four, we are splitting our input into a list of strings.
Therefore, we need to map the typecasting function of the integer data type to every element of the
list in order to use it.
'''




#Multithreading
'''
The next thing we need to do is defining a so-called worker function for our threads. This function
will be responsible for getting the port numbers from the queue, scanning them and printing the
results.
'''
def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print("Port {} is open!".format(port))
            open_ports.append(port)
		########
        #else:
        	#print("Port {} is closed!".format(port))
		########
'''
It is quite simple. As long as the queue is not empty, we get the next element and scan it. If the port
is open, we print it and if it is not we print that as well. What we additionally do when a port is open,
is adding it to our open_ports list.
'''
'''
Note: I would recommend not printing the information that a port is closed, since this information is
useless and makes our output confusing. You can basically remove the else-branch.
From ######## till ########
OR UNCOMMENT else: and the next line
'''





'''
So, now that we have implemented the functionality, we are going to write our main function, which
creates, starts and manages our threads.
'''
def run_scanner(threads, mode):

    get_ports(mode)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker) #Notice that we are not calling the function worker()
        										 # We are just referring to the worker function without calling it
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("Open ports are:", open_ports)
'''
In this function, we have two parameters. The first one is for the amount of threads we want to start
and the second one is our mode. We load our ports, depending on the mode we have chosen and we
create a new empty list for our threads. Then, we create the desired amount of threads, assign them
our worker function and add them to the list. After that, we start all our threads and let them work.
They are now scanning all the ports. Finally, we wait for all the threads to finish and print all the open
ports once again
'''

run_scanner(100, 1) #You can change 100 to 500 to scan 500 ports in a second

'''
By running the function like this, we scan all standardized ports. For this, we are using a hundred
threads. This means that we scan around one hundred ports per second. You can increase that
number if you want. The fastest I could go with my computer was around 800 port scans per second.
'''

#Run the script
# python port_scanner.py
'''
The results should look like this:
Port 22 is open!
Port 25 is open!
Port 80 is open!
Port 110 is open!
Port 119 is open!
Port 143 is open!
Port 443 is open!
Port 465 is open!
Port 554 is open!
Port 563 is open!
Port 587 is open!
Port 631 is open!
Port 993 is open!
Port 995 is open!
Open ports are: [22, 25, 80, 110, 119, 143, 443, 465, 554, 563, 587, 631, 993, 995]
'''