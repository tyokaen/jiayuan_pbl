# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 01:33:46 2016

@author: student
"""
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report


################################################################################
#                               データの前処理
################################################################################

# データ取得
training = pd.read_csv('C:/Users/student/.spyder-py3/training.csv')
test = pd.read_csv('C:/Users/student/.spyder-py3/test.csv')

training = training.dropna()
test = test.dropna()

# 列名追加
training.columns = ['label','x','y','z']
test.columns = ['label','x','y','z']

# データとラベルを取得
training_datas = np.array(training[['x','y','z']])
training_labels = np.array(training['label'])

test_datas = np.array(test[['x','y','z']])
test_labels = np.array(test['label'])


################################################################################
#                                   SVM
################################################################################
#svm = svm.SVC(kernel='linear', C=1.0 , random_state=0)
svm = svm.SVC(kernel='rbf', C=1.0 ,random_state=0)
#svm = svm.SVC(kernel='poly', C=1.0 , random_state=0)
#print(svm)
   

# 線形svmのモデルにトレーニングデータを適合させる
svm_fit = svm.fit(training_datas, training_labels)
#print('学習モデル：%s' % svm_fit)

# 2値分類予測
pred = svm.predict(test_datas)
#print('予測：%s' % y_pred)

target_names=['0','1']
print('評価：%s' % classification_report(test_labels,pred, target_names=target_names))

f = open('svm_sonomama.txt', 'w')
f.write('何もしないとドアの開閉状態の分類（データそのまま）：%s' % classification_report(test_labels,pred, target_names=target_names))
f.close()