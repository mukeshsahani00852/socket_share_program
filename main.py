#for program that share file between two computers connected through lan netword

from  tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import win32com.client
from socket import *
from tkinter import ttk
from time import *

global senderipaddress
global recevieripaddress

sp = win32com.client.Dispatch('SAPI.spvoice')

class recvroot:
	def __init__(self, root):
		self.statusbarrecv = Label(root, relief = SUNKEN, anchor = W, text = "Recvive file")
		self.statusbarrecv.pack(side = BOTTOM,fill = X)
		self.l_font = ('Times', -30, 'bold')
		self.lip = Label(root, text = "server Ip address : ", font = self.l_font, fg = 'blue')
		self.lip.place(x = 100, y = 30)
		self.e_self = ('Times', -30, 'bold underline')
		self.sp = win32com.client.Dispatch('SAPI.spvoice')
		self.ipadd = Entry(root, bg = 'white', fg = 'blue', font = self.e_self)
		self.ipadd.place(x = 100, y = 100)

		self.setdata = Button(root, bg = 'white', fg = 'blue', text = "Set ip address", font = self.l_font, command = self.setsip)
		self.setdata.place(x = 100, y = 150)
		self.server = socket()
		self.host = ' '
		self.port = 9000
		self.rlst = []
		self.i = 0
		self.fname = "demo.txt"
		self.senderbutton = Button(root, bg = 'white', fg = 'blue', text = "    Ok   ", font = self.l_font, command = self.startr)
		self.fileentry  = Entry(root, bg = 'white', fg = 'blue', font = self.l_font)
		self.numlabel = Label(root, bg = 'white', fg = 'blue', text = 'Name of file', font = self.l_font)
		self.namefile = Text(root, bg = 'white', fg = 'blue', font = self.l_font, height = 1, width = 20)
		self.addfilebutton = Button(root, bg = 'white', fg = 'blue', font = self.l_font, text = "ADD", command = self.addfile)
		self.okfile = Button(root, bg  = 'white', fg = 'blue', font = self.l_font, text = "Done", command = self.donefunc)
		self.lbox = Listbox(root, bg = 'white', fg = 'blue', activestyle = 'underline', selectmode = SINGLE, font = self.l_font)
		self.dummy = " "
		self.senderipaddress = " "
	def setsip(self):
		ipa = self.ipadd.get()
		self.senderipaddress = ipa
		self.statusbarrecv['text'] = "ip adress sender : " + self.senderipaddress
		#self.sp.speak("the ipaddress of server "  +   self.senderipaddress +  " for confirmation please check the statusbar")
		#self.host = senderipaddress
		self.senderbutton.place(x = 100, y = 250)


	def addfile(self):
		self.dummy = self.namefile.get(0.0, END)
		print(self.dummy.strip())
		self.dummy = self.dummy.strip()
		if self.dummy != "":
			self.rlst.append(self.dummy)
			self.lbox.insert(END, self.dummy)
			self.i += 1
		print(self.rlst)
		self.namefile.delete(1.0, END)

	def startr(self):
		#self.server = socket.connect((self.host, self.port))
		
		self.lbox.place(x = 800, y =50)
		self.numlabel.place(x = 100, y = 450)
		self.namefile.place(x = 300, y = 450)
		self.addfilebutton.place(x = 300, y = 500)
		self.okfile.place(x = 450, y = 500)

	def donefunc(self):
		self.server.connect((self.senderipaddress, self.port))
	
		data1 = str(self.i)
		self.server.send(data1.encode())
		i = 0
		sleep(0.025)
		for val in self.rlst:
			
			if val[len(val)-3:] == 'txt':
				self.server.send(val.encode())
				
				data2 = self.server.recv(1024*10000)

				data2 = data2.decode()
				data2 = str(data2)
				val = val[0 : len(val) - 4] + "sended"
				with open(val,"w") as f:
					f.write(data2)
				
				self.statusbarrecv['text'] += f" {self.rlst[i]} file is recived,"
				i+=1
			else:
	
				fnamer = self.rlst[i]
				self.server.send(fnamer.encode())
		
				datag = self.server.recv(1024*10000)
				val = fnamer[0 : len(fnamer) - 4] + "sender" + fnamer[len(fnamer) - 4 : ]
				with open(val, "wb") as f:
					f.write(datag)
				self.statusbarrecv['text'] += f" {self.rlst[i]} file is recived,"
				i+=1
		#messagebox.showinfo("info","data is transfered")
		self.server.close()
def recv_file():
	statusbar['fg'] = 'green'
	statusbar['text'] = 'Reciver program is initiated'
	root = Tk()
	root.title("Reciver")
	root.geometry("1360x768")
	root.wm_iconbitmap('book.ico')
	menubar = Menu(root)
	root.config(menu = menubar)

	exit = Menu(root, tearoff = 0)
	exit.add_command(label  = "Exit", command = root.destroy)

	menubar.add_cascade(menu = exit, label = "Exit")

	sendobj = recvroot(root)
	root.mainloop()


