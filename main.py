from tkinter import *
from tkinter import messagebox
import tkinter.messagebox
from PIL import Image
from PIL import ImageTk as itk
import os
import lprguiapi.ArtEnMonitor as lrn
import lprguiapi.ArtExMonitor as lrx
import lprguiapi.AutEnMonitor as lun
import lprguiapi.AutExMonitor as lux
import lprguiapi.Fhistory as lf
import lprguiapi.Toll as lt
import database.data as dd


class basedesk():
	def __init__(self,master):
		self.root = master
		self.root.title("智能车牌识别收费系统")
	    # 获取当前屏幕的宽
		width = 1120
	    # 获取当前屏幕的高
		height = 692
		self.root.geometry("{0}x{1}+-9+0".format(width,height))
		lf.Fhistory(self.root)
		lt.Toll(self.root)
		AutStatus(self.root)  

class ArtStatus():
	def __init__(self,master=None):
		self.master = master
		self.ArtStatus = Frame(self.master,)
		self.ArtStatus.place(relx=0,rely=0,relwidth=0.7,relheight=0.8)
		self.aln = lrn.ArtEnMonitor(self.ArtStatus)
		self.alx = lrx.ArtExMonitor(self.ArtStatus)
		self.createWidget()

	def createWidget(self):
		self.lbstatus = Label(self.ArtStatus,text="当前为人工模式",fg='black',bg='red',font=('微软雅黑',16))
		self.lbstatus.place(relx=0,rely=0.96,relwidth=0.5,relheight=0.04)
		self.btchange = Button(self.ArtStatus)
		self.btchange["text"] = "切换为自动状态"
		self.btchange.place(relx=0.5,rely=0.96,relwidth=0.5,relheight=0.04)
		self.btchange["command"] = self.change

	def change(self):
 		self.ArtStatus.destroy()
 		AutStatus(self.master)


class AutStatus():
	def __init__(self,master=None):
		self.master = master
		self.AutStatus = Frame(self.master,)
		self.AutStatus.place(relx=0,rely=0,relwidth=0.7,relheight=0.8)
		self.aln = lun.AutEnMonitor(self.AutStatus)
		self.alx = lux.AutExMonitor(self.AutStatus)
		self.createWidget()

	def createWidget(self):
		self.lbstatus = Label(self.AutStatus,text="当前为自动模式",fg='black',bg='red',font=('微软雅黑',16))
		self.lbstatus.place(relx=0,rely=0.96,relwidth=0.5,relheight=0.04)
		self.btchange = Button(self.AutStatus)
		self.btchange["text"] = "切换为人工状态"
		self.btchange.place(relx=0.5,rely=0.96,relwidth=0.5,relheight=0.04)
		self.btchange["command"] = self.rd_Art		

	def change(self):
		self.rd_Art()
		self.AutStatus.destroy()
		#ArtStatus(self.master)

	def rd_Art(self):
		global denglu1
		denglu1= Tk()
		denglu1.title("智能车牌识别收费系统员工登录")
		denglu1.geometry('300x200')
		lb1 = Label(denglu1, text='账号')
		lb1.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.1)
		lb2 = Label(denglu1, text='密码')
		lb2.place(relx=0.1, rely=0.6, relwidth=0.2, relheight=0.1)
		inp1 = Entry(denglu1)
		inp1.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.1)
		inp2 = Entry(denglu1)
		inp2.place(relx=0.3, rely=0.6, relwidth=0.4, relheight=0.1)
		btn1 = Button(denglu1, text='确认',command=lambda: self.run1(inp1.get(), inp2.get()))		
		btn1.place(relx=0.25, rely=0.8, relwidth=0.2, relheight=0.1)
		btn2 = Button(denglu1, text='取消',command=denglu1.destroy)
		btn2.place(relx=0.55, rely=0.8, relwidth=0.2, relheight=0.1)
		denglu1.mainloop()
		return 1
	def run1(self,x,y):
		db = dd.datab()
		cursor=db.cursor()
		sql='SELECT * FROM administrator where id=\'%s\'and password=\'%s\''% (x,y)  
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			flag=1
			for row in results:
				if(str(row[0]) == x):  
					self.AutStatus.destroy()
					ArtStatus(self.master)					
					denglu1.destroy()                                               
					flag=0       
			if(flag==1):
				tkinter.messagebox.showinfo('提示','账号或密码错误！')          
		except:
			tkinter.messagebox.showinfo('提示','数据库写入出错！') 
		db.close()
		



if __name__ == '__main__':    
    root = Tk()
    basedesk(root)
    root.mainloop()