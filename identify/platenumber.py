# import sys
# import cv2
# import numpy as np


# class Plateidenty():

# 	def preprocess(self,gray):
# 		# # 直方图均衡化
# 		# equ = cv2.equalizeHist(gray)
# 		# 高斯平滑
# 		gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
# 		# 中值滤波
# 		median = cv2.medianBlur(gaussian, 5)
# 		# Sobel算子，X方向求梯度
# 		sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0, ksize = 3)
# 		# 二值化
# 		ret, binary = cv2.threshold(sobel, 170, 255, cv2.THRESH_BINARY)
# 		# 膨胀和腐蚀操作的核函数
# 		element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
# 		element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
# 		# 膨胀一次，让轮廓突出
# 		dilation = cv2.dilate(binary, element2, iterations = 1)
# 		# 腐蚀一次，去掉细节
# 		erosion = cv2.erode(dilation, element1, iterations = 1)
# 		# 再次膨胀，让轮廓明显一些
# 		dilation2 = cv2.dilate(erosion, element2,iterations = 3)
# 		#cv2.imshow('dilation2',dilation2)
# 		#cv2.waitKey(0)
# 		return dilation2

# 	def findPlateNumberRegion(self,img):
# 		region = []
# 		# 查找轮廓
# 		contours,hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 		# 筛选面积小的
# 		for i in range(len(contours)):
# 			cnt = contours[i]
# 			# 计算该轮廓的面积
# 			area = cv2.contourArea(cnt)

# 			# 面积小的都筛选掉
# 			if (area < 1800):
# 				continue

# 			# 轮廓近似，作用很小
# 			epsilon = 0.001 * cv2.arcLength(cnt,True)
# 			approx = cv2.approxPolyDP(cnt, epsilon, True)

# 			# 找到最小的矩形，该矩形可能有方向
# 			rect = cv2.minAreaRect(cnt)
# 			print ("rect is: ")
# 			print (rect)

# 			# box是四个点的坐标
# 			box = cv2.boxPoints(rect)
# 			box = np.int0(box)

# 			# 计算高和宽
# 			height = abs(box[0][1] - box[2][1])
# 			width = abs(box[0][0] - box[2][0])
# 			# 车牌正常情况下长高比在2.7-5之间
# 			ratio =float(width) / float(height)
# 			print (ratio)
# 			if (ratio > 5 or ratio < 2):
# 				continue
# 			region.append(box)

# 		return region

# 	def detect(self,img):
# 		# 转化成灰度图
# 		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
# 		# 形态学变换的预处理
# 		dilation = self.preprocess(gray)

# 		# 查找车牌区域
# 		region = self.findPlateNumberRegion(dilation)

# 		# 用绿线画出这些找到的轮廓
# 		for box in region:
# 			cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
# 		ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
# 		xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]
# 		ys_sorted_index = np.argsort(ys)
# 		xs_sorted_index = np.argsort(xs)

# 		x1 = box[xs_sorted_index[0], 0]
# 		x2 = box[xs_sorted_index[3], 0]

# 		y1 = box[ys_sorted_index[0], 1]
# 		y2 = box[ys_sorted_index[3], 1]

# 		img_plate = img[y1+17:y2-17, x1+17:x2-17]

# 		return img_plate



# if __name__ == '__main__':

# 	imagePath = 'C:/Users/Abel/Desktop/License_Plate_Recognition/other/test/2.jpg'
# 	img = cv2.imread(imagePath)
# 	print(type(img))
# 	print(img.shape)
# 	img = cv2.resize(img,(640,480))
# 	cv2.imshow('img', img)
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()
# 	a = Plateidenty()
# 	img = a.detect(img)
# 	cv2.imshow('img', img)
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()
import cv2
import numpy as np


def stretch(img):
    max = float(img.max())
    min = float(img.min())
 
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = (255/(max-min))*img[i,j]-(255*min)/(max-min)
             
    return img
     
