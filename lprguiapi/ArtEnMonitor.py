from tkinter import *
from tkinter import messagebox
import cv2 as cv
from PIL import Image
from PIL import ImageTk as itk
from tkinter import filedialog
import do as d
import LPRspeech.LPRspeech as ll
import datetime
import database.data as dd


class ArtEnMonitor(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.place(relx=0,rely=0,relwidth=1,relheight=0.48)
        self.createWidget()
        

    def createWidget(self):
        #入口标签
        self.En_label = Label(self,text="入口处监控显示",bg='black',fg='white',font=('微软雅黑',16))
        self.En_label.place(relx=0,rely=0,relwidth=0.5,relheight=0.08)
        #入口视频label
        self.En_panel = Label(self)
        self.lbbg()
        #self.En_panel['bg'] = 'black'
        self.En_panel.place(relx=0,rely=0.08,relwidth=0.5,relheight=0.84)
        self.En_panel.config(cursor="arrow")
        #开启按钮
        self.btopen = Button(self)
        self.btopen["text"] = "开启"
        self.btopen.place(relx=0,rely=0.92,relwidth=0.25,relheight=0.08)
        self.btopen["command"] = self.open
        #关闭按钮
        self.btclose = Button(self)
        self.btclose["text"] = "关闭"
        self.btclose.place(relx=0.25,rely=0.92,relwidth=0.25,relheight=0.08)
        self.btclose["command"] = self.close
        self.btclose.config(state=DISABLED)
        # #文件按钮
        # self.btfile = Button(self)
        # self.btfile["text"] = "打开文件"
        # self.btfile.place(relx=0.3,rely=0.92,relwidth=0.2,relheight=0.08)
        # self.btfile["command"] = self.opfile
        #状态部分
        self.lbEntrance_number_plate = Label(self,text="入场车牌号",fg='black',font=('微软雅黑',16))
        self.lbEntrance_number_plate.place(relx=0.5,rely=0,relwidth=0.25,relheight=0.2)
        #
        self.etEntrance_number_plate = Entry(self,fg='black',font=('微软雅黑',18),state='normal')
        self.etEntrance_number_plate.place(relx=0.5,rely=0.2,relwidth=0.25,relheight=0.2)
        #
        self.lbEntrance_admission_time = Label(self,text="入场时间",fg='black',font=('微软雅黑',16))
        self.lbEntrance_admission_time.place(relx=0.75,rely=0,relwidth=0.25,relheight=0.2)
        #
        self.etEntrance_admission_time = Label(self,fg='black',font=('微软雅黑',18),state='disabled')
        self.etEntrance_admission_time.place(relx=0.75,rely=0.2,relwidth=0.25,relheight=0.2)
        #
        self.lbEntrance_vehicle_type = Label(self,text="车辆类型",fg='black',font=('微软雅黑',16))
        self.lbEntrance_vehicle_type.place(relx=0.5,rely=0.4,relwidth=0.25,relheight=0.2)
        #
        self.etEntrance_vehicle_type = Label(self,fg='black',font=('微软雅黑',18),state='disabled')
        self.etEntrance_vehicle_type.place(relx=0.5,rely=0.6,relwidth=0.25,relheight=0.2)
        #
        self.lbEntrance_user_type = Label(self,text="用户类型",fg='black',font=('微软雅黑',16))
        self.lbEntrance_user_type.place(relx=0.75,rely=0.4,relwidth=0.25,relheight=0.2)
        #
        self.etEntrance_user_type = Label(self,fg='black',font=('微软雅黑',18),state='disabled')
        self.etEntrance_user_type.place(relx=0.75,rely=0.6,relwidth=0.25,relheight=0.2)
        #
        self.btok = Button(self)
        self.btok["text"] = "确定"
        self.btok.place(relx=0.5,rely=0.8,relwidth=0.5,relheight=0.1)
        self.btok["command"] = self.ok


    def ok(self):
        self.numbername = self.etEntrance_number_plate.get()
        self.curr_time = datetime.datetime.now().replace(microsecond=0)
        n = str(self.curr_time).find(".")
        timechar = str(self.curr_time)[:n].split(" ")
        self.etEntrance_admission_time['text'] = timechar[1]
        db = dd.datab()
        cursor=db.cursor()
        sql='SELECT * FROM user_account where license=\'%s\''% self.numbername
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            flag=0 
            for row in results: 
                flag=1
                self.etEntrance_user_type['text'] ="注册用户"
            if(flag==0):        
                self.etEntrance_user_type['text'] ="非注册用户"
            sql_insert='insert into record (license,begin_time)values(\'%s\',\'%s\')'% ( self.numbername,self.curr_time )
            cursor.execute(sql_insert)
            db.commit()
        except Exception as e:
            print(e)
            tkinter.messagebox.showwarning('警告','出错')
        db.close()
        ll.ensay(self.numbername)

    def open(self):
        self.btclose.config(state=NORMAL)
        self.btopen.config(state=DISABLED)
        self.cap = cv.VideoCapture(0)
        self.show()

    def show(self):
        self.success,self.img = self.cap.read()
        if self.success:
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
        self.lbbg()
    
    def lbbg(self):
        self.En_panel['bg'] = 'black'



    # def opfile(self):
    #     '''打开文件的逻辑'''
    #     self.master.update()
    #     x = int(self.master.winfo_width()*0.7*0.5)
    #     y = int(self.master.winfo_height()*0.8*0.48*0.84)
    #     self.dirname = filedialog.askopenfilename() # 打开文件对话框
    #     if not self.dirname:
    #         messagebox.showwarning('警告', message='未选择文件夹！')  # 弹出消息提示框
    #     img = cv.imread(self.dirname)
    #     image = cv.resize(img,(x,y))
    #     cvimage = cv.cvtColor(image,cv.COLOR_BGR2RGBA)
    #     current_image = Image.fromarray(cvimage)
    #     imgtk = itk.PhotoImage(image=current_image)
    #     self.En_panel.imgtk = imgtk
    #     self.En_panel.config(image=imgtk)
    #     a = d.Do()
    #     self.numbername = a.do(img)





if __name__ == '__main__':
    root = Tk()
    root.title("智能车牌识别收费系统")
    # 获取当前屏幕的宽
    width = 1120
    # 获取当前屏幕的高
    height = 692
    root.geometry("{0}x{1}+-9+0".format(width,height))
    a = ArtEnMonitor(root)
    root.mainloop()
    cv.destroyAllWindows()