import socket
from tkinter import *
from tkinter import messagebox
import hashlib
import os
import struct
import pickle
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
from collections import namedtuple
Packet = namedtuple("Packet", ["SeqN","Data","CheckSum"])
Ack = namedtuple("Ack", ["Ack"])

# Todo
# 1-Implement Timeout
# 2-Implement Reading from File

BUFSIZ = 2048
# rdt vars
lossRate = 0
timeout = 0
Port = 8008
rcvPort = 8009
rcvIP = "127.0.0.1"
rcvAdd = (rcvIP,rcvPort)
sd = None
filename = "1.png"
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "send/" + filename
abs_file_path = os.path.join(script_dir, rel_path)

def CheckSum(Data):
    hash = hashlib.md5(Data).digest()
    return hash

# def build_pkts(file_data):
#     """Takes raw data to be sent and builds a list of pkt named tuples"""
#     seq_num = 0
#     pkts = []
#     mss= 500
#     HEADER_LEN = 8
#     sent = 0
#     to_send = min(mss - HEADER_LEN, len(file_data) - sent)
#     while to_send > 0:
#         # Build a pkt named tuple and add it to the list of packets
#         pkts.append(Packet(SeqN = seq_num, CheckSum = CheckSum(file_data[sent:sent + to_send]), Data = file_data[sent:sent + to_send]))
#         sent += to_send
#         to_send = min(mss - HEADER_LEN, len(file_data) - sent)
#         seq_num += 1

#     # Newly built list of pkts
#     return pkts

def SplitFile():
    try:
        file = open(abs_file_path, 'rb')
        Data = file.read()
        file.close()
        return Data
    # ChunkSize = 1024
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

def SocketAssign():
    global sd
    try:
        sd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sd.bind(("localhost",Port))
        # sd.setblocking(0)
    except:
        print("Socket Assignment Failed!")
        return

def RDT():
    SocketAssign()
    current = 0
    winSize = 4
    # Data = SplitFile()
    Data = ["Hello","Please","Send Me","the CN","Assignment"]
    SendData(filename.encode('utf-8'))
    # Data = list(map(bytes, DataSrc))
    for i in range(len(Data)):
        data = bytes(Data[i],'utf-8')
        chk = CheckSum(data)
        pkt = Packet(i,data,chk)
        bpkt = pickle.dumps(pkt)
        # msg = struct.pack((i,data,CheckSum(data)))
        while(True):
            try:
                SendData(bpkt)
                print("Sent#", i)
            except:
                print("Error Sending Data")
            ack = RecvData()
            Resp = pickle.loads(ack)
            print(Resp)
            if(Resp.Ack==i):
                break
    print("All Data Sent")
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
    (rmsg, peer) = sd.recvfrom(1024)
    return rmsg

def rdt_send(data,ack):
    chk = CheckSum(data)
    sndpkt = makepkt(ack,data,chk)
    udt_send(sndpkt)
    # start_timer()
def rdt_rcv(rcvpkt):
    return sd.recvfrom(1024)
def udt_send(pkt):
    sd.sendto(pkt, rcvAdd)

def chksum():
    return 0
def makepkt(ack,data,chksum):
    return (ack,data,chksum)

def isACK(rcvpkt,ack):
    return rcvpkt[0]==ack

RDT()


# def on_closing():
#     if messagebox.askokcancel("Quit", "Do you want to quit?"):
#         mainWindow.destroy()

# # GUI
# mainWindow = Tk()
# mainWindow.title('RDT3 - Sender')
# configFrame = Frame(mainWindow)
# configFrame.grid(row=0)
# SendButton = Button(configFrame, text='Send Data', width=25, command=RDT)
# SendButton.grid(row=0,column=0)
# mainWindow.protocol("WM_DELETE_WINDOW", on_closing)
# # mainWindow.mainloop()
