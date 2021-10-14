from tkinter import *
import tkinter.messagebox
import cv2 as cv
from PIL import Image
from PIL import ImageTk as itk
from tkinter import filedialog
import do as d
import datetime
import database.data as dd
import os
import time
import LPRspeech.LPRspeech as ll


class AutEnMonitor(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.a = d.Do()
        self.place(relx=0,rely=0,relwidth=1,relheight=0.48)
        self.createWidget()

    def createWidget(self):
        #入口标签
        self.En_label = Label(self,text="入口处监控显示",bg='black',fg='white',font=('微软雅黑',16))
        self.En_label.place(relx=0,rely=0,relwidth=0.5,relheight=0.08)
        #入口视频label
        self.En_panel = Label(self)
        self.En_panel['bg'] = 'black'
        self.En_panel.place(relx=0,rely=0.08,relwidth=0.5,relheight=0.84)
        self.En_panel.config(cursor="arrow")
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
        self.lbEntrance_number_plate = Label(self,text="入场车牌号",fg='black',font=('微软雅黑',16))
        self.lbEntrance_number_plate.place(relx=0.5,rely=0,relwidth=0.25,relheight=0.25)
        #
        self.etEntrance_number_plate = Label(self,fg='black',font=('微软雅黑',18))
        self.etEntrance_number_plate.place(relx=0.5,rely=0.25,relwidth=0.25,relheight=0.25)
        #
        self.lbEntrance_admission_time = Label(self,text="入场时间",fg='black',font=('微软雅黑',16))
        self.lbEntrance_admission_time.place(relx=0.75,rely=0,relwidth=0.25,relheight=0.25)
        #
        self.etEntrance_admission_time = Label(self,fg='black',font=('微软雅黑',18))
        self.etEntrance_admission_time.place(relx=0.75,rely=0.25,relwidth=0.25,relheight=0.25)
        #
        self.lbEntrance_vehicle_type = Label(self,text="车辆类型",fg='black',font=('微软雅黑',16))
        self.lbEntrance_vehicle_type.place(relx=0.5,rely=0.5,relwidth=0.25,relheight=0.25)
        #
        self.etEntrance_vehicle_type = Label(self,fg='black',font=('微软雅黑',18))
        self.etEntrance_vehicle_type.place(relx=0.5,rely=0.75,relwidth=0.25,relheight=0.25)
        #
        self.lbEntrance_user_type = Label(self,text="用户类型",fg='black',font=('微软雅黑',16))
        self.lbEntrance_user_type.place(relx=0.75,rely=0.5,relwidth=0.25,relheight=0.25)
        #
        self.etEntrance_user_type = Label(self,fg='black',font=('微软雅黑',18))
        self.etEntrance_user_type.place(relx=0.75,rely=0.75,relwidth=0.25,relheight=0.25)
        
            

    def open(self):
        self.btclose.config(state=NORMAL)
        self.btopen.config(state=DISABLED)
        self.cap = cv.VideoCapture(0)
        self.c = 1
        self.flo = 0
        self.show()

    def show(self):
        if self.flo ==1:
            time.sleep(4)
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
                    ll.ensay(self.numbername)
                    self.flo = 1
                    self.curr_time = datetime.datetime.now().replace(microsecond=0)
                    n = str(self.curr_time).find(".")
                    timechar = str(self.curr_time)[:n].split(" ")
                    db = dd.datab()
                    cursor=db.cursor()
                    sql='SELECT * FROM user_account where license=\'%s\''% self.numbername
                    try:
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        flag=0 
                        for row in results: 
                            flag=1
                            ptype ="注册用户"
                        if(flag==0):        
                            ptype ="非注册用户"
                        sql_insert='insert into record (license,begin_time)values(\'%s\',\'%s\')'% ( self.numbername,self.curr_time )
                        cursor.execute(sql_insert)
                        db.commit()
                        self.etEntrance_number_plate.configure(text=self.numbername)
                        self.etEntrance_admission_time.configure(text=timechar[1])
                        self.etEntrance_user_type.configure(text=ptype)
                    except Exception as e:
                        print(e)
                        tkinter.messagebox.showwarning('警告','出错')
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
            self.En_panel.imgtk = imgtk
            self.En_panel.config(image=imgtk)
            self.master.after(1,self.show)

    def close(self):
        self.cap.release()
        self.btopen.config(state=NORMAL)
        self.btclose.config(state=DISABLED)
        self.En_panel.bg = 'black'
        self.En_panel.config(bg='black')  


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
        self.En_panel.imgtk = imgtk
        self.En_panel.config(image=imgtk)
        
        self.numbername = self.a.do(img)
        if(self.numbername=='识别错误'):
            tkinter.messagebox.showwarning('警告','车牌识别出错，请转人工操作！')
        else:
            self.curr_time = datetime.datetime.now().replace(microsecond=0)
            n = str(self.curr_time).find(".")
            timechar = str(self.curr_time)[:n].split(" ")
            db = dd.datab()
            cursor=db.cursor()
            sql='SELECT * FROM user_account where license=\'%s\''% self.numbername
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                flag=0 
                for row in results: 
                    flag=1
                    ptype ="注册用户"
                if(flag==0):        
                    ptype ="非注册用户"
                sql_insert='insert into record (license,begin_time)values(\'%s\',\'%s\')'% ( self.numbername,self.curr_time )
                cursor.execute(sql_insert)
                db.commit()
                self.etEntrance_number_plate.configure(text=self.numbername)
                self.etEntrance_admission_time.configure(text=timechar[1])
                self.etEntrance_user_type.configure(text=ptype)
            except Exception as e:
                # print(e)
                tkinter.messagebox.showwarning('警告','出错')
            db.close()
            ll.ensay(self.numbername)
      




if __name__ == '__main__':
    root = Tk()
    root.title("智能车牌识别收费系统")
    # 获取当前屏幕的宽
    width = 1120
    # 获取当前屏幕的高
    height = 692
    root.geometry("{0}x{1}+-9+0".format(width,height))
    a = AutEnMonitor(root)
    root.mainloop()
    cv.destroyAllWindows()