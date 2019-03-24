#!/usr/bin/python
# -*-coding:utf-8-*-

from openpyxl import load_workbook
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def kmeans_plot():
    loan_data = pd.DataFrame(pd.read_excel('label0.xlsx', header=0))
    # print(loan_data[['sex', 'snlp']])
    loan = np.array(loan_data[['sex', 'snlp']])
    # 设置类别为3
    clf = KMeans(n_clusters=6)
    # 将数据代入到聚类模型中
    clf = clf.fit(loan)
    loan_data['label'] = clf.labels_
    # 提取不同类别的数据
    loan_data0 = loan_data.loc[loan_data["label"] == 0]
    loan_data1 = loan_data.loc[loan_data["label"] == 1]
    loan_data2 = loan_data.loc[loan_data["label"] == 2]
    loan_data3 = loan_data.loc[loan_data["label"] == 3]
    loan_data4 = loan_data.loc[loan_data["label"] == 4]
    loan_data5 = loan_data.loc[loan_data["label"] == 5]
    plt.rc('font', family='STXihei', size=10)
    plt.scatter(loan_data0['sex'], loan_data0['snlp'], 50, color='#99CC01', marker='+', linewidth=2,alpha=0.8)
    plt.scatter(loan_data1['sex'], loan_data1['snlp'], 50, color='#FE0000', marker='+', linewidth=2,alpha=0.8)
    plt.scatter(loan_data2['sex'], loan_data2['snlp'], 50, color='#0000FE', marker='+', linewidth=2,alpha=0.8)
    plt.scatter(loan_data3['sex'], loan_data3['snlp'], 50, color='#D15FEE', marker='+', linewidth=2, alpha=0.8)
    plt.scatter(loan_data4['sex'], loan_data4['snlp'], 50, color='#EE7600', marker='+', linewidth=2, alpha=0.8)
    plt.scatter(loan_data5['sex'], loan_data5['snlp'], 50, color='#FF82AB', marker='+', linewidth=2, alpha=0.8)
    plt.xlabel('sex')
    plt.ylabel('snlp')
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='both', alpha=0.4)
    plt.show()

if __name__ == "__main__":
    kmeans_plot()

