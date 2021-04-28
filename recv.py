import socket
import hashlib
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
from collections import namedtuple
Packet = namedtuple("Packet", ["SeqN","Data", "CheckSum"])

BUFSIZ = 2048
# rdt vars
lossRate = 0
timeout = 0
Port = 8009
rcvPort = 8008
rcvIP = "127.0.0.1"
rcvAdd = (rcvIP,rcvPort)
sd = None

def CheckSum(Data):
    hash = hashlib.md5(Data)
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
    current = 0
    winSize = 4
    while(True):
        print(RecvData())
        SendData()
    return
def SendData():
    return
def RecvData():
    (rmsg, peer) = sd.recvfrom(2048)
    Data = Packet(tuple.to_bytes())
    Data.CheckSum = CheckSum(Data.Data)
    return rmsg
RDT()