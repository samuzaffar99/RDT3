import socket
import hashlib
import pickle
import random
from collections import namedtuple
import time
import random
Packet = namedtuple("Packet", ["SeqN","Data", "CheckSum"])
Ack = namedtuple("Ack", ["Ack"])

# rdt vars
BUFSIZ = 1024
lossRate = 0.4
timeout = 2
Port = 8009
rcvPort = 8008
rcvIP = "127.0.0.1"
rcvAdd = (rcvIP,rcvPort)
sd = None

def CheckSum(Data):
    hash = hashlib.md5(Data).digest()
    return hash

def SocketAssign():
    try:
        global sd
        sd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sd.bind(("localhost",Port))
    except:
        print("Socket Assignment Failed!")
        return

def RDT():
    SocketAssign()
    # current = 0
    # winSize = 4
    filename = RecvData()
    Data = []
    while(True):
        rmsg = RecvData()
        # Transfer Complete
        if(rmsg==b'FIN'):
            SendData(b'FIN')
            break
        # Simulate Loss
        if(random.random()<lossRate):
            print("Client Not Responding/Dropping Packet")
            time.sleep(timeout+1)
            continue
        data = pickle.loads(rmsg)
        print(data)
        msg = data.Data.decode("utf-8")
        print(msg)
        chk = CheckSum(data.Data)
        # print(chk)
        # print(data.CheckSum)
        if chk==data.CheckSum:
            print("Valid Checksum")
            Data.append(msg)
        else:
            print("Invalid Checksum")
        ack = pickle.dumps(Ack(data.SeqN))
        SendData(ack)
    Output = " ".join(Data)
    print("Message Received:", Output)
    return

def SendData(message):
    sd.sendto(message, rcvAdd)
    return

def RecvData():
    (rmsg, peer) = sd.recvfrom(BUFSIZ)
    return rmsg

RDT()