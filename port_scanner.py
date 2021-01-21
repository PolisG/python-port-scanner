from queue import Queue
import threading
import socket

localhost = '127.0.0.1'
queue = Queue()
open_ports = []

def port_scanner(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((localhost, port))
        return True
    except:
        return False


def select_ports(select):
    if select == 1:
        for port in range(0, 1023):
            #The range of port numbers from 0 to 1023 are the well-known ports or system ports.
            queue.put(port)
    elif select == 2:
        for port in range(1024, 49151):
            #The range of port numbers from 1024 to 49151 are the registered ports.
            queue.put(port)
    elif select == 3:
        for port in range(0, 49151):
            #well-known and registered ports.
            queue.put(port)
    elif select == 4:
        for port in range(49152, 65535):
            #The range of port numbers from 49152 to 65535 contains dynamic or private ports.
            queue.put(port)
    else:
        #user specified ports.
        ports = input("Enter the ports you want to scan (seperate with space):")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)

#worker function - get port numbers from queue, scan them and print results
def worker():
    #As long as the queue is not empty, get the next element and scan it.
    while not queue.empty():
        port = queue.get()
        if port_scanner(port):
            print(f'Port {port} is open!')
            open_ports.append(port)

#main function - creates, starts and manages threads
def main(threads, select):
    select_ports(select)
    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    if not open_ports:
        print("No open ports!")
    else:
        open_ports.sort()
        print("Open ports are: ", open_ports)


print("Option 1: 0-1023 ports\nOption 2: 1024-49151 ports\nOption 3: 0-49151 ports\nOption 4: 49152-65535 ports")
select = int(input("Please type your option: "))
main(1024, select)
