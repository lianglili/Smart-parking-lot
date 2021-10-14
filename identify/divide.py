import cv2
def divide_image(img):
    #img=cv2.imread(imagepath)
    img1=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img2=img1
    cv2.threshold(img1,100,255,cv2.THRESH_BINARY_INV,img2)
    #cv2.imwrite('gray.jpg',img2)
    white=[]
    black=[]
    h,w=img2.shape
    white_max=0
    black_max=0
    for i in range(w):
        nw=0
        nb=0
        for j in range(h):
            if img2[j][i]==255:
                nw+=1
            if img2[j][i]==0:
                nb+=1
        white_max=max(white_max,nw)
        black_max=max(black_max,nb)
        white.append(nw)
        black.append(nb)
    arg=False
    if black_max>white_max:
        arg=True

    def find_end(start_):
        end_ = start_ + 1
        for m in range(start_ + 1, w - 1):
            if (black[m] if arg else white[m]) > (0.95 * black_max if arg else 0.95 * white_max):  # 0.95这个参数请多调整，对应下面的0.05
                end_ = m
                break
        return end_
    n=1
    start=1
    end=2
    imagelist=[]
    while n<w-2:
        n+=1
        if (white[n] if arg else black[n]) > (0.05*white_max if arg else 0.05*black_max):
            start=n
            end=find_end(start)
            n=end
            if end-start>5:
                cj=img2[8:h-6,start-1:end+1]
                print(cj.shape)
                #cv2.imshow('cut.jpg',cj)
                #cv2.waitKey(1000)
                imagelist.append(cj)
    return imagelist
if __name__ == '__main__':
    imagepath = "E:/License_Plate_Recognition/listc.jpg"
    img=cv2.imread(imagepath)
    il=divide_image(img)
    t=0
    for i in il:
        t+=1
        cv2.imshow('%s.jpg'%(t),i)
        cv2.waitKey(1000)