def dobinaryzation(img):
    max = float(img.max())
    min = float(img.min())
     
    x = max - ((max-min) / 2)
    ret, threshedimg = cv2.threshold(img, x, 255, cv2.THRESH_BINARY)
     
    return threshedimg
 
def find_retangle(contour):
    y, x = [], []

    for p in contour:
        y.append(p[0][0])
        x.append(p[0][1])

    return [min(y), min(x), max(y), max(x)]
 
def locate_license(img, orgimg):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找出最大的三个区域
    blocks = []
    for c in contours:
        # 找出轮廓的左上点和右下点，由此计算它的面积和长宽比
        r = find_retangle(c)
        a = (r[2]-r[0]) * (r[3]-r[1])
        s = (r[2]-r[0]) / (r[3]-r[1])

        blocks.append([r, a, s])

    # 选出面积最大的3个区域
    blocks = sorted(blocks, key=lambda b: b[2])[-3:]

    # 使用颜色识别判断找出最像车牌的区域
    maxweight = 0
    maxindex = -1
    for i in range(len(blocks)):
        b = orgimg[blocks[i][0][1]:blocks[i][0][3], blocks[i][0][0]:blocks[i][0][2]]
        # RGB转HSV
        hsv = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
        # 蓝色车牌范围
        lower = np.array([100,50,50])
        upper = np.array([140,255,255])
        # 根据阈值构建掩模
        mask = cv2.inRange(hsv, lower, upper)

        # 统计权值
        w1 = 0
        for m in mask:
            w1 += m / 255

        w2 = 0
        for w in w1:
            w2 += w

        # 选出最大权值的区域
        if w2 > maxweight:
            maxindex = i
            maxweight = w2

    return blocks[maxindex][0]

def find_license(img):
    '''预处理'''
    #img=cv2.GaussianBlur(img,(5,5),1)
    # 压缩图像
    img = cv2.resize(img, (400, 400*img.shape[0]//img.shape[1]))

    # RGB转灰色
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 灰度拉伸
    stretchedimg = stretch(grayimg)

    # 进行开运算，用来去噪声
    r = 16
    h = w = r * 2 + 1
    kernel = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(kernel, (r, r), r, 1, -1)

    openingimg = cv2.morphologyEx(stretchedimg, cv2.MORPH_OPEN, kernel)
    strtimg = cv2.absdiff(stretchedimg,openingimg)

    # 图像二值化
    binaryimg = dobinaryzation(strtimg)

    # 使用Canny函数做边缘检测
    cannyimg = cv2.Canny(binaryimg, binaryimg.shape[0], binaryimg.shape[1])

    ''' 消除小区域，保留大块区域，从而定位车牌'''
    # 进行闭运算
    kernel = np.ones((5,19), np.uint8)
    closingimg = cv2.morphologyEx(cannyimg, cv2.MORPH_CLOSE, kernel)

    # 进行开运算
    openingimg = cv2.morphologyEx(closingimg, cv2.MORPH_OPEN, kernel)

    # 再次进行开运算
    kernel = np.ones((11,5), np.uint8)
    openingimg = cv2.morphologyEx(openingimg, cv2.MORPH_OPEN, kernel)

    # 消除小区域，定位车牌位置
    rect = locate_license(openingimg, img)

    return rect, img

if __name__ == '__main__':
    # 读取图片
    orgimg = cv2.imread('E:/License_Plate_Recognition/images/pictures/9.jpg')
    rect, img = find_license(orgimg)

    # 框出车牌
    #cv2.rectangle(img, (rect[0], rect[1]), (rect[2], rect[3]), (0,255,0),2)
    image = img[rect[1]:rect[3],rect[0]:rect[2],:]
    print(image.shape)
    
    cv2.imshow('img', img)

    cv2.waitKey(10000)
    cv2.destroyAllWindows()
    cv2.imshow('image', image)
    cv2.imwrite('test1.jpg',image)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()
