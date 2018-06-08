# -*- coding: utf-8 -*-
# Created Time    : 18-5-23 上午10:30
# Connect me with : sttide@outlook.com

from pylab import *
from os import *
import cv2

def get_img(file):
    file_path = "GrayPics/"
    file_name = str(file) + ".jpg"
    img_path = path.join(file_path, file_name)
    imgs = cv2.imread(img_path)
    m,n = imgs.shape[0], imgs.shape[1]
    img = []
    img.append(imgs[:,:,0])
    img = np.array(img).reshape([m,n])
    print(img)
    print(img.shape)
    return img

def K_meansImg(img, c):
    m, n = img.shape[0], img.shape[1]
    generate = np.zeros([m,n])
    goal_class = set()
    num = len(goal_class)
    while(num < c):
        init = np.random.randint(255)
        goal_class.add(init)
        num = len(goal_class)
    print(num)
    print(goal_class)

    class_fea = list(goal_class)
    class_lab = np.zeros([m, n])
    for circle in range(100):
        for i in range(m):
            for j in range(n):
                min_dist = 99999999
                min_class = 0
                for cl in range(c):
                    dist = (img[i][j]-class_fea[cl])*(img[i][j]-class_fea[cl])
                    if min_dist>dist:
                        min_dist = dist
                        min_class = cl

                class_lab[i][j] = min_class
        change = 0
        for cl in range(c):
            sum = 0
            count = 0
            for i in range(m):
                for j in range(n):
                    if (class_lab[i][j]==cl):
                        sum = sum + img[i][j]
                        count = count+1
            if class_fea[cl] != sum/count:
                class_fea[cl] = sum / count
                change = 1
        if(change == 0):
            break
        print(circle, ":", class_fea)

    print(class_fea)
    for i in range(m):
        for j in range(n):
            pixe = int(class_lab[i][j])
            generate[i][j] = class_fea[pixe]

    generate.reshape(m,n)
    imshow(generate,cmap='gray')
    show()

#Gaps方法确定K值
def Get_Kfea(k):
    num =0
    goal_class = set()
    while (num < k):
        x = np.random.randint(255)
        goal_class.add(x)
        num = len(goal_class)
    print(num)
    print(goal_class)
    goal_class = list(goal_class)
    return goal_class

def GapsK(img):
    m, n = img.shape[0], img.shape[1]
    generate = np.zeros([m, n])
    ssw = np.zeros([11])   #每次分类的数量
    ssb = 0
    for k in range(1,11):
        class_fea = Get_Kfea(k)
        class_lab = np.zeros([m, n])
        for circle in range(100):
            for i in range(m):
                for j in range(n):
                    min_dist = 99999999
                    min_class = 0
                    for cl in range(k):
                        dist = (img[i][j] - class_fea[cl]) * (img[i][j] - class_fea[cl])
                        if min_dist > dist:
                            min_dist = dist
                            min_class = cl

                    class_lab[i][j] = min_class
            change = 0
            for cl in range(k):
                sum = 0
                count = 0
                for i in range(m):
                    for j in range(n):
                        if (class_lab[i][j] == cl):
                            sum = sum + img[i][j]
                            count = count + 1
                if class_fea[cl] != sum / count:
                    class_fea[cl] = sum / count
                    change = 1
            if (change == 0):
                break
            print(circle, ":", class_fea)

        d_r = np.zeros([k]) #类内距离
        n_r = np.zeros([k]) #每一个的数目

        print(class_fea)
        for i in range(m):
            for j in range(n):
                pixe = int(class_lab[i][j])
                d_r[pixe] = d_r[pixe] + abs(img[i][j]-class_fea[pixe])**2
                n_r[pixe] =  n_r[pixe]+1
                generate[i][j] = class_fea[pixe]

        for i in range(k):
            ssw[k] =ssw[k] + d_r[i] /(2*n_r[i])
        print(ssw[k])
        generate.reshape(m, n)
        imshow(generate, cmap='gray')
        show()
    plt.plot(ssw,'.')
    plt.show()

def get_pics():
    file_path = "GrayPics/"
    img = []  # img存储图片的信息
    imgsize = []  # imgsize存储每个图片的长宽
    for file in range(1000):
        file_name = str(file) + ".jpg"
        img_path = path.join(file_path, file_name)
        imgs = cv2.imread(img_path)
        imgs.astype('int32')
        imgsize.append([imgs.shape[0], imgs.shape[1]])
        img.append(np.array(imgs[:, :, 0].flatten()))
    img = np.array(img)
    print(img)
    print(img.shape)
    return img


def K_meansPics(img, c):
    num = 0
    goal_class = set()
    while (num < c):
        x = np.random.randint(1000)
        goal_class.add(x)
        num = len(goal_class)
    print(num)
    print(goal_class)

    goal_class = list(goal_class)
    init = []
    for i in range(c):
        init.append(img[goal_class[i],:])
    class_fea = np.array(init)
    class_lab = np.zeros(img.shape[0])
    #print(class_fea)
    print("A",np.shape(img))
    print("S",np.shape(class_fea))

    for k in range(5000):
        dist = np.zeros([c,img.shape[0]])
        for j in range(c):
            tmp = class_fea[j,:].reshape(1,-1)
            dist[j,:] = np.sum((img-tmp)*(img-tmp),axis=1)

        #最小距离的索引，即为标签
        print(np.shape(dist))
        class_lab = np.argmin(dist,axis=0).reshape(-1,1)
        #print(class_lab)
        print("steps:",k,np.shape(class_lab))

        change = 0
        for cl in range(c):
            #sum_fea = np.zeros(img.shape[1])
            sum_fea = []
            count = 0
            for i in range(img.shape[0]):
                if (class_lab[i] == cl):
                    sum_fea.append(img[i])
                    count = count + 1

            if (count != 0):
                mean_fea = np.mean(sum_fea,axis=0)
                mean_fea = np.array(mean_fea)
                if (np.all(class_fea[cl] == mean_fea) and count!=0):
                    class_fea[cl] = mean_fea
                    change = 1
        if (change == 0):
                break

    for i in range(1000):
        print("所属类别：",class_lab[i])
    print(k)
    return class_lab


def Savefig(class_lab, c):
    class_lab = class_lab.reshape(class_lab.shape[0])
    print(np.shape(class_lab))
    for i in range(c):
        x = np.where(class_lab==i)
        plt.figure()
        x = np.array(x)
        x = x.reshape(-1,1)
        for j in range(min(9,len(x))):
            file_name = str(x[j][0]) + ".jpg"
            img_path = path.join("GrayPics/", file_name)
            imgs = cv2.imread(img_path)
            imgs.astype('int32')
            plt.subplot(3,3,j+1)
            plt.imshow(imgs)
        save_name = str(i)
        save_path = path.join("K_meansResult10/",save_name)
        plt.savefig(save_path)
        plt.close()

if __name__=="__main__":
    #对一张图片进行K-means聚类，可实现图像分割
    img = get_img(111)
    #K_meansImg(img, 32)
    GapsK(img)
'''    start_time = time.time()
    img = get_pics()
    c = 256
    class_labs = K_meansPics(img, c)
    Savefig(class_labs, c)
    end_time = time.time()
    print("Total time:", end_time-start_time)
'''
