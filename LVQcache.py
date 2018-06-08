# -*- coding: utf-8 -*-
# @Time    : 18-5-7 下午2:16
# @Author  : Chao
# @Email   : sttide@outlook.com
# @File    : LVQcache.py
# @Software: PyCharm
import matplotlib.pyplot as plt
import numpy as np
import math
import pylab as pl
import cv2

batch_size = 37
seed = 23455
rnd = np.random.RandomState(seed)

#def generate()
X = [];Y = [];R = []
for i in range(100):
    r = np.random.uniform(0, 10)
    X.append(r)
for i in range(100):
    r = np.random.uniform(0, 10)
    Y.append(r)

for i in range(len(X)):
    R.append([X[i],Y[i]])
np.random.shuffle(R)

X=[];Y=[];labels=[];dataset = []
for i in range(len(R)):
    px, py = R[i][0], R[i][1]
    X.append(px)
    Y.append(py)
    judge = px+2-py
    if(judge > 0):
        plt.scatter(px, py, c='k')
        labels.append(1)
    elif(judge < 0):
        plt.scatter(px, py, c='b')
        labels.append(0)
    dataset.append([i,px,py,labels[i]])

print(dataset)
#for i in dataset:
    #print(i[0],i[1],i[2],i[3])

def dist(a, b):
    return math.sqrt(math.pow(a[1]-b[0], 2)+math.pow(a[2]-b[1], 2))

def LVQ(dataset, a, max_iter):
    #统计样本一共有多少个分类
    T = list(set(i[3] for i in dataset))
    print(len(T))
    #随机产生原型向量
    P = []
    lengths = len(P)

    while lengths==0:
        for i in np.random.choice(100, 1):
            if dataset[i][3] == 0:
                P.append([dataset[i][1], dataset[i][2]])
        lengths = len(P)
    while lengths==1:
        for i in np.random.choice(100, 1):
            if dataset[i][3] == 1:
                P.append([dataset[i][1], dataset[i][2]])
        lengths = len(P)
    print(len(P))

    while max_iter > 0:
        X = np.random.choice(100, 1)[0]
        dist1 = dist(dataset[X],P[0])
        dist2 = dist(dataset[X],P[1])
        if(dist1 > dist2):
            t = 0
            index = 0
        else:
            t = 1
            index = 1
        #print(index,t)
        if t == 1:
            P[index] = ((1 - a) * P[index][0] + a * dataset[X][1], (1 - a) * P[index][1] + a * dataset[X][2])
        else:
            P[index] = ((1 + a) * P[index][0] - a * dataset[X][1], (1 + a) * P[index][1] - a * dataset[X][2])
        max_iter -= 1
    return P

def train_show(dataset, P):
    C = [[] for i in P]
    for i in dataset:
        C[i[3] == 1].append(i)
    return C

#画图
def draw(C, P):
    colValue = ['r', 'c', 'g', 'b', 'y', 'k', 'm']
    for i in range(len(C)):
        coo_X = []    #x坐标列表
        coo_Y = []    #y坐标列表
        for j in range(len(C[i])):
            coo_X.append(C[i][j][1])
            coo_Y.append(C[i][j][2])
        pl.scatter(coo_X, coo_Y, marker='x', color=colValue[i%len(colValue)], label=i)
    #展示原型向量
    P_x = []
    P_y = []
    for i in range(len(P)):
        P_x.append(P[i][0])
        P_y.append(P[i][1])
        print(P[i][0], P[i][1])
        pl.scatter(P[i][0], P[i][1], marker='o', color=colValue[i%len(colValue)], label="vector")
    pl.legend(loc='upper right')
    pl.show()

if __name__ == "__main__":
    plt.xlim(-2.5, 12.5)
    plt.ylim(-2.5, 12.5)
    plt.grid()
    P = LVQ(dataset,0.1,1000)
    #plt.show()

    C = train_show(dataset, P)
    draw(C, P)