class sendroot:
	def __init__(self, root):
		self.statusbarsend = ttk.Label(root, relief = SUNKEN, anchor = W, text = "Send file")
		self.statusbarsend.pack(side = BOTTOM,fill = X)
		self.l_font = ('Times', -30, 'bold')
		self.lip = Label(root, text = "server Ip address : ", font = self.l_font, fg = 'blue')
		self.lip.place(x = 100, y = 30)
		self.e_self = ('Times', -30, 'bold underline')
		self.sp = win32com.client.Dispatch('SAPI.spvoice')
		self.ipadd = Entry(root, bg = 'white', fg = 'blue', font = self.e_self)
		self.ipadd.place(x = 100, y = 100)

		self.setdata = Button(root, bg = 'white', fg = 'blue', text = "Set ip address", font = self.l_font, command = self.setsip)
		self.setdata.place(x = 100, y = 150)
		self.socket = socket()
		self.host = ' '
		self.port = 9000
		self.rlst = []
		self.fname = "demo.txt"
		self.c = " "
		self.addr = " "
		self.sendbutton = Button(root, bg = 'white', fg = 'blue', text = "Start", font = self.l_font, command = self.startc)
		self.senderipaddress = " "


	def setsip(self):
		ipa = self.ipadd.get()
		self.senderipaddress = ipa
		self.statusbarsend['text'] = "ip adress sender : " + self.senderipaddress
		#self.sp.speak("sender ip address" + self.senderipaddress +"for confirmation please check the statusbar")
		print(self.senderipaddress)
		self.sendbutton.place(x = 100, y = 300)




	def startc(self):
		self.host = self.senderipaddress
		self.port = 9000
		self.socket.bind((self.host, self.port))
		self.socket.listen(5)
		self.c,self.addr = self.socket.accept()
		data1 = self.c.recv(1024)
		data1 = data1.decode()
		data2 = data1
		data2 = int(data2)
		print(data2)
		i = 0
		while i < data2 :
			fname = self.c.recv(1024)
			fname = fname.decode()
			fname = str(fname)
			if fname[len(fname) - 3 : ] == 'txt':
				with open(fname,"r") as f:
					datag = f.read()
				self.c.send(datag.encode())
				self.statusbarsend['text'] += f' {fname}   is sended, '
			else:
				with open(fname,"rb") as f:
					datag = f.read()
				self.c.send(datag)
				self.statusbarsend['text'] += f' {fname}   is sended, '
			i+=1
		self.socket.close()
		self.c.close()
				
def send_file():
	statusbar['fg'] = 'green'
	statusbar['text'] = 'Sender program is initiated'
	root = Tk()
	root.title("sender")
	root.geometry("1360x768")
	root.wm_iconbitmap('book.ico')
	
	menubar = Menu(root)
	root.config(menu = menubar)

	exit = 	Menu(root, tearoff = 0)
	exit.add_command(label = "Exit", command = root.destroy)

	menubar.add_cascade(label = "Exit", menu = exit)


	sendobj = sendroot(root)
	root.mainloop()



mainroot = Tk()
mainroot.title("Share_er")
mainroot.geometry("1360x700")
mainroot.wm_iconbitmap('book.ico')


menubar = Menu(mainroot)
mainroot.config(menu = menubar)
filemenu = Menu(mainroot, tearoff = 0)

filemenu.add_command(label = "Help")
filemenu.add_command(label = "Open web page")
exit = Menu(mainroot, tearoff = 0)
exit.add_command(label = "exit".title(), command = mainroot.destroy)
menubar.add_cascade(menu = filemenu, label = "Help")
menubar.add_cascade(menu =exit, label = "Exit")

statusbar = Label(mainroot, anchor = W, relief = SUNKEN, bg = 'white', text = "Share file")
statusbar.pack(side = BOTTOM, fill = X)
'''
leftframe = Frame(mainroot, bg = 'blue')
leftframe.propagate(0)
leftframe.pack()
'''

self_font = ('Times', -40, 'bold italic')

lbl = Label(mainroot, font = self_font, text = "Share_er", fg = 'blue')
lbl.place(x = 610, y = 10)

brecv = Button(mainroot, font = self_font, text = "         Recive          ", fg = 'blue', command = recv_file)
brecv.place(x = 580, y = 200)

bsend = Button(mainroot, font = self_font, text = "         Send            ", fg = 'blue', command = send_file)
bsend.place(x = 580, y = 400)


'''
rightframe = Frame(mainroot, bg = 'blue')
rightframe.propagate(0)
rightframe.pack(side = RIGHT)
'''
mainroot.mainloop()