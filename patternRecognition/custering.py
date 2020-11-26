import numpy as np
import matplotlib.pyplot as plt

class Clustering(object):
    def __init__(self,data):
        self.data=data
    def SystematicClustering2D(self,k):
        W = [[self.data[i]] for i in range(1, len(self.data))]
        def dataDis(data1, data2):
            return (data1[0] - data2[0])**2+(data1[1] - data2[1])**2
        def classDis(class1, class2):
            sum = 0
            for i in class1:
                for j in class2:
                    sum += dataDis(i, j) ** 2
            return sum / (len(class1) * len(class2))
        def updateD():
            global D
            D = np.zeros((len(W) - 1, len(W)))
            for i in range(D.shape[0]):
                for j in range(D.shape[1]):
                    D[i][j] = classDis(W[i + 1], W[j])  # (4,5) i=3,j=3
        def findmin():
            min = D[0][0]
            min_i = 0
            min_j = 0
            for i in range(D.shape[0]):
                for j in range(i + 1):
                    if min > D[i][j]:
                        min = D[i][j]
                        min_i, min_j = i, j
            return min, min_i + 1, min_j
        def cluster(classID1, classID2):
            W[classID1] = W[classID1] + W[classID2]
            W.pop(classID2)
        def outputPlot():
            plt.figure(figsize=(8, 8))
            plt.xlim(-10, 10)
            plt.ylim(-10, 10)
            color=[
                'red',
                'black',
                'blue',
                'pink',
                'green',
                'purple',
                'magenta'
            ]

            for idx,item_class in enumerate(W):
                X, Y = [], []
                for item_data in item_class:
                    X.append(item_data[0])
                    Y.append(item_data[1])
                plt.scatter(X, Y, color=color[idx])
            plt.show()
        while len(W) > k:
            updateD()
            _, a, b = findmin()
            cluster(a, b)
        outputPlot()

    def SystematicClustering1D(self,k):
        W=[[self.data[i]] for i in range(1,len(self.data))]
        def dataDis(data1,data2):
            return np.abs(data1-data2)
        def classDis(class1,class2):
            sum=0
            for i in class1:
                for j in class2:
                    sum+=dataDis(i,j)**2
            return sum/(len(class1)*len(class2))
        def updateD():
            global D
            D = np.zeros((len(W)- 1, len(W)))
            for i in range(D.shape[0]):
                for j in range(D.shape[1]):
                    D[i][j]=classDis(W[i+1],W[j])#(4,5) i=3,j=3
        def findmin():
            min=D[0][0]
            min_i=0
            min_j=0
            for i in range(D.shape[0]):
                for j in range(i+1):
                    if min>D[i][j]:
                        min=D[i][j]
                        min_i,min_j=i,j
            return min,min_i+1,min_j
        def cluster(classID1,classID2):
            W[classID1]=W[classID1]+W[classID2]
            W.pop(classID2)
        while len(W)>k:
            updateD()
            _,a,b=findmin()
            cluster(a,b)
if __name__ == '__main__':#满足 脚本直接执行
    '''
    分解聚类算法设计
    根据样本进行聚类分析，以达到要求的类数或者聚类效果
    代码实现(python版）
    '''
    # 读取SampleNum 个样本
    ClassNum = 2  # 期望的分类数
    SampleNum = 21  # 样本数
    PointData = np.array([([SampleNum, 1]), ([0, 6]), ([0, 5]), ([2, 5]),
                          ([2, 3]), ([4, 4]), ([4, 3]),
                          ([5, 1]), ([6, 2]), ([6, 1]),
                          ([7, 0]), ([-4, 3]), ([-2, 2]),
                          ([-3, 2]), ([-3, 0]), ([-5, 2]),
                          ([1, 1]), ([0, -1]), ([0, -2]),
                          ([-1, -1]), ([-1, -3]), ([-3, -5])])
    print('现在的样本为\n{}'.format(PointData[range(1, SampleNum + 1)]))
    Clustering1=Clustering(PointData)
    Clustering1.SystematicClustering2D(7)
