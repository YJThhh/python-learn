import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
from numpy import *


def loadDataSet(filename):
    fr = open(filename)
    data = []
    label = []
    for line in fr.readlines():
        lineAttr = line.strip().split('\t')
        data.append([float(x) for x in lineAttr[:-1]])
        label.append(float(lineAttr[-1]))
    return data, label


def selectJrand(i, m):
    j = i
    while j == i:
        j = int(random.uniform(0, m))
    return j


def clipAlpha(a_j, H, L):
    if a_j > H:
        a_j = H
    if L > a_j:
        a_j = L
    return a_j


def smoSimple(data, label, C, toler, maxIter):
    dataMatrix = mat(data)
    labelMatrix = mat(label).transpose()
    b = 0.0
    iter = 0
    m, n = shape(dataMatrix)
    alpha = mat(zeros((m, 1)))
    while iter < maxIter:
        alphapairChanged = 0
        for i in range(m):
            fxi = float(multiply(alpha, labelMatrix).T * (dataMatrix * dataMatrix[i, :].T)) + b
            Ei = fxi - float(labelMatrix[i])
            if labelMatrix[i] * Ei < -toler and alpha[i] < C or labelMatrix[i] * Ei > toler and alpha[i] > 0:
                j = selectJrand(i, m)
                fxj = float(multiply(alpha, labelMatrix).T * (dataMatrix * dataMatrix[j, :].T)) + b
                Ej = fxj - float(labelMatrix[j])
                alphaIOld = alpha[i].copy()
                alphaJOld = alpha[j].copy()
                if labelMatrix[i] != labelMatrix[j]:
                    L = max(0, alpha[j] - alpha[i])
                    H = min(C, C + alpha[j] - alpha[i])
                else:
                    L = max(0, alpha[i] + alpha[j] - C)
                    H = min(C, alpha[j] + alpha[i])
                if L == H:
                    # print ("L==H")
                    continue
                eta = 2.0 * dataMatrix[i, :] * dataMatrix[j, :].T - dataMatrix[i, :] * dataMatrix[i, :].T - dataMatrix[
                                                                                                            j,
                                                                                                            :] * dataMatrix[
                                                                                                                 j, :].T
                if eta >= 0:
                    # print ("eta >= 0")
                    continue
                alpha[j] -= labelMatrix[j] * (Ei - Ej) / eta
                alpha[j] = clipAlpha(alpha[j], H, L)
                if abs(alpha[j] - alphaJOld) < 0.00001:
                    # print ("j not move enough")
                    continue
                alpha[i] += labelMatrix[j] * labelMatrix[i] * (alphaJOld - alpha[j])
                b1 = b - Ei - labelMatrix[i] * (alpha[i] - alphaIOld) * dataMatrix[i, :] * dataMatrix[i, :].T \
                     - labelMatrix[j] * (alpha[j] - alphaJOld) * dataMatrix[i, :] * dataMatrix[j, :].T
                b2 = b - Ej - labelMatrix[i] * (alpha[i] - alphaIOld) * dataMatrix[i, :] * dataMatrix[j, :].T \
                     - labelMatrix[j] * (alpha[j] - alphaJOld) * dataMatrix[j, :] * dataMatrix[j, :].T
                if alpha[i] > 0 and alpha[i] < C:
                    b = b1
                elif alpha[j] > 0 and alpha[j] < C:
                    b = b2
                else:
                    b = (b1 + b2) / 2.0
                alphapairChanged += 1
                # print ("iter: %d i:%d,oairs changed %d" %(iter,i,alphapairChanged))
        if alphapairChanged == 0:
            iter += 1
        else:
            iter = 0
        # print ("iteration number: %d" % iter)
    return b, alpha


def main():
    train = pd.read_csv('/home/aistudio/data/data14453/train1.csv')
    data = np.hstack((np.array(train['X']).reshape(len(train), 1), np.array(train['Y']).reshape(len(train), 1)))
    label = np.array(train['Class'])
    test = pd.read_csv('/home/aistudio/data/data14453/test1.csv')
    data_test = np.hstack((np.array(test['X']).reshape(len(test), 1), np.array(test['Y']).reshape(len(test), 1)))
    # print (data)
    # print (label)
    b, alpha = smoSimple(data, label, 0.6, 0.001, 40)
    # print (b)
    # print (alpha)
    # for i in range(100):
    # if alpha[i]>0:
    # print (data[i],label[i])

    w1 = 0
    w2 = 0
    # print(data[0].shape[0])

    # print(data[0])
    for i in range(alpha.shape[0]):
        w1 += alpha[i] * label[i] * data[i][0]
        w2 += alpha[i] * label[i] * data[i][1]  # 根据公式分别求出w向量里面的分量
    x = np.arange(-5, 25)
    y = (-b.tolist()[0][0] - (w1.tolist()[0][0]) * x) / (w2.tolist()[0][0])  # 分类器表达式
    plt.figure(figsize=(8, 8))
    plt.xlim(-5, 25)
    plt.ylim(-5, 25)
    plt.plot(x, y)
    class1_X, class1_Y, class2_1_X, class2_1_Y, class2_2_X, class2_2_Y, class_sv_X, class_sv_Y = [], [], [], [], [], [], [], []
    for i in range(180):  # 提取支持向量
        if -0.01 < (w2.tolist()[0][0]) * data[i][1] + (w1.tolist()[0][0]) * data[i][0] + b.tolist()[0][
            0] - 1 < 0.01 or -0.01 < (w2.tolist()[0][0]) * data[i][1] + (w1.tolist()[0][0]) * data[i][0] + \
                b.tolist()[0][0] + 1 < 0.01:
            class_sv_X.append(data[i][0])
            class_sv_Y.append(data[i][1])
        else:
            class1_X.append(data[i][0])
            class1_Y.append(data[i][1])
    for i in range(20):  # 测试集分类
        if (w2.tolist()[0][0]) * data_test[i][1] + (w1.tolist()[0][0]) * data_test[i][0] + b.tolist()[0][0] > 0:
            class2_1_X.append(data_test[i][0])
            class2_1_Y.append(data_test[i][1])
        else:
            class2_2_X.append(data_test[i][0])
            class2_2_Y.append(data_test[i][1])
    s1 = plt.scatter(class1_X, class1_Y, color='pink')
    s2 = plt.scatter(class_sv_X, class_sv_Y, color='red')
    s3 = plt.scatter(class2_1_X, class2_1_Y, color='blue')
    s4 = plt.scatter(class2_2_X, class2_2_Y, color='green')
    plt.legend((s1, s2, s3, s4), ('train data', 'support vectors', 'class1 of test data', 'class2 of test data'),
               loc='upper left')


if __name__ == '__main__':
    main()
    plt.title("Two Classification Result")
    plt.savefig("picture.png")