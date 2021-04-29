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
lossRate = 0.3
timeout = 2 # not needed
Port = 8009
rcvPort = 8008
rcvIP = "127.0.0.1"
rcvAdd = (rcvIP,rcvPort)
sd = None

# Calculate md5 hash
def CheckSum(Data):
    hash = hashlib.md5(Data).digest()
    return hash

# Assign and bind a socket
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
        # Blocking wait for Receive
        rmsg = RecvData()
        # Check if Transfer Complete
        if(rmsg==b'FIN'):
            SendData(b'FIN')
            break
        # Simulate Loss
        if(random.random()<lossRate):
            print("Client Not Responding/Dropping Packet")
            time.sleep(timeout+1)
            continue
        # Deserialize the data
        data = pickle.loads(rmsg)
        print(data)
        msg = data.Data.decode("utf-8")
        print(msg)
        chk = CheckSum(data.Data)
        # print(chk)
        # print(data.CheckSum)
        # Verify Checksum and duplicate packet
        if chk==data.CheckSum:
            if(data.SeqN<len(Data)):
                print("Duplicate Packet!")
                continue
            print("Valid Checksum")
            Data.append(msg)
        else:
            print("Invalid Checksum")
        # Create and Send Ack
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