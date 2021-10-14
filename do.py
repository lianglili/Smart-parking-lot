import identify.identifynet1 as ii1
import identify.identifynet2 as ii2
import identify.identifynet3 as ii3
import identify.platenumber as ip
import identify.divide as iid
import LPRspeech.LPRspeech as ll
import numpy as np
import datetime
import cv2 as cv
import sys
import os
from aip import AipOcr
import json



class Do():

	def do(self,pic):
		self.curr_path = os.getcwd().replace("\\","/")
		self.curr_time = str(datetime.datetime.now()).replace(" ","")
		self.curr_time = self.curr_time.replace(".","")
		self.curr_time = self.curr_time.replace(":","")
		rect, img = ip.find_license(pic)
		listc = img[rect[1]:rect[3],rect[0]:rect[2],:]
		self.listchar = iid.divide_image(listc)
		for i in range(len(self.listchar)):
			cv.imwrite('{0}/result/charimage/{1}{2}.jpg'.format(self.curr_path,self.curr_time,i),self.listchar[i])
		self.number = self.didentify()
		print(self.number)
		return self.number


	def didentify(self):
		# for i in self.listchar:
		# 	cv.imshow('img',i)
		# 	cv.waitKey(0)
		# cv.destroyAllWindows()
		try:
			i1 = ii1.Net1()
			s1 = i1.dataidentify(self.listchar[0])
			i2 = ii2.Net2()
			s2 = i2.dataidentify(self.listchar[1])
			i3 = ii3.Net3()
			s3 = i3.dataidentify(self.listchar[2])
			s4 = i3.dataidentify(self.listchar[3])
			s5 = i3.dataidentify(self.listchar[4])
			s6 = i3.dataidentify(self.listchar[5])
			s7 = i3.dataidentify(self.listchar[6])
		except Exception as e:
			print(e)
			ll.say("识别错误")
			return "识别错误"
		a = s1+s2+s3+s4+s5+s6+s7
		return  a

	def enspeech(self,payment):
		ll.ensay(self.number)
		if payment <= 2:
			ll.paymentreminder()

	def exspeech(self,fee):
		ll.exsay(self.number,self.hour,self.minuter,self.fee)

	def get_file_content(self,filePath):
	    with open(filePath, 'rb') as fp:
	        return fp.read()

	""" get licsense plate """
	def get_license_plate(self,filePath):
	    """ APPID AK SK """
	    APP_ID = '20566720'
	    API_KEY = 'uXG0RZ6rLLzkHQC9tY2DvTPs'
	    SECRET_KEY = 'UYhI9C71xpL0WNOGkz5sCq887KglH4Zk'

	    """ create client """
	    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

	    image = self.get_file_content(filePath)

	    """ 调用车牌识别 """
	    res = client.licensePlate(image)
	    return res

	def doapi(self,str):
		""" call example """
		#str = 'E:/License_Plate_Recognition/images/pictures/99.png' 
		res = self.get_license_plate(str)
		return res['words_result']['number']
		# print('车牌颜色：' + res['words_result']['color'])

if __name__ == '__main__':
	img=cv.imread('E:/License_Plate_Recognition/images/pictures/9.jpg')
	a = Do()
	a.do(img)


