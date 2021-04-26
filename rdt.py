import socket
from tkinter import *
from tkinter import messagebox
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
from collections import namedtuple
MyStruct = namedtuple("Packet", "SeqN AckN Data")

BUFSIZ = 1024
# rdt vars
lossRate = 0
timeout = 0
Port = 8008
rcvPort = 8009
rcvIP = "127.0.0.1"
rcvAdd = (rcvIP,rcvPort)

def SocketAssign():
    try:
        sd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    except:
        return
def RDT():
    current = 0
    winSize = 4
    return
def SendData():
    return


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        mainWindow.destroy()

# GUI
mainWindow = Tk()
mainWindow.title('RDT3 - Sender')
configFrame = Frame(mainWindow)
configFrame.grid(row=0)
SendButton = Button(configFrame, text='Send Data', width=25, command=SendData)
SendButton.grid(row=0,column=0)
mainWindow.protocol("WM_DELETE_WINDOW", on_closing)
mainWindow.mainloop()