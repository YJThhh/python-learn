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

    def DecompositionClustering(self):
        G1, G2 = [item for item in PointData[range(1, self.data.__len__())]], []
        def MeanVariance(g1, g2):
            N1, N2 = g1.__len__(), g2.__len__()
            N = g1.__len__() + g2.__len__()
            return ((N1 * N2) / N) * (
                np.dot(np.mean(g1,axis=0) - np.mean(g2,axis=0), np.transpose(np.mean(g1,axis=0) - np.mean(g2,axis=0))))
        def calculateE(G1,G2):
            E = []
            for i, item in enumerate(G1):
                import copy
                g1, g2 = copy.deepcopy(G1), copy.deepcopy(G2)
                g2.append(item)
                g1.pop(i)
                E.append((i, MeanVariance(g1, g2)))
            E.sort(key=lambda x: x[1])
            return E[-1]

        def outputPlot():
            plt.figure(figsize=(8, 8))
            plt.xlim(-10, 10)
            plt.ylim(-10, 10)
            color = [
                'red',
                'black',
                'blue',
                'pink',
                'green',
                'purple',
                'magenta'
            ]

            for idx, item_class in enumerate([G1,G2]):
                X, Y = [], []
                for item_data in item_class:
                    X.append(item_data[0])
                    Y.append(item_data[1])
                plt.scatter(X, Y, color=color[idx])
            plt.show()

        E = 0
        while E <= calculateE(G1,G2)[1]:
            E = calculateE(G1, G2)[1]
            G2.append(G1[calculateE(G1,G2)[0]])
            G1.pop(calculateE(G1,G2)[0])

        outputPlot()

    def Kmeans(self):

        def compute_euclidean_distance(point, centroid):
            return np.sqrt(np.sum((point - centroid) ** 2))

        def assign_label_cluster(distance, data_point, centroids):
            index_of_minimum = min(distance, key=distance.get)
            return [index_of_minimum, data_point, centroids[index_of_minimum]]

        def compute_new_centroids(cluster_label, centroids):
            return np.array(cluster_label + centroids) / 2

        def iterate_k_means(data_points, centroids, total_iteration):
            label = []
            cluster_label = []
            total_points = len(data_points)
            k = len(centroids)

            for iteration in range(0, total_iteration):
                for index_point in range(0, total_points):
                    distance = {}
                    for index_centroid in range(0, k):
                        distance[index_centroid] = compute_euclidean_distance(data_points[index_point],
                                                                              centroids[index_centroid])
                    label = assign_label_cluster(distance, data_points[index_point], centroids)
                    centroids[label[0]] = compute_new_centroids(label[1], centroids[label[0]])

                    if iteration == (total_iteration - 1):
                        cluster_label.append(label)

            return [cluster_label, centroids]

        def print_label_data(result):
            print("Result of k-Means Clustering: \n")
            for data in result[0]:
                print("data point: {}".format(data[1]))
                print("cluster number: {} \n".format(data[0]))
            print("Last centroids position: \n {}".format(result[1]))

        def outputPlot(plot):

            plt.figure(figsize=(8, 8))
            plt.xlim(-10, 10)
            plt.ylim(-10, 10)
            color = [
                'red',
                'black',
                'blue',
                'pink',
                'green',
                'purple',
                'magenta'
            ]

            for idx, item_class in enumerate(plot):
                X, Y = [], []
                for item_data in item_class:
                    X.append(item_data[0])
                    Y.append(item_data[1])
                plt.scatter(X, Y, color=color[idx])
            plt.show()

        center=self.data[10:12]
        total_iteration = 1000
        [cluster_label, new_centroids] = iterate_k_means(self.data[1:], center, total_iteration)
        print_label_data([cluster_label, new_centroids])
        plot=[]
        for i in range(center.shape[0]):
            lista=[]
            for item in cluster_label:
                if item[0]==i:
                    lista.append(item[1].tolist())
            plot.append(lista)
        outputPlot(plot)


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
    #print('现在的样本为\n{}'.format(PointData[range(1, SampleNum + 1)]))
    Clustering1=Clustering(PointData)
    #Clustering1.SystematicClustering2D(2)
    Clustering1.Kmeans()

