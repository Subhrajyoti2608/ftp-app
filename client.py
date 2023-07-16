#-----------Bolierplate Code Start -----
import socket
from threading import Thread
from tkinter import *
from tkinter import ttk


PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096


name = None
listbox =  None
textarea= None
labelchat = None
text_message = None
filePathLabel = None
sending_file=None

def connectWithClient():
    global SERVER
    global listbox

    text = listbox.get(ANCHOR)
    list_item = text.split(":")
    message = "Connect " + list_item[1]
    SERVER.send(message.encode("ascii"))

def disconnectWithClient():
    global SERVER
    global listbox 

    text=listbox.get(ANCHOR)
    list_item=text.split(":")
    message="Disconnect " + list_item[1]
    SERVER.send(message.encode("ascii"))



def recvMessage():
     global SERVER
     global BUFFER_SIZE

     while True:
        chunk = SERVER.recv(BUFFER_SIZE)
        try:
            if("tiul" in chunk.decode() and "1.0," not in chunk.decode()):
                letter_list = chunk.decode().split(",")
                listbox.insert(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
                print(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
            else:
                textarea.insert(END,"\n"+chunk.decode('ascii'))
                textarea.see("end")
                print(chunk.decode('ascii'))
        except:
            pass



     

def showClients():
    global listbox
    global SERVER
    
    listbox.delete(0, "end")
    SERVER.send("show list".encode('ascii'))

def connectToServer():
    global SERVER
    global name
    global sending_file

    cName = name.get()
    SERVER.send(cName.encode())

    

def openChatWindow():

   
    print("\n\t\t\t\tIP MESSENGER")

    #Client GUI starts here
    window=Tk()

    window.title('Messenger')
    window.geometry("500x350")

    global name
    global listbox
    global textarea
    global labelchat
    global text_message
    global filePathLabel

    namelabel = Label(window, text= "Enter Your Name", font = ("Calibri",10))
    namelabel.place(x=10, y=8)


    name = Entry(window,width =30,font = ("Calibri",10))
    name.place(x=120,y=8)
    name.focus()

    connectserver = Button(window,text="Connect to Chat Server",bd=1, font = ("Calibri",10), command=connectToServer)
    connectserver.place(x=350,y=6)

    separator = ttk.Separator(window, orient='horizontal')
    separator.place(x=0, y=35, relwidth=1, height=0.1)

    labelusers = Label(window, text= "Active Users", font = ("Calibri",10))
    labelusers.place(x=10, y=50)

    listbox = Listbox(window,height = 5,width = 67,activestyle = 'dotbox', font = ("Calibri",10))
    listbox.place(x=10, y=70)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)

    connectButton=Button(window,text="Connect",bd=1, font = ("Calibri",10), command=connectWithClient)
    connectButton.place(x=282,y=160)

    disconnectButton=Button(window,text="Disconnect",bd=1, font = ("Calibri",10), command=disconnectWithClient)
    disconnectButton.place(x=350,y=160)

    refresh=Button(window,text="Refresh",bd=1, font = ("Calibri",10), command=showClients)
    refresh.place(x=435,y=160)

    labelchat = Label(window, text= "Chat Window", font = ("Calibri",10))
    labelchat.place(x=10, y=180)

    textArea = Text(window, width=67, height=6, font = ("Calibri",10))
    textArea.place(x=10, y=200)

    scrollbar2 = Scrollbar(textArea)
    scrollbar2.place(relheight = 1,relx = 1)
    scrollbar2.config(command = listbox.yview)

    attachButton = Button(window, text="Attact and send", bd=1, font=("Calibri",10))
    attachButton.place(x=10, y=305)

    textmessage = Entry(window,width =30,font = ("Calibri",10))
    textmessage.pack()
    textmessage.place(x=98,y=306)
    

    sendButton = Button(window, text="Send", bd=1, font=("Calibri",10))
    sendButton.place(x=450, y=305)

    filepathlabel = Label(window, text= "", fg="blue", font = ("Calibri",10))
    filepathlabel.place(x=10, y=330)
  
  
  
  
  
    window.mainloop()




def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    rcvthread = Thread(target = recvMessage)
    rcvthread.start()
    openChatWindow()

setup()
