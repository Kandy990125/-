#!/usr/bin/python
# -*-coding:utf-8-*-

from openpyxl import load_workbook
import sqlite3
import openpyxl
import pandas as pd
import seaborn as sns  #用于绘制热图的工具包
from scipy.cluster import hierarchy  #用于进行层次聚类，话层次聚类图的工具包
from scipy import cluster
import matplotlib.pyplot as plt
from sklearn import decomposition as skldec #用于主成分分析降维的包
if __name__=="__main__":
    # 读取用于聚类的数据，并创建数据表
    loan_data = pd.DataFrame(pd.read_excel('data1.xlsx', header=0))
    # 查看数据表
    loan_data.head()