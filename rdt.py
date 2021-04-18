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
def RDT():
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