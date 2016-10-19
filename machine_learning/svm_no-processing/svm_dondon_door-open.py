# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:28:52 2016

@author: student
"""


import pandas as pd
import numpy as np
#from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn import svm
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import os



################################################################################
#                               データの前処理
################################################################################

# データ取得
open1 = pd.read_csv('C:/Users/student/Documents/door-open/open1.csv')
open2 = pd.read_csv('C:/Users/student/Documents/door-open/open2.csv')
open3 = pd.read_csv('C:/Users/student/Documents/door-open/open3.csv')
open4 = pd.read_csv('C:/Users/student/Documents/door-open/open4.csv')

dondon1 = pd.read_csv('C:/Users/student/Documents/dondon/dondon1.csv')
dondon2 = pd.read_csv('C:/Users/student/Documents/dondon/dondon2.csv')
dondon3 = pd.read_csv('C:/Users/student/Documents/dondon/dondon3.csv')
dondon4 = pd.read_csv('C:/Users/student/Documents/dondon/dondon4.csv')


# 列名追加
open1.columns = ['index','x', 'y', 'z']
open2.columns = ['index','x', 'y', 'z']
open3.columns = ['index','x', 'y', 'z']
open4.columns = ['index','x', 'y', 'z']

dondon1.columns = ['index','x', 'y', 'z']
dondon2.columns = ['index','x', 'y', 'z']
dondon3.columns = ['index','x', 'y', 'z']
dondon4.columns = ['index','x', 'y', 'z']

# 列の削除
open1 = open1.drop('index', axis=1)
open2 = open2.drop('index', axis=1)
open3 = open3.drop('index', axis=1)
open4 = open4.drop('index', axis=1)

dondon1 = dondon1.drop('index', axis=1)
dondon2 = dondon2.drop('index', axis=1)
dondon3 = dondon3.drop('index', axis=1)
dondon4 = dondon4.drop('index', axis=1)

# データの長さを求める
open1_length = len(open1)
open2_length = len(open2)
open3_length = len(open3)
open4_length = len(open4)

dondon1_length = len(dondon1)
dondon2_length = len(dondon2)
dondon3_length = len(dondon3)
dondon4_length = len(dondon4)

################################################################################
#                               5秒間を切り出す
################################################################################
split_second = 5000
start = 0
stop = split_second
roop_count = 1

# 商を求める
open1_quotient = int(open1_length / split_second)
open2_quotient = int(open2_length / split_second)
open3_quotient = int(open3_length / split_second)
open4_quotient = int(open4_length / split_second)

dondon1_quotient = int(dondon1_length / split_second)
dondon2_quotient = int(dondon2_length / split_second)
dondon3_quotient = int(dondon3_length / split_second)
dondon4_quotient = int(dondon4_length / split_second)

# 商の最小値を求める
quotient_length = np.array((open1_quotient, open2_quotient, open3_quotient, open4_quotient,
                            dondon1_quotient, dondon2_quotient, dondon3_quotient, dondon4_quotient))
quotient_min = quotient_length.min()
quotient_min = quotient_min - 30
################################################################################
################################################################################



################################################################################
#                                   SVM
################################################################################

    
# トレーニングデータとテストデータを ７:３ に分割
training_datas_quotient_num = int(quotient_min * 0.7)

training_num = int(split_second * training_datas_quotient_num)   
test_upper = int(split_second * quotient_min)
test_num = test_upper - training_num    

X_training_open1 = open1[0 : training_num]
X_training_open2 = open2[0 : training_num]

X_test_open1 = open1[training_num : test_upper]
X_test_open2 = open2[training_num : test_upper]

X_training_dondon1 = dondon1[0 : training_num]
X_training_dondon2 = dondon2[0 : training_num]

X_test_dondon1 = dondon1[training_num : test_upper]
X_test_dondon2 = dondon2[training_num : test_upper]

# 特徴量の抽出
training_datas_open1 = X_training_open1[['x','y','z']]
training_datas_open2 = X_training_open2[['x','y','z']]

test_datas_open1 = X_test_open1[['x', 'y', 'z']]
test_datas_open2 = X_test_open2[['x', 'y', 'z']]

training_datas_dondon1 = X_training_dondon1[['x','y', 'z']]
training_datas_dondon2 = X_training_dondon2[['x', 'y', 'z']]

test_datas_dondon1 = X_test_dondon1[['x', 'y', 'z']]
test_datas_dondon2 = X_test_dondon2[['x', 'y', 'z']]

# ラベル付け
training_labels_open1 = np.zeros(len(X_training_open1))
training_labels_open2 = np.zeros(len(X_training_open2))

test_labels_open1 = np.zeros(len(X_test_open1))
test_labels_open2 = np.zeros(len(X_test_open2))

training_labels_dondon1 = np.ones(len(X_training_dondon1))
training_labels_dondon2 = np.ones(len(X_training_dondon2))

test_labels_dondon1 = np.ones(len(X_test_dondon1))
test_labels_dondon2 = np.ones(len(X_test_dondon2))


# データとラベル
training_datas = np.vstack((training_datas_open1,
                            training_datas_open2,
                            training_datas_dondon1,
                            training_datas_dondon2
                            ))

test_datas = np.vstack((test_datas_open1,
                        test_datas_open2,
                        test_datas_dondon1,
                        test_datas_dondon2
                        ))

training_labels = np.hstack((training_labels_open1,
                             training_labels_open2,
                             training_labels_dondon1,
                             training_labels_dondon2
                             ))

test_labels = np.hstack((test_labels_open1,
                         test_labels_open2,
                         test_labels_dondon1,
                         test_labels_dondon2
                         ))

# ここにデータとトレーニングデータを付け加える
training = pd.DataFrame({'x':training_datas[:,0],
                         'y':training_datas[:,1],
                         'z':training_datas[:,2],
                         'lablel':training_labels})

test = pd.DataFrame({'x':test_datas[:,0],
                     'y':test_datas[:,1],
                     'z':test_datas[:,2],
                     'lablel':test_labels})

#                            
#    # csvファイルに書き出し
fileName = "training.csv"
fileName2 = "test.csv"
if os.path.exists(fileName):
    os.remove(fileName)
if os.path.exists(fileName2):
    os.remove(fileName2)
    
training.to_csv(fileName, mode='a',header=None, index=None)
test.to_csv(fileName2, mode='a',header=None, index=None)


## 統計量
##df = pd.DataFrame(X)
##print('統計量：%s' % df.describe())
#
#
## 特徴量の標準化
#standardScaler = StandardScaler()
## トレーニングデータの平均と標準偏差を計算
#standardScaler.fit(training_datas)
#
## 平均と標準偏差を用いて標準化
#training_datas_std = standardScaler.transform(training_datas)
#test_datas_std = standardScaler.transform(test_datas)
#
#
#svm = svm.SVC(kernel='linear', C=1.0 , random_state=0)
##svm = svm.SVC(kernel='rbf', C=1.0 , random_state=0)
##svm = svm.SVC(kernel='poly', C=1.0 , random_state=0)
##print(svm)
#   
#
## 線形svmのモデルにトレーニングデータを適合させる
#svm_fit = svm.fit(training_datas_std, training_labels)
##print('学習モデル：%s' % svm_fit)
#
## 2値分類予測
#pred = svm.predict(test_datas_std)
##print('予測：%s' % y_pred)
#
#target_names=['0','1']
#print('評価：%s' % classification_report(test_labels,pred, target_names=target_names))
#
#f = open('svm_dondon_door-open.txt', 'w')
#f.write('何もしないとドアの開閉状態の分類（データそのまま）：%s' % classification_report(test_labels,pred, target_names=target_names))
#f.close()

    


################################################################################
################################################################################






