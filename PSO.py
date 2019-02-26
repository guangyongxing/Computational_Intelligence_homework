# coding: utf-8
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
sns.set_style("whitegrid")
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

"""
   参数表
   w：惯量权重，0.5
   c1,c2：加速系数，2.0
   r1,r2：[0，1]区间随机数
   pre：模型结果向量，这里假设只有两个模型
   X：融合系数，[0,1]，即粒子位置
   sum：真实label之和
   gbest：全局最优位置向量，引导收敛
   pbest：个体最优位置向量
   f1_list：粒子的最佳函数评估结果
   f2_list：粒子的函数评估结果
"""
# '设定随机种子，每次生成一样随机数'
# random.seed(10)

'随机生成[0,1]之间的随机数'
# print(random.random())
class PSO:
    def __init__(self):
        self.pop=10000
        self.w = 0.5
        self.c1 = 2.0
        self.c2 = 2.0
        self.pre=np.array([350, 328])
        self.sum=311
        self.v=np.zeros((self.pop,2))
        self.X=np.zeros((self.pop,2))
        self.pbest=self.X  #个体经历的最佳位置
        self.gbest = np.zeros((1,2))  # 全局最佳位置
        self.f1_list=[]
        self.f2_list=[]
        self.r = self.X.shape[0]
        self.c = self.X.shape[1]
        self.gbest_hist=[]
        for i in range(self.r):
            for j in range(self.c):
                self.X[i][j]=random.random()
                self.v[i][j]=random.random()

    pass

    def fun(self,X):
        '计算评估函数'
        f_list=[]
        for i in range(self.pop):
            f_list.append(abs(self.pre.dot(X[i])-self.sum))
        return f_list

    def m1(self):
        min=65535
        self.f1_list=self.fun(self.X)
        for i in range(len(self.f1_list)):
            if self.f1_list[i]<min:   #寻找最小值
                min=self.f1_list[i]
                k=i      #记录最佳下标
        self.gbest=self.pbest[k]
        pass

    def m2(self):
        '粒子速度和位置更新'
        for i in range(self.r):
            vtmp1=[]
            for j in range(self.c):
                r1=random.random()
                r2=random.random()
                vtmp2=self.w*self.v[i][j]+\
                     self.c1*r1*(self.pbest[i][j]-self.X[i][j])+\
                     self.c2*r2*(self.gbest[j]-self.X[i][j])
                vtmp1.append(vtmp2)
            self.X[i]=self.X[i]+np.array(vtmp1)

        '之后再加上合法性调整'
        '大于1的位置调整成1'
        # for i in range(self.r):
        #     for j in range(self.c):
        #         if self.X[i][j]>1:
        #             self.X[i][j]=1


    def m3(self):
        self.f2_list=self.fun(self.X)
        for i in range(self.r):
            if self.f2_list[i]<self.f1_list[i]:
                self.f1_list[i]=self.f2_list[i]
                self.pbest[i]=self.X[i]
        min=65535
        for i in range(self.r):
            if self.f1_list[i]<min:
                min=self.f1_list[i]
                k=i
        self.gbest=self.pbest[k]
        pass

    def run(self):
        print("PSO算法开始运行：")
        self.m1()
        for i in range(100):
            self.m2()
            self.m3()
            print(self.gbest)
            t=abs(self.pre.dot(self.gbest)-self.sum)
            self.gbest_hist.append(t)
        plt.plot(self.gbest_hist)
        plt.title("迭代次数与最佳评估函数值的关系")
        plt.xlabel("迭代次数")
        plt.ylabel("最佳评估函数值")
        plt.show()
        pass

if __name__ == "__main__":
    pso=PSO()
    pso.run()

    pass
