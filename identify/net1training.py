import sys
import os
import numpy as np
import cv2
import tensorflow as tf
from sklearn.model_selection import train_test_split


cur_dir = os.getcwd().replace('\\','/')
arent_path = os.path.dirname(cur_dir).replace('\\','/')
data_dir = os.path.join(arent_path, 'images/province')
label = ['川', '鄂', '赣', '甘', '贵', '桂', '黑', '沪', '冀', '津',
                '京', '吉', '辽', '鲁', '蒙', '闽', '宁', '青', '琼',
                '陕', '苏', '晋', '皖', '湘', '新', '豫', '渝', '粤', '云',
                '藏', '浙']
dataset = ['Schuan','Se','Sgan','Slong','Sgui','Sguii','Shei','Shu','Sjii','Sjin','Sjing','Sji','Sliao',
           'Slu','Smeng','Smin','Sning','Sqing','Sqiong','Sshan','Ssu','Sjinn','Swan','Sxiang','Sxin',
            'Syuu','Syu','Syue','Syun','Szang','Szhe']
dataset_len = len(dataset)
def list_all_files(root):
    files = []
    list = os.listdir(root)
    for i in range(len(list)):
        element = os.path.join(root, list[i])
        if os.path.isdir(element):
            temp_dir = os.path.split(element)[-1]
            if temp_dir in dataset:
                files.extend(list_all_files(element))
        elif os.path.isfile(element):
            files.append(element)
    return files
def init_data(dir):
    X = []
    y = []
    if not os.path.exists(data_dir):
        raise ValueError('没有找到文件夹')
    files = list_all_files(dir)
    i = 0
    for file in files:
        
        i+=1
        src_img = cv2.imread(file, cv2.COLOR_BGR2GRAY)
        if src_img.ndim == 3:
            continue
        resize_img = cv2.resize(src_img, (20, 20))
        resize_img = cv2.threshold(resize_img,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        X.append(resize_img[1])
        # 获取图片文件全目录
        dir = os.path.dirname(file)
        # 获取图片文件上一级目录名
        dir_name = os.path.split(dir)[-1]
        vector_y = [0 for i in range(len(dataset))]
        index_y = dataset.index(dir_name)
        vector_y[index_y] = 1
        y.append(vector_y)

    X = np.array(X)
    y = np.array(y).reshape(-1, dataset_len)
    return X, y

X,y = init_data(data_dir)

#对输入数据整理
def X_Two_dimensional(x):
    '''将三维数组变成二维'''
    X = np.empty((x.shape[0],400))
    for i in range(X.shape[0]):
        X[i] = np.array(x[i]).reshape((1,400))
    return X

X = X_Two_dimensional(X)
#对数据集分割，分为训练集与测试集
train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=0)

#定义一个神经网络，结构400-100-31
#定义输入层到隐藏层之间的权值矩阵,取值范围为（-1，1）
V = np.random.random((400,140))*2-1
# 定义隐藏层1到隐藏层2之间的权值矩阵，取值范围为（-1，1）
W = np.random.random((140,31))*2-1

# 激活函数
def sigmoid(x):
    return 1/(1+np.exp(-x))

# 激活函数的导数
def dsigmoid(x):
    return x*(1-x)

# 训练模型
def train(X,y,steps=30000,lr=0.31):
    global V,W
    for n in range(steps+1):
        # 随机选取一个数据
        i = np.random.randint(X.shape[0])
        # 获取一个数据
        x = X[i]
        x = np.atleast_2d(x)
        # BP算法公式
        # 计算隐藏层1的输出
        L1 = sigmoid(np.dot(x,V))
        # 计算输出的输出
        L2 = sigmoid(np.dot(L1,W))
        # 计算L2_delta，L1_delta
        L2_delta = (y[i]-L2)*dsigmoid(L2)
        L1_delta = L2_delta.dot(W.T)*dsigmoid(L1)
        # 更新权值
        W += lr*L1.T.dot(L2_delta)
        V += lr*x.T.dot(L1_delta)
        
        # 每训练1000次预测一次准确率
        if n%5000==0:
            output = predict(test_x)
            predictions = np.argmax(output,axis=1)
            pre_y = np.argmax(test_y,axis=1)
            acc = np.mean(np.equal(predictions,pre_y))
            print('steps:',n,'accuracy:',acc)

def predict(x):
    # 计算隐藏层的输出
    L1 = sigmoid(np.dot(x,V))
    # 计算输出的输出
    L2 = sigmoid(np.dot(L1,W))
    return L2

if __name__ == '__main__':
    train(train_x,train_y,200000,0.31)
    #保存训练数据
    net1V = os.path.join(cur_dir,'Txtnetdata/net1V.txt')
    np.savetxt(net1V,V)
    net1W = os.path.join(cur_dir,'Txtnetdata/net1W.txt')
    np.savetxt(net1W,W)