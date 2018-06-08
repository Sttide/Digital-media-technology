import tensorflow as tf
a = tf.constant([1, 2, 3, 4, 5, 6], shape=[1,6])
b = tf.constant([1,1,1,1,1,1,1,1,1,1,1,1],shape=[6,2])
c = tf.matmul(a, b)
with tf.Session() as sess:
    c = sess.run(c)
    print(a.eval())
    print(b.eval())
    print(c)


'''
PCA随机数据

import matplotlib.pyplot as plt

batch_size = 37
seed = 23455
rnd = np.random.RandomState(seed)

def generate():
    #生成数据
    X = [];Y = []
    for i in range(30):
        r = np.random.uniform(2, 6)
        X.append(r)
    for i in range(30):
        r = np.random.uniform(5, 8)
        Y.append(r)
    R = []
    for i in range(len(X)):
        R.append([X[i],Y[i]])
    np.random.shuffle(R)
    return R

def printGraph(R,length):
    #画图
    for i in range(length):
        plt.scatter(R[i][0], R[i][1], c='g')
    plt.xlim(-5, 10)
    plt.ylim(-5, 10)
    plt.grid()
    plt.show()
    
def PCAtransfer(Martic):
    #PCA算法
    #中心化
    meanR = np.mean(R, axis=0)
    print(meanR)
    cen_R = []
    for i in range(len(R)):
        res = R[i] - meanR
        cen_R.append(res)
    print(cen_R)
    printGraph(cen_R, len(cen_R))
    # 求协防差矩阵
    cen_Rrr = np.array(cen_R)
    cov_R = np.cov(cen_Rrr.T)
    print(cov_R.shape)
    # 求特征值和特征向量
    lambd, features = np.linalg.eig(cov_R)
    print(lambd)
    print(features)
    # KL变换
    if lambd[0] > lambd[1]:
        maxlambd = 0
    else:
        maxlambd = 1
    print(features[maxlambd])
    new_R = cen_R * features[maxlambd].T
    printGraph(new_R, len(new_R))

'''
