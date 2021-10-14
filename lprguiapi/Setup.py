from tkinter import *
import tkinter.ttk
import tkinter.messagebox
import os
import numpy as np


class Setup():
	def __init__(self,master):
		self.root = master
		self.root.title("收费设置")
		self.root.wm_attributes('-topmost',1)
		width = 240
		height = 200
		self.result = np.zeros(3)
		self.root.geometry("{0}x{1}+200+80".format(width,height))
		self.root.resizable(0,0) 
		self.feestand = 0
		self.freetime = 0
		self.feevip = 0
		self.create()
	
	def create(self):
		#临时用户
		self.lbprice = Label(self.root,text="收费标准（单价）",fg='black',bg='white',font=('微软雅黑',10))
		self.lbprice.place(x=30,y=20,width=200,height=20)
		self.varsatnd = tkinter.StringVar()
		self.enprice = tkinter.ttk.Combobox(self.root, textvariable=self.varsatnd)
		self.enprice['value'] = (0.5,0.8,1,1.5)
		self.enprice.set(0)
		self.enprice.bind("<<ComboboxSelected>>",self.go)
		self.enprice.place(x=30,y=40,width=120,height=20)
		self.lbunit = Label(self.root,text="元/小时",fg='black',bg='white',font=('微软雅黑',10))
		self.lbunit.place(x=150,y=40,width=80,height=20)
		#
		self.lbbasic = Label(self.root,text="免收费时长",fg='black',bg='white',font=('微软雅黑',10))
		self.lbbasic.place(x=30,y=60,width=200,height=20)
		self.var = tkinter.StringVar()
		self.combasic = tkinter.ttk.Combobox(self.root, textvariable=self.var)
		self.combasic['value'] = (0.5,1,1.5,2,0)
		self.combasic.set(0)
		self.combasic.bind("<<ComboboxSelected>>",self.gofreetime)
		self.combasic.place(x=30, y=80,width=120,height=20)
		self.lbunit = Label(self.root,text="小时",fg='black',bg='white',font=('微软雅黑',10))
		self.lbunit.place(x=150,y=80,width=80,height=20)
		#会员
		self.lbvip = Label(self.root,text="会员收费标准",fg='black',bg='white',font=('微软雅黑',10))
		self.lbvip.place(x=30,y=100,width=200,height=20)
		self.varvip = tkinter.StringVar()
		self.comvip = tkinter.ttk.Combobox(self.root, textvariable=self.varvip)
		self.comvip['value'] = (0)
		self.comvip.set(0)
		self.comvip.bind("<<ComboboxSelected>>",self.govip)
		self.comvip.place(x=30, y=120,width=120,height=20)
		self.lbvip = Label(self.root,text="元/小时",fg='black',bg='white',font=('微软雅黑',10))
		self.lbvip.place(x=150,y=120,width=80,height=20)
		#确定
		self.btsure = Button(self.root)
		self.btsure["text"] = "确认"
		self.btsure.place(x=80,y=160,width=80,height=30)
		self.btsure["command"] = self.sure


	def go(self,*a):
		self.feestand = float(self.enprice.get())
		self.result[1] = self.feestand
		self.comvip.set(0)
		self.result[2] = 0
		valuevip = [round(self.feestand*0.9,1),round(self.feestand*0.8,1),round(self.feestand*0.7,1),round(self.feestand*0.6,1),round(self.feestand*0.5,1),round(self.feestand*0.4,1),round(self.feestand*0.3,1)]
		self.comvip['value'] = valuevip
		

	def govip(self,*a):
		if self.feestand == 0:
			tkinter.messagebox.showwarning('警告','请先设置收费标准')
		else:
			self.feevip = float(self.comvip.get())
			self.result[2] = self.feevip

	def gofreetime(self,*a):
		self.freetime = float(self.combasic.get())
		self.result[0] = self.freetime

	def sure(self):
		if self.feestand ==0 or self.feevip == 0:
			tkinter.messagebox.showinfo('提示','设置失败')
		else:
			cur_dir = str(os.getcwd()).replace("\\","/")
			path = os.path.join(cur_dir,'Txtnetdata/pay.txt')
			np.savetxt(path,self.result)
			tkinter.messagebox.showinfo('提示','设置完成')
		self.root.destroy()


if __name__ == '__main__':
	a = Tk()
	p = Setup(a)
	a.mainloop()