# -*- coding: utf-8 -*-
# Created Time    : 18-6-5 下午9:46
# Connect me with : sttide@outlook.com

from pylab import *
import matplotlib.pyplot as plt
from os import *
import cv2


def SetDataSet(file_path):
    img = []  # img存储图片的信息
    #imgsize = []  # imgsize存储每个图片的长宽

    for circle in range(10):
        for j in range(70):
            file_name = str(circle*10+j) + ".jpg"
            img_path = path.join(file_path, file_name)
            imgs = cv2.imread(img_path)
            #imgsize.append([imgs.shape[0], imgs.shape[1]])
            img.append(np.array(imgs[:, :, 0].flatten()))
    img = np.array(img)
    print("所有图像数据的shape:", img.shape)
    return img#, imgsize



#获取全部数据的直方图
def Histogram(Data):
    hist = np.zeros([700, 256])
    num = 0
    for circle in range(10):
        for x in range(70):
            i = circle*10+x
            for j in range(98304):
                hist[num][Data[i][j]] = hist[num][Data[i][j]]+1
            num = num + 1
    return hist

def GetHistogram(Data):
    hist = Histogram(Data)
    print(np.shape(hist))
    np.savetxt("histTrain.mat", hist, fmt=" %d", delimiter=" ")
    
    plt.hist(Data[2], bins=256, facecolor='green', alpha=0.75)
    plt.show()
    
'''

def GetHistogram(Data):
    hist = np.zeros([256])
    for i in range(98304):
            hist[Data[i]] = hist[Data[i]]+1
    return hist

def HistogramFea(input_img,k):
    imgs = cv2.imread(input_img)
    img = np.array(imgs[:, :, 0].flatten())
    img_hist = GetHistogram(img)
    matfn = "./histTrain.mat"
    hist = np.loadtxt(matfn, dtype=int)
    dist = CalDist(img_hist, hist, "L2")
    # print(dist)
    print(np.shape(dist))
    x = sort(dist)
    for i in range(1,k+1):
        t = np.where(dist == x[i])
        print((t[0][0]))
'''

def GetInput(file_path):
    imgs = cv2.imread(file_path)
    return np.array(imgs[:, :, 0].flatten())

def CalDist(input_img, data, DistName):
    if DistName == "L2":
        return np.sum((input_img-data)**2,axis=1)
    if DistName ==  "cos":
        return np.dot(input_img, data.T)/(np.sum(input_img)*(np.sum(data,axis=1)))


def Train():
    matfn = "./histTrain.mat"
    hist = np.loadtxt(matfn, dtype=int)
    accurancy = np.zeros([22])
    for k in range(1,20):
        for i in range(700):
            img_hist = hist[i]
            dist = CalDist(img_hist, hist, "L2")
            # print(dist)
            #print(np.shape(dist))
            x = sort(dist)
            label = np.zeros([10])
            for pos in range(k + 1):
                t = np.where(dist == x[pos])
                res = t[0]
                #print(res)
                for bianliang in t[0]:
                    label[int(bianliang/70)] = label[int(bianliang/70)] + 1
            #print(label)
            rea_l = np.argmax(label)
            if (rea_l) == (int(i/70)):
                accurancy[k] = accurancy[k]+1
        print(accurancy[k]/700)
    plt.plot(accurancy,'.')
    plt.show()



if __name__ == "__main__":
    Data = SetDataSet("./GrayPics")
    print(Data)
    GetHistogram(Data)
    Train()
    #HistogramFea("./GrayPics/555.jpg",5)
