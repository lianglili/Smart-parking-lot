import database.data as dd
from tkinter import * 
from tkinter import ttk
import tkinter.messagebox
class Zhuce(Frame):
    def __init__(self,master):
        self.root = master
        self.root.title("用户修改")
        # 获取当前屏幕的宽
        width = 300
        # 获取当前屏幕的高
        height = 300
        self.root.geometry("{0}x{1}+200+80".format(width,height))
        self.rd()
        self.root.resizable(0,0) 
        self.db = dd.datab()
        self.cursor=self.db.cursor()
        #self.db.close()   
    def run1(self,y,z,w):
        sql='SELECT * FROM user_account where license=\'%s\''% z
        sql_insert='insert into user_account (name,license,balance)values(\'%s\',\'%s\',\'%s\')'% ( y, z, w)        
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            flag=0 
            for row in results:
                if(str(row[1]==z)):  
                    flag=1 
                    tkinter.messagebox.showinfo('提示','车牌号重复！')
            if(flag==0):
                try:            
                    self.cursor.execute(sql_insert)
                    self.db.commit()
                    tkinter.messagebox.showinfo('提示','注册成功！')
                except:
                    tkinter.messagebox.showinfo('提示','数据写入出错！')
        except:
            tkinter.messagebox.showinfo('提示','数据库连接出错！')
    def run2(self,z):
        sql='SELECT * FROM user_account where license=\'%s\''% z
        sql_del='delete from user_account where license=\'%s\''%z
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            flag=0 
            for row in results:
                if(str(row[1]==z)):  
                    flag=1
                    try: 
                        self.cursor.execute(sql_del)
                        self.db.commit()
                        tkinter.messagebox.showinfo('提示','删除成功！')
                    except:
                        tkinter.messagebox.showinfo('提示','数据删除出错！')
            if(flag==0):        
                    tkinter.messagebox.showinfo('提示','没有找到信息记录！')
        except:
            tkinter.messagebox.showinfo('提示','数据库连接出错！')
    def run3(self,x,y):
        if x!="" and y=="":
            sql='SELECT * FROM user_account where name=\'%s\''% x
        if x=="" and y!="":
            sql='SELECT * FROM user_account where license=\'%s\''% y
        if x!="" and y!="":
            sql='SELECT * FROM user_account where name=\'%s\'and license=\'%s\''% (x,y)  
        if x=="" and y=="":
            return 0
        s=self.lbhistory1.get_children()
        for item in s:
             self.lbhistory1.delete(item) 
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            print(results)
            flag=0 
            for row in results: 
                flag=1
                self.lbhistory1.insert('',0,values=(row[0],row[1],row[2]))
            if(flag==0):        
                tkinter.messagebox.showinfo('提示','没有找到用户记录！')
        except:
            tkinter.messagebox.showinfo('提示','数据库连接出错！')
    def rd(self):
        #self.lb1 = Label(self.root, text='id')
        #self.lb1.place(relx=0.05, rely=0.3, relwidth=0.2, relheight=0.1)
        self.lb2 = Label(self.root, text='姓名')
        self.lb2.place(relx=0.05, rely=0.1, relwidth=0.2, relheight=0.1)
        self.lb3=Label(self.root,text='车牌号')
        self.lb3.place(relx=0.05, rely=0.3, relwidth=0.2, relheight=0.1)
        self.lb4=Label(self.root,text='余额')
        self.lb4.place(relx=0.05, rely=0.5, relwidth=0.2, relheight=0.1)
        #self.inp1 = Entry(self.root)
        #self.inp1.place(relx=0.25, rely=0.3, relwidth=0.35, relheight=0.1)
        self.inp2 = Entry(self.root)
        self.inp2.place(relx=0.25, rely=0.1, relwidth=0.35, relheight=0.1)
        self.inp3 = Entry(self.root)
        self.inp3.place(relx=0.25, rely=0.3, relwidth=0.35, relheight=0.1)
        self.inp4 = Entry(self.root)
        self.inp4.place(relx=0.25, rely=0.5, relwidth=0.35, relheight=0.1)
        self.btn1 = Button(self.root, text='注册',command=lambda: self.run1(self.inp2.get(),self.inp3.get(),self.inp4.get()))
        self.btn1.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.1)
        self.btn2 = Button(self.root, text='删除',command=lambda: self.run2(self.inp3.get()))
        self.btn2.place(relx=0.7, rely=0.3, relwidth=0.2, relheight=0.1)
        self.btn3 = Button(self.root, text='查询',command=lambda: self.run3(self.inp2.get(),self.inp3.get()))
        self.btn3.place(relx=0.7, rely=0.5, relwidth=0.2, relheight=0.1)
        self.lbhistory1 = ttk.Treeview(self.root,show="headings")
        self.lbhistory1["columns"] = ['0','1','2']
        self.lbhistory1.place(relx=0,rely=0.65,relwidth=1.0,relheight=0.35)
        self.lbhistory1.column('0',width=30)
        self.lbhistory1.column('1',width=60)
        self.lbhistory1.column('2',width=30)
        self.lbhistory1.heading('0',text='姓名')
        self.lbhistory1.heading('1',text='车牌号')
        self.lbhistory1.heading('2',text='余额')
          