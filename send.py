import socket
import hashlib
import os
import pickle
import random
import time
from collections import namedtuple

Packet = namedtuple("Packet", ["SeqN","Data","CheckSum"])
Ack = namedtuple("Ack", ["Ack"])

# Todo
# 1-Implement Timeout
# 2-Implement Reading from File
# 3-Implement GoBackN or Slective Repeat/ Currently using Stop and Wait

# rdt vars
BUFSIZ = 1024
lossRate = 0.3 # not needed
timeout = 2
Port = 8008
rcvPort = 8009
rcvIP = "127.0.0.1"
rcvAdd = (rcvIP,rcvPort)
sd = None

# Calculate md5 hash
def CheckSum(Data):
    hash = hashlib.md5(Data).digest()
    return hash

# Assign and bind a socket
def SocketAssign():
    global sd
    try:
        sd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sd.bind(("localhost",Port))
        sd.setblocking(0)
    except:
        print("Socket Assignment Failed!")
        return

def RDT():
    SocketAssign()
    # Data = SplitFile()
    Data = ["Hello!","Please","Send Me","the CN","Assignment","18K-0169","Syed Abdullah Muzaffar","CS-6H"]
    SendData(filename.encode('utf-8'))

    for i in range(len(Data)):
        # Create Packet and Convert into bytes
        data = bytes(Data[i],'utf-8')
        chk = CheckSum(data)
        pkt = Packet(i,data,chk)
        bpkt = pickle.dumps(pkt)
        while(True):
            try:
                # Send Packet
                SendData(bpkt)
                print("Sent Packet#", i)
            except:
                print("Error Sending Data")
            # Receive Ack
            start = time.time()
            tflag = 0
            while(True):
                try:
                    # Check timer
                    if(time.time()-start>=timeout):
                        print("Timeout!")
                        tflag=1
                        break
                    ack, peer = sd.recvfrom(BUFSIZ)
                    break
                except OSError:
                    # print("No Data")
                    continue
            if(tflag==1):
                continue
            Resp = pickle.loads(ack)
            print(Resp)
            if(Resp.Ack==i):
                # Correct Ack Received
                break
            else:
                # Wrong Ack Received
                continue
    print("All Data Sent")
    sd.setblocking(1)
    while(True):
        SendData(b'FIN')
        Resp = RecvData()
        if Resp == b'FIN':
            print("Closing Server")
            break
    return

def SendData(message):
    sd.sendto(message, rcvAdd)
    return

def RecvData():
    (rmsg, peer) = sd.recvfrom(BUFSIZ)
    return rmsg




# DEPRECATED

# def rdt_send(data,ack):
#     chk = CheckSum(data)
#     sndpkt = makepkt(ack,data,chk)
#     udt_send(sndpkt)
#     # start_timer()
# def rdt_rcv(rcvpkt):
#     return sd.recvfrom(BUFSIZ)
# def udt_send(pkt):
#     sd.sendto(pkt, rcvAdd)

# def chksum():
#     return 0
# def makepkt(ack,data,chksum):
#     return (ack,data,chksum)

# def isACK(rcvpkt,ack):
#     return rcvpkt[0]==ack

filename = "1.png"
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "send/" + filename
abs_file_path = os.path.join(script_dir, rel_path)

# deprecated fun for reading a file
def SplitFile():
    try:
        file = open(abs_file_path, 'rb')
        Data = file.read()
        file.close()
        return Data
    # ChunkSize = 512
    # SplitData = []
    # fpath = "send/1.png"
    # try:
    #     file = open(abs_file_path,'rb')
    #     print("true1")
    #     while(file):
    #         SplitData.append(file.read(ChunkSize))
    #     print("true2")
    #     file.close()
    #     print("File Split!")
    #     return SplitData
    except:
        print("Error Reading File!")
        return None


RDT()