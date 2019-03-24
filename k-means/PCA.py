#!/usr/bin/python
# -*-coding:utf-8-*-
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import math
def PCA_main():
    loan_data = pd.DataFrame(pd.read_excel('data.xlsx', header=0))
    # 设置要进行聚类的字段
    loan = np.array(loan_data[['x', 'y','new_snlp']])
    #print(loan)
    pca = PCA(n_components=2)  # 降到2维
    pca.fit(loan)  # 训练
    new = pca.fit_transform(loan)  # 降维后的数据
    loan_data["new_x"] = [i[0] for i in new]
    loan_data["new_y"] = [i[1] for i in new]
    return loan_data
def plot(loan_data):
    loan = np.array(loan_data[['new_x', 'new_y']])
    loan_data_list = np.array(loan_data)
    clf = KMeans(n_clusters=8)
    clf = clf.fit(loan)
    loan_data['label'] = clf.labels_
    centroids = clf.cluster_centers_  # 获取聚类中心
    centroids = np.array(centroids)
    x_p = []
    y_p = []
    for item in centroids:
        min =100
        x = item[0]
        y = item[1]
        for item1 in loan_data_list:
            new_x = item1[7]
            new_y = item1[7]
            if math.sqrt((new_x-x)*(new_x-x)+(new_y-y)*(new_y-y)) < min:
                real_x = item1[2]
                real_y = item1[3]
                min = math.sqrt((new_x-x)*(new_x-x)+(new_y-y)*(new_y-y))
        x_p.append(real_x)
        y_p.append(real_y)
    loan_data0 = loan_data.loc[loan_data["label"] == 0]
    loan_data1 = loan_data.loc[loan_data["label"] == 1]
    loan_data2 = loan_data.loc[loan_data["label"] == 2]
    loan_data3 = loan_data.loc[loan_data["label"] == 3]
    loan_data4 = loan_data.loc[loan_data["label"] == 4]
    loan_data5 = loan_data.loc[loan_data["label"] == 5]
    loan_data6 = loan_data.loc[loan_data["label"] == 6]
    loan_data7 = loan_data.loc[loan_data["label"] == 7]
    plt.rc('font', family='STXihei', size=10)
    #plt.scatter(loan_data0['x'], loan_data0['y'], 50, color='#99CC01', marker='+', linewidth=2, alpha=0.8)
    #plt.scatter(loan_data1['x'], loan_data1['y'], 50, color='#FE0000', marker='+', linewidth=2, alpha=0.8)
    #plt.scatter(loan_data2['x'], loan_data2['y'], 50, color='#0000FE', marker='+', linewidth=2, alpha=0.8)
    #plt.scatter(loan_data3['x'], loan_data3['y'], 50, color='#D15FEE', marker='+', linewidth=2, alpha=0.8)
    #plt.scatter(loan_data4['x'], loan_data4['y'], 50, color='#EE7600', marker='+', linewidth=2, alpha=0.8)
    #plt.scatter(loan_data5['x'], loan_data5['y'], 50, color='#FF82AB', marker='+', linewidth=2, alpha=0.8)
    #plt.scatter(loan_data6['x'], loan_data6['y'], 50, color='#B0E2FF', marker='+', linewidth=2, alpha=0.8)
    plt.scatter(loan_data7['x'], loan_data7['y'], 50, color='#62c0c0', marker='+', linewidth=2, alpha=0.8)

    plt.scatter(x_p[7], y_p[7], 50, color='black', marker='*', linewidth=3, alpha=0.8)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='both', alpha=0.4)
    plt.show()
    return loan_data
plot(PCA_main())