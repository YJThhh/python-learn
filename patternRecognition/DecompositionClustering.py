import numpy as np
import matplotlib.pyplot as plt

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

class DecompositionClustering(object):
    def __init__(self, data):
        self.data = data
        self.G1, self.G2 = [item for item in PointData[range(1, self.data.__len__())]], []
    def MeanVariance(self,g1,g2):
        N1, N2 = g1.__len__(), g2.__len__()
        N = g1.__len__() + g2.__len__()
        return ((N1 * N2) / N) * (
            np.dot(np.mean(g1) - np.mean(g2), np.transpose(np.mean(g1) - np.mean(g2))))
    def calculateE(self):
        E = []
        for i,item in enumerate(self.G1):
            g1, g2 = self.G1.copy(), self.G2.copy()
            g2.append(item)
            g1.pop(i)
            E.append((i,self.MeanVariance(g1,g2)))
        E.sort(key=lambda x:x[1])
        return E[-1]
    def G(self):
        E=0
        while E<self.calculateE()[1]:
            E=self.calculateE()[1]
            self.G2.append(self.G1[self.calculateE()[0]])
            self.G1.pop(self.calculateE()[0])
        aaa=0




decompositionClustering1=DecompositionClustering(PointData)


decompositionClustering1.G()
