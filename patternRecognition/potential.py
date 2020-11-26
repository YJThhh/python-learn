import numpy as np
import matplotlib.pyplot as plt
import math
'''
实现对如图所示六个已知样本的分类器训练
               ^
               |
               X     O
               |
---------------O-----X------------->
               |
               X     O
               |
'''
PointData=np.array([(0,0,1),(2,0,1),(1,1,-1),(1,-1,-1)])
class potentialDistribution(object):
    def __init__(self,PointData):
        self.KProduceList=[]#[x,y],r，KProduceList里放的是
        self.PointData = PointData.tolist()
        num = 0
        iter = 0
        # 加入一个新的点，更新判别式
        while num <= len(PointData):
            KProduceListLen = len(self.KProduceList)
            if iter != len(PointData) - 1:
                iter += 1
            else:
                iter = 0
            self.updateK(PointData[iter])
            if KProduceListLen == len(self.KProduceList):
                num += 1
            else:
                num = 0
    def XXk(self, X, Xk):
        return np.exp(-((X[0] - Xk[0]) ** 2 + (X[1] - Xk[1]) ** 2))
    def Kcalculation(self,X):
        k=0
        for item in self.KProduceList:
            k+=item[1]*self.XXk(item[0],X)
        return k

    def updateK(self,data):
        if data[2] * self.Kcalculation([data[0], data[1]]) > 0:
            return None
        else:
            self.KProduceList.append(([data[0], data[1]], data[2]))

    def outputK(self):
        print("g(x)=", end='')
        for item in self.KProduceList:
            if item[1] > 0:
                print('{}exp{{-((x-({}))^2+(x-({}))^2)}}'.format('+', item[0][0], item[0][1]), end='')
            else:
                print('{}exp{{-((x-({}))^2+(x-({}))^2)}}'.format('-', item[0][0], item[0][1]), end='')
    def outputPlot(self):
        # 作图
        xx = np.arange(-3, 3, 0.1)
        yy = np.arange(-3, 3, 0.1)
        X, Y = np.meshgrid(xx, yy)
        # 定义新的三维坐标轴
        Z = self.Kcalculation([X, Y])
        fig4 = plt.figure()
        ax4 = plt.axes(projection='3d')
        # 作图
        ax4.plot_surface(X, Y, Z, alpha=0.8, cmap='winter')  # 生成表面， alpha 用于控制透明度
        ax4.contour(X, Y, Z, zdir='z', offset=- 3, cmap="rainbow")  # 生成z方向投影，投到x-y平面
        ax4.contour(X, Y, Z, zdir='x', offset=- 6, cmap="rainbow")  # 生成x方向投影，投到y-z平面
        ax4.contour(X, Y, Z, zdir='y', offset=6, cmap="rainbow")  # 生成y方向投影，投到x-z平面
        # 设定显示范
        ax4.set_xlabel('X')
        ax4.set_xlim(- 6, 4)  # 开坐标轴范围显示投影
        ax4.set_ylabel('Y')
        ax4.set_ylim(- 4, 6)
        ax4.set_zlabel('Z')
        ax4.set_zlim(- 3, 3)
        plt.show()
potentialDis1=potentialDistribution(PointData)
potentialDis1.outputK()
potentialDis1.outputPlot()


