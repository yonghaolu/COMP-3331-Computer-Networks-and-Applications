#Python version 3.6
#Created by Yonghao Lu, z5125710
from socket import *
from datetime import datetime
import time
import sys

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

#creat an UDP socket
clientSocket = socket(AF_INET,SOCK_DGRAM)
addr = (serverIP,serverPort)

rtt_list = []
packet_lost = 0

for i in range(15):
    #creat time stamp
    timeStamp = datetime.now().isoformat(sep = ' ')[:-3]
    ping_message = f'{i+3331} PING seq = {i}' + ', ' + timeStamp + '\r\n'

    time_send = datetime.now()
    
    #send message
    clientSocket.sendto(ping_message.encode(),addr)

    try:
        clientSocket.settimeout(0.6) #600ms
        responsedMessage, serverAddress = clientSocket.recvfrom(1024)

        time_receive = datetime.now()

        rtt = round((time_receive - time_send).total_seconds() * 1000)

        rtt_list.append(rtt)
        print(f"{3331+i} ping to {serverIP}, seq = {i}, rtt = {rtt} ms")	
        clientSocket.settimeout(None)

    except timeout:
        packet_lost += 1
        print(f"{3331+i} ping to {serverIP}, seq = {i}, rtt = time out")

#print the report
print("\n")
print(f'Minimun RTT = {min(rtt_list)}ms')
print(f'Maximun RTT = {max(rtt_list)}ms')
print(f'Average RTT = {round(float(sum(rtt_list)/len(rtt_list)))}ms')
print(f'{float(packet_lost)/15 *100} % of packets have been lost through the network.')

clientSocket.close()











