# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import xlrd
import xlwt
def f_a_plot(filename):
    workbook = xlrd.open_workbook(filename)
    sheet_names = workbook.sheet_names()
    sheet3 = workbook.sheet_by_name(sheet_names[0])
    q_list = sheet3.col_values(0)[1:]
    Hq_list = sheet3.col_values(1)[1:]
    Hq_diff_list = sheet3.col_values(2)[1:]
    a_list = []
    f_a_list = []
    for i in range(len(q_list)):
        a = Hq_list[i] + q_list[i] * Hq_diff_list[i]
        a_list.append(a)
        f_a = q_list[i] * (a - Hq_list[i]) + 1
        f_a_list.append(f_a)
    plt.figure(figsize = (8,6))
    plt.plot(a_list, f_a_list)
    plt.xlabel('α')
    plt.ylabel('f(α)')
    print("f（a）与a关系图")
    plt.savefig(filename='picture_Tem\\f_a.tiff')# 路径可修改
    excel = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # sheet2 = excel.add_sheet('H(q)_q')
    sheet3 = excel.add_sheet('f(a)_a')
    # sheet4 = excel.add_sheet('')
    # sheet2.write(0, 0, 'q')
    sheet3.write(0, 0, 'a')
    # sheet2.write(0, 1, 'H(q)')
    sheet3.write(0, 1, 'f(a)')
    for i in range(len(a_list)):
        # sheet2.write(i + 1, 0, qList[i])
        # sheet2.write(i + 1, 1, HxyList[i])
        sheet3.write(i + 1, 0, a_list[i])
        sheet3.write(i + 1, 1, f_a_list[i])
    name = filename.split('.')[0].split('\\')[1] + '.xls'
    excel.save('Data_file2\\' + name)
f_a_plot('Data_file\pm_tem_ck.xls')