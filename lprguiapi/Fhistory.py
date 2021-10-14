from tkinter import *
import database.data as dd
import datetime,time
from tkinter import messagebox
import tkinter.messagebox
from tkinter import ttk
import cv2 as cv
from PIL import Image
from PIL import ImageTk as itk
import time
import os


class Fhistory(Frame):
    """系统GUI自定义类"""
    def __init__(self,master=None):
        super().__init__(master)    # suoer是父类定义，而不是对象
        # 获取当前路径
        #self.LPR_path = os.getcwd().replace('\\','/')
        self.place(relx=0,rely=0.8,relwidth=1.0,relheight=0.2)
        self.createWidget()
        self.showHistroy()

    def createWidget(self):
        """创建组件"""

        #查看历史按钮
        self.btnhistory = Button(self,text="历史记录查询",fg='black',font=('微软雅黑',16))
        self.btnhistory.place(relx=0.86,rely=0.7,relwidth=0.14,relheight=0.3)
        self.btnhistory["command"] = self.history


        #历史记录列表
        self.lbhistory = ttk.Treeview(self)
        #定义列
        self.lbhistory["columns"] = ['1','2','3','4']
        #设置位置、大小
        self.lbhistory.place(relx=0,rely=0,relwidth=0.86,relheight=1.0)
        #设置列宽度
        self.lbhistory.column('1',width=35)
        self.lbhistory.column('2',width=40)
        self.lbhistory.column('3',width=40)
        self.lbhistory.column('4',width=35)
        #添加列名
        self.lbhistory.heading('1',text='车牌号')
        self.lbhistory.heading('2',text='入场时间')
        self.lbhistory.heading('3',text='出场时间')
        self.lbhistory.heading('4',text='停车金额')
        #添加数据
        #self.lbhistory.insert('',0,text='date1',values=('哈1','哈2','哈3'))
   
    def showHistroy(self):
        s=self.lbhistory.get_children()
        for item in s:
             self.lbhistory.delete(item)      
        db = dd.datab()
        cursor=db.cursor()
        sql='select * from record order by begin_time DESC limit 10 '
        try:
            cursor.execute(sql)
            results=cursor.fetchall()
            for row in results:               
                self.lbhistory.insert('','end',values=(row[0],row[1],row[2],row[3])) 
        except:
            tkinter.messagebox.showinfo('提示','数据库连接出错！')
        db.close()
        self.lbhistory.after(10000,self.showHistroy)

    def hrun(self,x,y): 
        s=lbhistory1.get_children()
        for item in s:
             lbhistory1.delete(item)        
        # db=pymysql.connect("127.0.0.1","niu","hanshu123??","carset",charset='utf8' 
        db = dd.datab()
        cursor=db.cursor()
        if(x!="" and y!=""):
            sql='select * from record where license=\'%s\'and (DATE_FORMAT(begin_time,\'%%Y\')=\'%s\'or DATE_FORMAT(begin_time,\'%%Y-%%m\')=\'%s\'or DATE_FORMAT(begin_time,\'%%Y-%%m-%%d\')=\'%s\')'%(x,y,y,y)
        if((x=="" and y!="") or (x!="" and y=="")):
            sql='select * from record where license=\'%s\'or DATE_FORMAT(begin_time,\'%%Y\')=\'%s\'or DATE_FORMAT(begin_time,\'%%Y-%%m\')=\'%s\'or DATE_FORMAT(begin_time,\'%%Y-%%m-%%d\')=\'%s\''%(x,y,y,y)
        if(x=="" and y==""):
            return 0
        try:
            cursor.execute(sql)
            results=cursor.fetchall()
            for row in results:
                lbhistory1.insert('',0,values=(row[0],row[1],row[2],row[3]))
        except:
            tkinter.messagebox.showinfo('提示','数据库连接出错！')
        db.close()
 
    def history(self):
        h_record=tkinter.Toplevel()
        h_record.title("历史查询")
        h_record.geometry('600x400')  
        lb1 = Label(h_record, text='车牌号')
        lb1.place(relx=0.1, rely=0.1, relwidth=0.1, relheight=0.1)
        inp1 = Entry(h_record)
        inp1.place(relx=0.2, rely=0.1, relwidth=0.2, relheight=0.1)
        lb2 = Label(h_record, text='日期')
        lb2.place(relx=0.5, rely=0.1, relwidth=0.1, relheight=0.1)
        inp2 = Entry(h_record)
        inp2.place(relx=0.6, rely=0.1, relwidth=0.2, relheight=0.1) 
        btn1 = Button(h_record, text='确认',command=lambda: self.hrun(inp1.get(),inp2.get()))
        btn1.place(relx=0.25, rely=0.3, relwidth=0.1, relheight=0.1)
        btn2 = Button(h_record, text='取消',command=h_record.destroy)
        btn2.place(relx=0.55, rely=0.3, relwidth=0.1, relheight=0.1)
        global lbhistory1
        lbhistory1 = ttk.Treeview(h_record,show="headings")
        lbhistory1["columns"] = ['0','1','2','3']
        lbhistory1.place(relx=0,rely=0.45,relwidth=1.0,relheight=0.55)
        lbhistory1.column('0',width=40)
        lbhistory1.column('1',width=60)
        lbhistory1.column('2',width=60)
        lbhistory1.column('3',width=40)
        lbhistory1.heading('0',text='车牌号')
        lbhistory1.heading('1',text='入场时间')
        lbhistory1.heading('2',text='出场时间')
        lbhistory1.heading('3',text='停车金额')