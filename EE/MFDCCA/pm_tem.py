# -*- coding: utf-8 -*-
# coding: utf-8

# MF-DCCA coder


from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import math
import xlrd
import numpy as np

file_name = 'pm_tem_ck.xlsx'
work_sheet = xlrd.open_workbook(file_name)
sheet_names = work_sheet.sheet_names()
sheet1 = work_sheet.sheet_by_name(sheet_names[0])
# 读取两列数据x,y
X = sheet1.col_values(0)[1:]
M = len(X)
X = X + X
print(len(X))
Y = sheet1.col_values(1)[1:]
Y = Y + Y
hua_Hxy = []

for o in range(0, len(X) - M):
    x = X[o:M + o]
    y = Y[o:M + o]
    # 零均值归一化
    # def zeroMeanNormalization(x):
    #     return (x - x.mean())/x.std()

    # 零均值归一化
    # x = zeroMeanNormalization(x)
    # y = zeroMeanNormalization(y)

    # 线性归一化
    # def linerNormalization(x):
    #     return (x - x.min())/(x.max() - x.min())

    # 线性归一化
    # x = linerNormalization(x)
    # y = linerNormalization(y)

    N = len(x)
    # print(N)
    axi = []
    for i in range(N):
        axi.append(i)

    # 求平均值函数
    def mean(list):
        sum = 0
        for i in range(len(list)):
            sum += list[i]
        return sum / len(list)


    xAverageValue = mean(x)
    yAverageValue = mean(y)
    # print("aAverage:", xAverageValue, "\nyAverageValue:", yAverageValue)
    # 构造新的时间序列
    xNewSequence = []
    yNewSequence = []

    for i in range(N):
        xTemp = 0
        yTemp = 0
        j = 0
        while j < i:
            xTemp += x[j] - xAverageValue
            yTemp += y[j] - yAverageValue
            j += 1
        xNewSequence.append(xTemp)
        yNewSequence.append(yTemp)

    # 对xNewSequence、yNewSequence求逆序 inverse sequence
    xNewSequenceInverse = []
    yNewSequenceInverse = []
    for i in range(N):
        xNewSequenceInverse.append(xNewSequence[N - i - 1])
        yNewSequenceInverse.append(yNewSequence[N - i - 1])

    # 最小二乘拟合函数
    # 构造拟合函数
    def func(p, x):
        k, b, c = p
        return k * x ** 2 + b * x + c


    # 定义误差函数
    def error(p, x, y):
        return func(p, x) - y  # x、y都是列表，故返回值也是个列表


    # 计算局部协方差,其中i表示第几个小区间,s表示小区间长度
    def calculateLocalCovariance(data1, data2, s):
        sNumber = int(len(data1) / s) * s
        #     print(sNumber)
        xTemp = []
        yTemp = []
        for i in range(0, sNumber, s):
            xTemp.append(data1[i:i + s])
            yTemp.append(data2[i:i + s])
        allSum = []
        for i in range(len(xTemp)):  # 依次取出Ns个小区间
            j = 0
            localCovarianceSum = 0
            x1 = np.array(range(1, s + 1))
            data1TempList = xTemp[i]
            data2TempList = yTemp[i]
            p0 = [5, 2, 4]
            # 最小二乘拟合系数
            data1Paratmer = leastsq(error, p0, args=(x1, data1TempList))
            data2Paratmer = leastsq(error, p0, args=(x1, data2TempList))
            data1_a, data1_b, data1_c = data1Paratmer[0]
            data2_a, data2_b, data2_c = data2Paratmer[0]
            while j < s:
                # 二次函数拟合计算
                # tempSum = abs(data1TempList[j]-(data1_a*data1TempList[j]**2 + data1_b*data1TempList[j] + data1_c))* \
                # abs(data2TempList[j]-(data2_a*data2TempList[j]**2 + data2_b*data2TempList[j] + data2_c))
                # 一次函数拟合计算
                tempSum = abs(data1TempList[j] - (data1_a * x1[j] ** 2 + data1_b * x1[j] + data1_c)) * abs(
                    data2TempList[j] - (data2_a * x1[j] ** 2 + data2_b * x1[j] + data2_c))
                localCovarianceSum += tempSum
                j += 1
            allSum.append(localCovarianceSum / s)
        return allSum


    # In[22]:

    # 对所有子区间的局部协方差取均值，得到q阶波动函数
    def qOrderWaveFunction(Q, data):
        N = len(data)
        f_q_sum = 0
        if Q != 0:
            for i in range(N):
                f_q_sum += math.pow(data[i], Q / 2)
            return math.pow((f_q_sum / N), 1 / Q)
        else:
            for i in range(N):
                f_q_sum += math.log(data[i])
            f_q_sum = math.exp(f_q_sum / (2 * N))
            return f_q_sum


    # 最小二乘拟合函数
    # 构造拟合函数
    def func1(p, x):
        k, b = p
        return k * x + b


    # 定义误差函数
    def error1(p, x, y):
        return func1(p, x) - y  # x、y都是列表，故返回值也是个列表


    q = 2
    while q <= 2:
        sList = []
        FqList = []
        # qList.append(q)
        for n in range(8, int(len(x) / 4)):
            sList.append(n)
            f1_LocalCovariance = calculateLocalCovariance(xNewSequence, yNewSequence, n)
            f2_LocalCovariance = calculateLocalCovariance(xNewSequenceInverse, yNewSequenceInverse, n)

            # 2Ns的局部协方差列表合并
            sumLocalCovariance = f1_LocalCovariance + f2_LocalCovariance
            FqList.append(qOrderWaveFunction(q, sumLocalCovariance))
        log_sList = np.log10(sList)
        log_FqList = np.log10(FqList)

        log_p0 = [5, 2]
        FqListParatmer = leastsq(error1, log_p0, args=(log_sList, log_FqList))
        Hxy, _ = FqListParatmer[0]
        print(Hxy)
        hua_Hxy.append(Hxy)
        q += 0.5
k_list = [k + 1 for k in range(len(hua_Hxy))]
plt.figure(figsize=(8, 6))
plt.ylabel('Hxy')
plt.plot(k_list, hua_Hxy, 'k',label='pm_tem', linewidth='1')
plt.legend()
name = file_name.split('_')
names = name[0] + '_' + name[1] + '.tiff'

plt.savefig(filename=names)
plt.show()

# -*- coding: utf-8 -*-
