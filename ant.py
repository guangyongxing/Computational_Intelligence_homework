import numpy as np
from numpy import nan
import random
import math
class ANT():
    def __init__(self):
        self.pop=20  #初始化蚂蚁个数
        self.M = np.array([[0, 3, 4, nan, nan, nan, nan, nan, nan, nan],  # 有向无环图
                           [nan, 0, nan, 5, 6, nan, nan, nan, nan, nan],
                           [nan, nan, 0, 8, nan, 7, nan, nan, nan, nan],
                           [nan, nan, nan, 0, 3, nan, nan, nan, nan, nan],
                           [nan, nan, nan, nan, 0, nan, 9, 4, nan, nan],
                           [nan, nan, nan, nan, nan, 0, nan, 6, nan, nan],
                           [nan, nan, nan, nan, nan, nan, 0, nan, nan, 2],
                           [nan, nan, nan, nan, nan, nan, nan, 0, 5, nan],
                           [nan, nan, nan, nan, nan, nan, nan, nan, 0, 3],
                           [nan, nan, nan, nan, nan, nan, nan, nan, nan, 0]])
        self.T = np.array([[0, self.pop,self.pop,nan, nan, nan, nan, nan, nan, nan],  #  路径信息素矩阵，初始化为蚂蚁个数
                           [nan, 0, nan,self.pop, self.pop, nan, nan, nan, nan, nan],
                           [nan, nan, 0, self.pop, nan, self.pop, nan, nan, nan, nan],
                           [nan, nan, nan, 0, self.pop, nan, nan, nan, nan, nan],
                           [nan, nan, nan, nan, 0, nan, self.pop, self.pop, nan, nan],
                           [nan, nan, nan, nan, nan, 0, nan, self.pop, nan, nan],
                           [nan, nan, nan, nan, nan, nan, 0, nan, nan,self.pop],
                           [nan, nan, nan, nan, nan, nan, nan, 0, self.pop, nan],
                           [nan, nan, nan, nan, nan, nan, nan, nan, 0,self.pop],
                           [nan, nan, nan, nan, nan, nan, nan, nan, nan, 0]])
        self.ant=np.zeros((self.pop,10))     #构建蚂蚁路径矩阵
        self.r=self.ant.shape[0]         #蚂蚁路径矩阵行数
        self.c = self.ant.shape[1]       #蚂蚁路径矩阵列数
        self.arrival=0                   #到达终点的蚂蚁数量
        self.antW=np.zeros((1,self.pop))  #每只蚂蚁所走路径的权重和
        self.path = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9']
    '为每只蚂蚁选择出发城市，即源点'
    def m1(self):
        for r in range(self.r):
            self.ant[r][0]=1       #所有蚂蚁都是从源点开始
    '为每只蚂蚁进行不同路径到达终点'
    def m2(self):
        for r in range(self.r):
            for c in range(self.c-1,-1,-1): #倒序遍历
                if self.ant[r][9] != 1:  # 该只蚂蚁没有到达最后结点
                    if self.ant[r][c]==1: #第r只蚂蚁，已到达c号结点
                            neweight = []  # 下一步可以走的路径权值
                            nestep=[]      #下一步可以走的结点
                            for m in range(self.M.shape[1]):
                                if (not math.isnan(self.M[c][m])) & (self.M[c][m]!=0):
                                    neweight.append(self.M[c][m])
                                    nestep.append(m)
                            sumT=0 #信息素与路径的相乘的权值和
                            pT=[]  #路径的选择权值比例
                            for i in range(len(nestep)):
                                t=self.T[c][nestep[i]]*neweight[i]
                                sumT=sumT+t
                                pT.append(t)
                            for i in range(len(pT)):
                                pT[i]=pT[i]/sumT  #求出每条路径的权值比例
                            #轮盘赌选择下一个结点
                            selectr=random.random()
                            h=0
                            for i in range(len(pT)):
                                h=h+pT[i]
                                if selectr<=h: #选择第i个可以走的结点
                                    self.ant[r][nestep[i]]=1   #蚂蚁走入下一个结点
                                    self.antW[0][r]=self.antW[0][r]+neweight[i] #保存权重和
                                    break
                            break
                else:
                    self.arrival=self.arrival+1   #到达终点的蚂蚁+1
                    break
    '循环执行，要求所有蚂蚁到达终点'
    def m3(self):
        while self.arrival<self.pop:
            self.m2()
        pass

    '所有蚂蚁到达终点后，开始更新信息素'
    '难点在于如何从蚂蚁的路径矩阵里确定点与点的关系，即两个1之间'
    def m4(self):
        '蒸发'
        for r in range(self.T.shape[0]):
            for c in range(self.T.shape[1]):
                if not math.isnan(self.T[r][c]):
                    self.T[r][c]=self.T[r][c]*0.5 #信息素蒸发50%
        '增加T的变化量'
        for r in range(self.r):
            i=0
            for c in range(self.c):
                if self.ant[r][c]==1:
                    self.T[i][c]=self.T[i][c]+self.antW[0][r]*0.2 #信息素增量：该只蚂蚁总路径的20%
                    i=c

    def run(self):
        self.m1()
        self.m2()
        self.m3()
        self.m4()
        print("蚁群算法")
        print('关键路径长度',self.antW.max())
        max=self.antW.max()
        for i in range(self.antW.shape[1]):
            if self.antW[0][i]==max:
                cpt=self.ant[i]
                break
        pass
        cp=[]
        for i in range(len(cpt)):
            if cpt[i]==1:
                cp.append(self.path[i])
        print("关键路径为",cp)
        print("相关参数：")
        print("蚂蚁个数：",20,' ',"迭代次数：",0)

if __name__=='__main__':
    # for i in range(5-1,-1,-1):
    #     print(i)

    # l=[1,2,3,6]
    # for i in range(len(l)):
    #     l[i]=l[i]/5
    # print(l)

    a2=ANT()
    a2.run()
    pass