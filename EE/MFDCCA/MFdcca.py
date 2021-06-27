# -*- coding: utf-8 -*-
# coding: utf-8

# MF-DCCA coder


from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import math
import xlrd
import xlwt
import numpy as np

file_name = 'pm_tem_ck.xlsx'
work_sheet = xlrd.open_workbook(file_name)
sheet_names = work_sheet.sheet_names()
sheet1 = work_sheet.sheet_by_name(sheet_names[0])
# 读取两列数据x,y
x = sheet1.col_values(0)[1:]
y = sheet1.col_values(1)[1:]

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
print(N)
axi = []
for i in range(N):
    axi.append(i)

# 绘制原始数据趋势图
plt.figure(figsize=(8, 6))
plt.plot(axi, x, color="red", label="Polar Surface Area", linewidth=2)
plt.plot(axi, y, color="green", label="measured log solubility in mols per litre", linewidth=2)
# plt.scatter(x, y ,color="green",label="中证500",linewidth=2)
plt.legend()  # 绘制图例
plt.show()


# 求平均值函数
def mean(list):
    sum = 0
    for i in range(len(list)):
        sum += list[i]
    return sum / len(list)


xAverageValue = mean(x)
yAverageValue = mean(y)
print("aAverage:", xAverageValue, "\nyAverageValue:", yAverageValue)
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

print("xNewSequence:", len(xNewSequence), "\nyNewSequence:", len(yNewSequence))

# 绘制新序列数据趋势图
plt.figure(figsize=(8, 6))
plt.plot(axi, xNewSequence, color="red", label="Number of Rings", linewidth=2)
plt.plot(axi, yNewSequence, color="green", label="measured log solubility in mols per litre", linewidth=2)
plt.legend()  # 绘制图例
plt.show()

# 对xNewSequence、yNewSequence求逆序 inverse sequence
xNewSequenceInverse = []
yNewSequenceInverse = []
for i in range(N):
    xNewSequenceInverse.append(xNewSequence[N - i - 1])
    yNewSequenceInverse.append(yNewSequence[N - i - 1])
print("xNewSequenceInverse:", len(xNewSequenceInverse), "\nyNewSequenceInverse:", len(yNewSequenceInverse))

# 绘制新序列数据逆序趋势图
plt.figure(figsize=(8, 6))
plt.plot(axi, xNewSequenceInverse, color="red", label="Number of Rings", linewidth=2)
plt.plot(axi, yNewSequenceInverse, color="green", label="measured log solubility in mols per litre", linewidth=2)
plt.legend()  # 绘制图例
plt.show()


# In[20]:

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


# top_q和q之间的关系图
# top_q = q*Hxy(q)-1
plt.figure(figsize=(8, 6))
plt.xlabel('log(s)')
plt.ylabel('logFq(s)')

qList = []
HxyList = []
top_qList = []
q = -10
# for q in range(-10, 11, 0.5):
while q <= 10:
    sList = []
    FqList = []
    qList.append(q)
    for n in range(8, int(len(x) / 4)):
        sList.append(n)
        f1_LocalCovariance = calculateLocalCovariance(xNewSequence, yNewSequence, n)
        f2_LocalCovariance = calculateLocalCovariance(xNewSequenceInverse, yNewSequenceInverse, n)

        # 2Ns的局部协方差列表合并
        sumLocalCovariance = f1_LocalCovariance + f2_LocalCovariance
        FqList.append(qOrderWaveFunction(q, sumLocalCovariance))
    log_sList = np.log10(sList)
    log_FqList = np.log10(FqList)
    #     print("log_sList:",len(log_sList),"log_FqList:",len(log_FqList))
    plt.plot(log_sList, log_FqList, linewidth=1)

    log_p0 = [5, 2]
    FqListParatmer = leastsq(error1, log_p0, args=(log_sList, log_FqList))
    Hxy, _ = FqListParatmer[0]
    if q == 2:
        print("Hxy:", Hxy)
    HxyList.append(Hxy)
    q += 0.5

print("log(s)与logFq(s)对数双曲线图")
plt.savefig(filename='picture_Tem\logFq_logs.tiff')
# plt.show()

for i in range(len(qList)):
    top_q = qList[i] * HxyList[i] - 1
    top_qList.append(top_q)

# 绘制Tq和q图
plt.figure(figsize=(8, 6))
plt.xlabel('q')
plt.ylabel('T(q)')
plt.plot(qList, top_qList)
print("τ（q）与q关系图")
plt.savefig(filename='picture_Tem\T_q.tiff')
# plt.show()
# 绘制Hq和q图
print(HxyList)
plt.figure(figsize=(8, 6))
plt.xlabel('q')
plt.ylabel('Hxy(q)')
plt.plot(qList, HxyList)
print("Hxy（q）与q关系图")
plt.savefig(filename='picture_Tem\Hxy_q.tiff')


# plt.show()
# 将Hq和q写入excel
excel = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet2 = excel.add_sheet('H(q)_q')
sheet3 = excel.add_sheet('T(q)_q')
# sheet4 = excel.add_sheet('')
sheet2.write(0, 0, 'q')
sheet3.write(0, 0, 'q')
sheet2.write(0, 1, 'H(q)')
sheet3.write(0, 1, 'T(q)')
for i in range(len(HxyList)):
    sheet2.write(i + 1, 0, qList[i])
    sheet2.write(i + 1, 1, HxyList[i])
    sheet3.write(i + 1, 0, qList[i])
    sheet3.write(i + 1, 1, top_qList[i])
name = file_name.split('.')[0] + '.xls'
excel.save('Data_file\\' + name)