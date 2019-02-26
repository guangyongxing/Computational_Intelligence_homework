import numpy as np
from numpy import nan
import random
import math
class GA1:
    def __init__(self):
        self.M=np.array([[0,3,4,nan,nan,nan,nan,nan,nan,nan], #有向无环图
                    [nan,0,nan,5,6,nan,nan,nan,nan,nan],
                    [nan,nan,0,8,nan,7,nan,nan,nan,nan],
                    [nan,nan,nan,0,3,nan,nan,nan,nan,nan],
                    [nan,nan,nan,nan,0,nan,9,4,nan,nan],
                    [nan,nan,nan,nan,nan,0,nan,6,nan,nan],
                    [nan,nan,nan,nan,nan,nan,0,nan,nan,2],
                    [nan,nan,nan,nan,nan,nan,nan,0,5,nan],
                    [nan,nan,nan,nan,nan,nan,nan,nan,0,3],
                    [nan,nan,nan,nan,nan,nan,nan,nan,nan,0]])
        self.pop=100 #种群规模
        self.C=np.zeros((self.pop,10)) #种群染色体矩阵
        self.r=self.C.shape[0]         #种群染色体矩阵行数
        self.c=self.C.shape[1]         #种群染色体矩阵列数
        self.E=np.zeros((1,self.pop)) #存储个体适应值
        self.path=['V0','V1','V2','V3','V4','V5','V6','V7','V8','V9']
        '种群的第一个基因与最后一个基因均为1,其余自动生成，是0或1'
        for i in range(self.r): #遍历行
            for j in range(self.c): #遍历列
                if (j==0)|(j==9):
                    self.C[i][j]=1
                else:
                    self.C[i][j]=np.random.randint(0,2)

    '计算适应值评价，顺带检查基因顺序合法性，不合法的会被修改'
    def m2(self):
        for r in range(self.r):#遍历每一条染色体
            sum=0
            i=0
            for c in range(1,self.c): #从1开始到最大,因为第一个基因都是1
                if self.C[r][c]==1:
                    if self.M[i][c]!=nan:
                        sum=sum+self.M[i][c]
                        i=c
                    else:
                        self.C[r][c]=0 #不合法的基因会被置零
            self.E[0][r]=sum #存储每条染色体的适应值
    '选择'
    def m3(self):
        eval_sum=self.E.sum()
        eval_p=np.zeros((1,self.pop)) #存储每个染色体的适应值占比
        select=np.zeros((1,self.pop)) #记录被选中的染色体
        for r in range(self.r):  #计算每个染色体适应值的占比
            eval_p[0][r]=self.E[0][r]/eval_sum
        for r in range(self.r): #轮盘赌算法选择染色体
            m=0
            p=random.random()
            for i in range(self.r):
                m=m+eval_p[0][i]
                if p<=m:
                    select[0][r]=i
                    break
        Ccopy=self.C       #复制一份种群基因
        for r in range(select.shape[1]):
            self.C[r]=Ccopy[select[0][r]] #产生新的种群
    '交配'
    def m4(self):
        p=0.88 #设交配概率为0.88
        copulate=np.zeros((1,self.r)) #确定参与交配的染色体，参与标1，否则标0
        for r in range(self.r):
            copup=random.random()     #生成交配概率
            if copup<p:
                copulate[0][r]=1 #参与交配
            else:
                copulate[0][r]=0 #不参与交配

        for r in range(self.r): #开始交配
            i=0
            j=0
            if copulate[0][r]==1:
                i=r            #选出一个参与交配的染色体
                copulate[0][r]=0
            for h in range(i+1,self.r):
                if copulate[0][h]==1:
                    j=h        #选出第二个参与交配的染色体
                    copulate[0][h]=0
            if j>i:
                coplace=random.randint(1,9) #生成交配位，随机整数 0号9号基因不参与交配
                for e in range(coplace,self.c):
                    t=self.C[i][e]
                    self.C[i][e]=self.C[j][e]
                    self.C[j][e]=t
    '变异'
    def m5(self):
        p=0.1 #设变异概率为0.1
        for r in range(self.r):
            for c in range(1,self.c-1): #0号与9号基因不参与变异
                varp=random.random()
                if varp<p: #小于变异概率,进行变异
                    if self.C[r][c]==1: #若为1，则变为0
                        self.C[r][c]=0
                    else:               #若为0，则变为1
                        self.C[r][c]=1
    '评价Best'
    def m6(self):
        for r in range(self.r):#遍历每一条染色体
            sum=0
            i=0
            for c in range(self.c): #从1开始到最大,因为第一个基因都是1
                if self.C[r][c]==1:
                    if math.isnan(self.M[i][c]):
                        self.C[r][c] = 0  # 不合法的基因会被置零
                        sum = 0
                        break
                    else:
                        sum = sum + self.M[i][c]
                        i = c
            self.E[0][r]=sum #存储每条染色体的适应值
        return self.E.max()

    def run(self):
        self.m2()
        best=0
        for i in range(1000):
            self.m3()
            self.m4()
            self.m5()
            bt=self.m6()
            # print(bt)
            if bt>=best:
                best=bt
        cpt=[]
        for i in range(self.E.shape[1]):
            if self.E[0][i]==best:
                cpt=self.C[i]
                break
        cp=[]
        for i in range(len(cpt)):
            if cpt[i]==1:
                cp.append(self.path[i])
        print("遗传算法")
        print("关键路径长度为",best)
        print("关键路径为",cp)
        print("相关参数:")
        print("种群规模：",100,' ',"迭代次数：",1000)




if __name__=='__main__':

    # m=np.array([[1,2,3,4,nan]])
    # print(math.isnan(m[0][4]))

    # r=random.random() #生成0，1之间随机数
    # print(r)

    # l=np.zeros((1,10))
    # l[0][3]=1
    # print(l[0][3])

    # r=random.randint(1,10)
    # print(r)

    a1=GA1()
    a1.run()