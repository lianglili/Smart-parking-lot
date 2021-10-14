from tkinter import *
from tkinter import messagebox
import cv2 as cv
import tkinter
from PIL import Image
from PIL import ImageTk as itk
from tkinter import filedialog
import do as d
import LPRspeech.LPRspeech as ll
import database.data as dd
import pay.pay as pp
import os
import datetime
import time


class AutExMonitor(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.a = d.Do()
        self.place(relx=0,rely=0.48,relwidth=1,relheight=0.48)
        self.createWidget()

    def createWidget(self):
        #入口标签
        self.Ex_label = Label(self,text="出口处监控显示",bg='black',fg='white',font=('微软雅黑',16))
        self.Ex_label.place(relx=0,rely=0,relwidth=0.5,relheight=0.08)
        #入口视频label
        self.Ex_panel = Label(self)
        self.Ex_panel['bg'] = 'black'
        self.Ex_panel.place(relx=0,rely=0.08,relwidth=0.5,relheight=0.84)
        self.Ex_panel.config(cursor="arrow")
        #开启按钮
        self.btopen = Button(self)
        self.btopen["text"] = "开启"
        self.btopen.place(relx=0,rely=0.92,relwidth=0.15,relheight=0.08)
        self.btopen["command"] = self.open
        #关闭按钮
        self.btclose = Button(self)
        self.btclose["text"] = "关闭"
        self.btclose.place(relx=0.15,rely=0.92,relwidth=0.15,relheight=0.08)
        self.btclose["command"] = self.close
        self.btclose.config(state=DISABLED)
        #文件按钮
        self.btfile = Button(self)
        self.btfile["text"] = "打开文件"
        self.btfile.place(relx=0.3,rely=0.92,relwidth=0.2,relheight=0.08)
        self.btfile["command"] = self.opfile
        #状态部分
        self.lbExit_number_plate = Label(self,text="出场车牌号",fg='black',font=('微软雅黑',16))
        self.lbExit_number_plate.place(relx=0.5,rely=0,relwidth=0.25,relheight=0.25)
        #
        self.etExit_number_plate = Label(self,fg='black',font=('微软雅黑',18))
        self.etExit_number_plate.place(relx=0.5,rely=0.25,relwidth=0.25,relheight=0.25)
        #
        self.lbExit_admission_time = Label(self,text="出场时间",fg='black',font=('微软雅黑',16))
        self.lbExit_admission_time.place(relx=0.75,rely=0,relwidth=0.25,relheight=0.25)
        #
        self.etExit_admission_time = Label(self,fg='black',font=('微软雅黑',18))
        self.etExit_admission_time.place(relx=0.75,rely=0.25,relwidth=0.25,relheight=0.25)
        #
        self.lbExit_time_consuming = Label(self,text="停车耗时",fg='black',font=('微软雅黑',16))
        self.lbExit_time_consuming.place(relx=0.5,rely=0.5,relwidth=0.25,relheight=0.25)
        #
        self.etExit_time_consuming = Label(self,fg='black',font=('微软雅黑',18))
        self.etExit_time_consuming.place(relx=0.5,rely=0.75,relwidth=0.25,relheight=0.25)
        #
        self.lbExit_Payable = Label(self,text="应收金额",fg='black',font=('微软雅黑',16))
        self.lbExit_Payable.place(relx=0.75,rely=0.5,relwidth=0.25,relheight=0.25)
        #
        self.etExit_Payable = Label(self,fg='black',font=('微软雅黑',18))
        self.etExit_Payable.place(relx=0.75,rely=0.75,relwidth=0.25,relheight=0.25)

    def open(self):
        self.btclose.config(state=NORMAL)
        self.btopen.config(state=DISABLED)
        self.cap = cv.VideoCapture(0)
        self.c = 1
        self.flo = 0
        self.show()

    def show(self):
        if self.flo ==1:
            time.sleep(8)
            self.flo =0
        frameRate = 10
        self.success,self.img = self.cap.read()
        if self.success:
            if (self.c % frameRate == 0):
                self.curr_path = os.getcwd().replace("\\","/")
                self.curr_time = str(datetime.datetime.now()).replace(" ","")
                self.curr_time = self.curr_time.replace(".","")
                self.curr_time = self.curr_time.replace(":","")
                path = '{0}/result/platenumber/{1}.jpg'.format(self.curr_path,self.curr_time)
                cv.imwrite(path,self.img)
                try:
                    self.numbername = self.a.doapi(path)
                    self.flo = 1
                    self.etExit_number_plate['text'] = self.numbername
                    self.curr_time = datetime.datetime.now().replace(microsecond=0)
                    n = str(self.curr_time).find(".")
                    timechar = str(self.curr_time)[:n].split(" ")
                    self.etExit_admission_time['text'] = timechar[1]
                    db = dd.datab()
                    cursor=db.cursor()
                    sql='SELECT * FROM record where license=\'%s\' '% self.numbername
                    try:
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        parktime=0
                        for row in results: 
                            if(row[2]==None):
                                self.etExit_time_consuming['text'] =str(self.curr_time-row[1])
                                parktime=(self.curr_time-row[1])
                        flag=0 
                        ap = False
                        for row in results: 
                            flag=1
                            ap = True
                        if(flag==0):        
                            ap = False
                        parktime=float(parktime.total_seconds()/3600.0)
                        self.fee = pp.pay(ap,parktime)
                        self.fee = round(self.fee, 2)
                        self.etExit_Payable['text'] = self.fee 
                        sql_update='UPDATE record SET end_time=\'%s\' ,parking_rate= \'%.2f\'WHERE license=\'%s\' and end_time is null'%(self.curr_time,self.fee,self.numbername)
                        cursor.execute(sql_update)
                        db.commit()
                        sql_user='SELECT * FROM user_account where license=\'%s\' '% self.numbername
                        cursor.execute(sql_user)
                        results = cursor.fetchall()
                        flag2=0
                        for row2 in results: 
                            flag2=1
                            if(row2[2] > self.fee):
                                sql_update2='UPDATE user_account SET balance=\'%.2f\'WHERE license=\'%s\' '%(row2[2]-self.fee,self.numbername)
                                cursor.execute(sql_update2)
                                db.commit()
                            else:
                                tkinter.messagebox.showinfo('提示','余额不足，更换人工收费，稍后请充值！')
                                ll.paymentreminder()
                        if(flag2==0):
                               tkinter.messagebox.showinfo('提示','非会员用户，请人工收费！') 
                    except Exception as e:
                        print(e)
                    ll.exsay(self.numbername,parktime,self.fee)
                    db.close()
                except Exception as e:
                    self.flo = 0
                    print(e)
            self.c+=1
            if self.c > 10000:
                self.c =1
            cvimage = cv.cvtColor(self.img,cv.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cvimage)
            imgtk = itk.PhotoImage(image=current_image)
            self.Ex_panel.imgtk = imgtk
            self.Ex_panel.config(image=imgtk)
            self.master.after(1,self.show)

    def close(self):
        self.cap.release()
        self.btopen.config(state=NORMAL)
        self.btclose.config(state=DISABLED)
        self.Ex_panel.bg = 'black'
        self.Ex_panel.config(bg='black')        


    def opfile(self):
        '''打开文件的逻辑'''
        self.master.update()
        x = int(self.master.winfo_width()*0.7*0.5)
        y = int(self.master.winfo_height()*0.8*0.48*0.84)
        self.dirname = filedialog.askopenfilename() # 打开文件对话框
        if not self.dirname:
            messagebox.showwarning('警告', message='未选择文件夹！')  # 弹出消息提示框
        img = cv.imread(self.dirname)
        image = cv.resize(img,(x,y))
        cvimage = cv.cvtColor(image,cv.COLOR_BGR2RGBA)
        current_image = Image.fromarray(cvimage)
        imgtk = itk.PhotoImage(image=current_image)
        self.Ex_panel.imgtk = imgtk
        self.Ex_panel.config(image=imgtk)
        self.numbername = self.a.do(img)
        self.etExit_number_plate['text'] = self.numbername
        self.curr_time = datetime.datetime.now().replace(microsecond=0)
        n = str(self.curr_time).find(".")
        timechar = str(self.curr_time)[:n].split(" ")
        self.etExit_admission_time['text'] = timechar[1]
        db = dd.datab()
        cursor=db.cursor()
        sql='SELECT * FROM record where license=\'%s\' '% self.numbername
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            parktime=0
            for row in results: 
                if(row[2]==None):
                    self.etExit_time_consuming['text'] =str(self.curr_time-row[1])
                    parktime=(self.curr_time-row[1])
            flag=0 
            ap = False
            for row in results: 
                flag=1
                ap = True
            if(flag==0):        
                ap = False
            parktime=float(parktime.total_seconds()/3600.0)
            self.fee = pp.pay(ap,parktime)
            self.fee = round(self.fee, 2)
            self.etExit_Payable['text'] = self.fee 
            sql_update='UPDATE record SET end_time=\'%s\' ,parking_rate= \'%.2f\'WHERE license=\'%s\' and end_time is null'%(self.curr_time,self.fee,self.numbername)
            cursor.execute(sql_update)
            db.commit()
            sql_user='SELECT * FROM user_account where license=\'%s\' '% self.numbername
            cursor.execute(sql_user)
            results = cursor.fetchall()
            flag2=0
            for row2 in results: 
                flag2=1
                if(row2[2] > self.fee):
                    sql_update2='UPDATE user_account SET balance=\'%.2f\'WHERE license=\'%s\' '%(row2[2]-self.fee,self.numbername)
                    cursor.execute(sql_update2)
                    db.commit()
                else:
                    tkinter.messagebox.showinfo('提示','余额不足，更换人工收费，稍后请充值！')
                    ll.paymentreminder()
            if(flag2==0):
                   tkinter.messagebox.showinfo('提示','非会员用户，请人工收费！') 
        except Exception as e:
            # print(e)
            pass
        ll.exsay(self.numbername,parktime,self.fee)
        db.close()

if __name__ == '__main__':
    root = Tk()
    root.title("智能车牌识别收费系统")
    # 获取当前屏幕的宽
    width = 1120
    # 获取当前屏幕的高
    height = 692
    root.geometry("{0}x{1}+-9+0".format(width,height))
    a = AutExMonitor(root)
    root.mainloop()
    cv.destroyAllWindows()


