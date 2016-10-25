# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:24:50 2016

@author: student
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:28:52 2016

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
training = pd.read_csv('C:/Users/student/.spyder-py3/dondon_door-open_training.csv')
test = pd.read_csv('C:/Users/student/.spyder-py3/dondon_door-open_test.csv')

# 列名追加
training.columns = ['label','var', 'mean', 'median', 'max', 'min']
test.columns = ['label','var', 'mean', 'median', 'max', 'min']

# データとラベルを取得
training_datas = np.array(training[['var', 'mean', 'median', 'max', 'min']])
training_labels = np.array(training['label'])
test_datas = np.array(test[['var', 'mean', 'median', 'max', 'min']])
test_labels = np.array(test['label'])


################################################################################
#                                   SVM
################################################################################

#svm = svm.SVC(kernel='linear', C=1.0 , random_state=0)
#svm = svm.SVC(kernel='rbf', C=1.0 , random_state=0)
svm = svm.SVC(kernel='poly', C=1.0 ,degree=4, random_state=0)
#print(svm)

#線形svmのモデルにトレーニングデータを適合させる
svm_fit = svm.fit(training_datas, training_labels) 
#    print('学習モデル：%s' % svm_fit) 
    
#     2値分類予測
pred = svm.predict(test_datas)
#print('予測：%s' % y_pred)

target_names=['0','1']
print('評価：%s' % classification_report(test_labels,pred, target_names=target_names))

f = open('svm_statistick_dondon_door-open.txt', 'w')
f.write('何もしないとドアの開閉状態の分類（統計）：%s' % classification_report(test_labels,pred, target_names=target_names))
f.close()









