import sys
import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
class Net1():
    def __init__(self):
        self.cur_dir = os.getcwd().replace('\\','/')
        self.data_dir = os.path.join(self.cur_dir, 'images/province')
        self.net1V = os.path.join(self.cur_dir, 'Txtnetdata/net1V.txt')
        self.net1W = os.path.join(self.cur_dir, 'Txtnetdata/net1W.txt')
        
        self.dataset = ['Schuan','Se','Sgan','Slong','Sgui','Sguii','Shei','Shu','Sjii','Sjin','Sjing','Sji','Sliao',
           'Slu','Smeng','Smin','Sning','Sqing','Sqiong','Sshan','Ssu','Sjinn','Swan','Sxiang','Sxin',
            'Syuu','Syu','Syue','Syun','Szang','Szhe']
        self.label = ['川', '鄂', '赣', '甘', '贵', '桂', '黑', '沪', '冀', '津',
                '京', '吉', '辽', '鲁', '蒙', '闽', '宁', '青', '琼',
                '陕', '苏', '晋', '皖', '湘', '新', '豫', '渝', '粤', '云',
                '藏', '浙']
        self.dataset_len = len(self.dataset)
        self.V = np.loadtxt(self.net1V)
        self.W = np.loadtxt(self.net1W)
    # 激活函数
    def sigmoid(self,x):
        return 1/(1+np.exp(-x))
    def predict(self,x):
        # 计算隐藏层的输出
        L1 = self.sigmoid(np.dot(x,self.V))
        # 计算输出的输出
        L2 = self.sigmoid(np.dot(L1,self.W))
        return L2
    def dataidentify(self,img):
        #定义图片宽度
        width = 20
        #定义图片长度
        high = 20
        index = (img == 255)
        img[index] = 1
        image = cv.resize(img,(width,high))
        # gray = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
        # image = cv.threshold(gray,0,1,cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        X = np.empty((1,400))
        X = np.array(image).reshape((1,400))
        output = self.predict(X)
        pre = np.argmax(output)
        return self.label[pre]