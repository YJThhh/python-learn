import numpy as np
class Path(object):
    def __init__(self,m,n,weight):
        self.m,self.n,self.weight=m,n,weight
class Graph(object):
    def __init__(self, vertexList, vertexMatrix):
        self.vertexList=vertexList
        self.vertexMatrix=vertexMatrix
        #判断输入是否合法：输入点的数目和矩阵行列长度是否一样
        if len(vertexList)!=vertexMatrix.shape[0] or vertexMatrix.shape[0]!=vertexMatrix.shape[1]:
            raise Exception("异常!")

    def prim(self):#生成最小树的普里姆算法
        # Vnew已经连通的点；V还未连通的点；Pnew每个点可使用的边；P中为使用过的边
        Vnew, V, Pnew, P = [], self.vertexList.copy(), [], []
        def NotExist(path,pathList):#判断是否存在重合边，如果两条边的头点和尾点都相同或者两条边都头点和尾点相同以及尾点和头点相同，则重合
            for item in pathList:
                if (path.m==item.m and path.n==item.n) or  (path.n==item.m and path.m==item.n):
                    return False
            return True
        def vertexAdd(vertex):#Vnew中添加连通过的点，并把此点从V中移除
            Vnew.append(vertex)
            V.remove(vertex)
        def pathAdd(vertex):
            for i in range(len(self.vertexList)):
                weight=self.vertexMatrix[self.vertexList.index(vertex),i]
                path=Path(vertex,self.vertexList[i],weight)
                if weight!=0 and NotExist(path,Pnew):#判断点与点之间点权重是否为0或者是否存在重合边，不为0、不重合则加入Pnew中
                    Pnew.append(path)
        def findMinPath(i):
            Pnew.sort(key=lambda x: x.weight)#按照权重对Pnew从小到大排序
            return Pnew[i]

        for i in range(len(self.vertexList)-1):
            #先取第一个点，再判断其他点的边和路径
            if i==0:
                vertexAdd(self.vertexList[0])
                pathAdd(self.vertexList[0])
                minPath=findMinPath(0)
            else:
                P.append(minPath)
                vertexAdd(minPath.n)
                pathAdd(minPath.n)
                minPath=findMinPath(0)
                j=1
                while minPath.n not in V :#可用否？看最小边连接的点是否已经使用过，如果用过，则继续寻找可用路径
                    minPath=findMinPath(j)
                    j+=1#继续找
        P.append(minPath)
        vertexAdd(minPath.n)
        print('连接顺序为：')
        for item in P:
            print("{}-->{},权重：{}".format(item.m,item.n,item.weight))

        #add x0 to Vnew and remove form V
        # add x0's path to Pnew
        #findMinpath in Pnew
        #add minPath(x0,X) to P

        # add X path to Pnew
        #findMinpath in Pnew
        #add minPath(X,Y) to P
        #……
if __name__ == '__main__':
    g1=Graph(['a','b','c','d','e','f','g'],np.array([[0,19,0,0,14,0,18],
                                                     [19,0,5,7,12,0,0],
                                                     [0,5,0,3,0,0,0],
                                                     [0,7,3,0,8,21,0],
                                                     [14,12,0,8,0,0,16],
                                                     [0,0,0,21,0,0,27],
                                                     [18,0,0,0,16,27,0]]))
    g1.prim()

