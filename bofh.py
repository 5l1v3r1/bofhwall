#!/usr/bin/python3
"""
bofhwall - build July 5 2017
https://github.com/RomelSan/bofhwall

Bastard Operator From Hell - Firewall
This service listen in a port and send to the client a BOFH excuse.

Use this IPTABLE rule to redirect all traffic incoming from all ports to this service.
iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 1:65535 -j DNAT --to-destination HOST:PORT

If you redirect to localhost, you need this:
sysctl -w net.ipv4.conf.eth0.route_localnet=1

=> Bastard Operator From Hell everywhere.
"""

import socket
import sys
import random
import time

#-----------------------
# You can change the following:
config_ip = '127.0.0.1' #If using IPv6 then on line 46 change "socket.AF_INET" to "socket.AF_INET6"
config_port = 8080
#-----------------------
config_file = "excuses.txt"

file = open(config_file, 'r')
bofh_collection = file.readlines()

def send_random_bofh(conn, ip, port):
    pre_message = "Bastard Operator From Hell excuse is:\r\n"
    message =  random.choice(list(bofh_collection))
    message = message.rstrip()
    message_full = pre_message + message
    try:
        conn.sendall(message_full.encode("utf-8"))  # send it to client
        conn.close()  # close connection
        print('Sent Message to ' + ip + ':' + port)
        print('Message: ' + message + "\r\n")
    except:
        print('Port probed, remote host will not take the message\r\n')
    
def start_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    try:
        soc.bind((config_ip, config_port))
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    print('Socket now listening\r\n')

    # for handling task in separate jobs we need threading
    from threading import Thread

    # this will make an infinite loop needed for 
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        localtime = time.asctime(time.localtime(time.time()))
        print('Accepting connection from ' + ip + ':' + port + " at " + str(localtime))
        try:
            Thread(target=send_random_bofh, args=(conn, ip, port)).start()
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()
    soc.close()

start_server()  
