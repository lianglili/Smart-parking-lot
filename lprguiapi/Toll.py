from tkinter import *
import time
import lprguiapi.Setup as ls
import lprguiapi.zhuce as lz


class Toll(Frame):
	def __init__(self,master=None):
		super().__init__(master)
		self.master = master
		self.place(relx=0.84,rely=0,relwidth=0.16,relheight=0.8)
		self.createWidget()
		self.run()


	def createWidget(self):
		self.lbtitle = Label(self,text="智能停车场\n车牌识别收费系统",bg='green',fg='black',font=('微软雅黑',14))
		self.lbtitle.place(relx=0,rely=0,relwidth=1,relheight=0.1)

		self.btset = Button(self)
		self.btset["text"] = "设置费用标准"
		self.btset.place(relx=0.2,rely=0.2,relwidth=0.6,relheight=0.08)
		self.btset["command"] = self.set

		self.btzc = Button(self)
		self.btzc["text"] = "用户修改"
		self.btzc.place(relx=0.2,rely=0.3,relwidth=0.6,relheight=0.08)
		self.btzc["command"] = self.zhuce

		#self.lbEmployee_number = Label(self,text="当前员工编号",fg='black',font=('微软雅黑',14))
		#self.lbEmployee_number.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.08)
		#self.etEmployee_number = Label(self,fg='black',font=('微软雅黑',14))
		#self.etEmployee_number.place(relx=0.1,rely=0.48,relwidth=0.8,relheight=0.08)

		self.lbtime = Label(self,text="当前时间",fg='black',font=('微软雅黑',14))
		self.lbtime.place(relx=0.1,rely=0.6,relwidth=0.8,relheight=0.08)
		self.ettime = Label(self,fg='black',font=('微软雅黑',14))
		self.ettime.place(relx=0.1,rely=0.7,relwidth=0.8,relheight=0.08)    

		# self.lbtoll = Label(self,text="当前收费状态",fg='black',font=('微软雅黑',14))
		# self.lbtoll.place(relx=0.1,rely=0.8,relwidth=0.8,relheight=0.08)
		# self.ettoll = Label(self,fg='black',font=('微软雅黑',14))
		# self.ettoll.place(relx=0.1,rely=0.9,relwidth=0.8,relheight=0.08) 		

	def set(self):
		p = Tk()
		ls.Setup(p)
		p.mainloop()

	def zhuce(self):
		q = Tk()
		lz.Zhuce(q)
		q.mainloop
	#def setetEmployee_number(self,x):
		#self.etEmployee_number["text"]=x

	def run(self):
		self.t = time.strftime('%H:%M:%S')    #获取本地时间，变量名为t
		self.ettime.config(text=self.t)                   #标签label0的文本内容为t
		self.ettime.after(1000, self.run)                 #每隔1秒执行run()函数（每隔1秒，更新标签内容）循环