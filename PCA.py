from pylab import *
from os import *
import cv2

def PCAimage(img):
    #求均值
    meanImg = np.mean(img, axis=0)
    print("图像均值:",meanImg)

    #中心化
    new_img = []
    for i in range(len(img)):
        x = img[i] - meanImg[i]
        new_img.append(x)
    imarr = np.array(new_img)

    #求协防差矩阵
    cov_img = np.dot(imarr,imarr.T)
    print("协防差矩阵的维度:",cov_img.shape)
    # 求特征值和特征向量
    lambd, features = np.linalg.eig(cov_img)

    #求取能量总和大于90%的特征值和特征向量
    total_sum = lambd.sum()
    print("lambda's total_sum:",total_sum)
    sort_lambd = sorted(lambd, reverse=True)
    print(sort_lambd)
    sum = 0
    rest = []
    for i in range(len(lambd)):
        if sum/total_sum < 0.90:
            sum = sum + sort_lambd[i]
            inde = np.where(lambd == sort_lambd[i])
            rest.append(features[inde])
        else:
            break
    rest = np.reshape(rest,[len(rest),100])
    print("用到的特征值的和:",sum, "\t需要用的特征向量的个数:",len(rest))
    print("特征值的shape",np.shape(rest))

    #返回均值、中心化的图像、降维之后的基
    return meanImg, np.array(new_img), rest



def getPics(start, end, file_path):
    img = []        #img存储图片的信息
    imgsize = []    #imgsize存储每个图片的长宽
    circle = start
    while (circle < end):
        file_name = str(circle) + ".jpg"
        img_path = path.join(file_path, file_name)
        imgs = cv2.imread(img_path)
        imgsize.append([imgs.shape[0], imgs.shape[1]])
        img.append(np.array(imgs[:, :, 0].flatten()))
        circle = circle + 1
    img = np.array(img)
    print("所有图像数据的shape:", img.shape)
    return img, imgsize

def display():
    pass

#生成1000张降维处理之后的结果
def Result(clun, imgsize):
    for i in range(100):
        show_img = np.array(clun[i].repeat(3), dtype=int)
        m, n = imgsize[i][0], imgsize[i][1]
        file_name = str(i) + ".jpg"
        img_path = path.join(save_path, file_name)
        cv2.imwrite(img_path, show_img.reshape(m,n,3))


if __name__ == "__main__":
    file_path = "GrayPics/"
    save_path = "Result/"
    #图片类别的起末位置
    start = 100
    end = 200
    show_num = 7    #0-100 查看结果的图片的索引

    #获取图片信息
    img, imgsize = getPics(start,end,file_path)
    #PCA处理
    meanImg, new_img, rest = PCAimage(img)

    # 用归一化后的各个数据与特征矩阵相乘，映射到新的空间
    new_imgs = np.dot(new_img.T, rest.T)
    print("映射:",new_imgs.shape)
    # 还原原始数据
    new_imgss = np.dot(new_imgs,rest)+(meanImg.repeat(100).reshape([-1,100]))
    print("映射之后的数据:", new_imgss.shape)

    clun = new_imgss.T      #新生成图片的数据
    show_img = np.array(clun[show_num].repeat(3), dtype=int)
    print(show_img)
    print("show_imgs_shape:",show_img.shape)
    m,n = imgsize[show_num][0],imgsize[show_num][1]
    imshow(show_img.reshape(m,n,3))
    show()
