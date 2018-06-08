# -*- coding: utf-8 -*-
# Created Time    : 18-6-6 下午5:28
# Connect me with : sttide@outlook.com

import tensorflow as tf
import reader
import vgg
from os import *

# 以下先用conv提取特征

# 分离的图层
CONTENT_LAYERS = ["relu4_2"]
#STYLE_LAYERS = ["relu1_1", "relu2_1", "relu3_1", "relu4_1", "relu5_1"]
STYLE_LAYERS = ["relu4_1"]
#学习率
LEARNING_RATE = 0.1

def gram(layer):
    shape = tf.shape(layer)
    num_images = shape[0]
    width = shape[1]
    height = shape[2]
    num_filters = shape[3]
    filters = tf.reshape(layer, tf.stack([num_images, -1, num_filters]))
    grams = tf.matmul(filters, filters, transpose_a=True) / tf.to_float(width * height * num_filters)
    return grams


def get_style_features(style_paths, style_layers):
    with tf.Graph().as_default() as g:
        images = tf.stack([reader.get_image(style_paths,256)])
        net, _ = vgg.net(images - reader.mean_pixel)
        features = []
        for layer in style_layers:
            features.append(gram(net[layer]))

        with tf.Session() as sess:
            return sess.run(features)


def get_content_features(content_layers):
    with tf.Graph().as_default() as g:
        #tf.expand_dims 在位置0扩展了一个维度[2,3]=>[1,2,3]变成图片
        fea_content = []
        for file in range(1000):
            file_path = "GrayPics/"
            file_name = str(file) + ".jpg"
            img_path = path.join(file_path, file_name)
            image = tf.stack([reader.get_image(img_path,256)])
            net, _ = vgg.net(image)
            for layer in content_layers:
                # net字典形式，net{"conv1_1":"conv1_1的结果“}
                fea_content.append(gram(net[layer]))

        with tf.Session() as sess:
                #返回features + 图片
                return sess.run(fea_content)


def act(style_paths):

    style_features_t = get_style_features(style_paths, STYLE_LAYERS)
    content_features = get_content_features(CONTENT_LAYERS)

    print(tf.shape(style_features_t))
    print(tf.shape(content_features))
    y = content_features - style_features_t

    content_loss = 0
    for layer in CONTENT_LAYERS:
        content_loss += tf.nn.l2_loss(content_features - style_features_t)
    content_loss = content_loss

    style_loss = 0
    style_loss += tf.nn.l2_loss(content_features - style_features_t)


    loss = style_loss + content_loss

    #训练方法
    train_op = tf.train.AdamOptimizer(LEARNING_RATE).minimize(loss)

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        for step in range(1):
            _, real_y = sess.run([train_op, y])
            print("step:",real_y)


if __name__ == "__main__":
    act("./GrayPics/111.jpg")
