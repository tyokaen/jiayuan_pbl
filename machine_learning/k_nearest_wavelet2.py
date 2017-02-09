# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 09:51:32 2017
一定サイズにしたウェーブレット変換後のファイルを用いて、
異常検知(k近傍法)を行うプログラム
利用方法を以下に示す。
１．正例を学習させる
プログラムを次のように変更し、実行する
#        clf = neighbors.KNeighborsClassifier(k, weights=weights)
        clf = joblib.load('model\\knn_clf')
#        clf.fit(inputs, label)
#        joblib.dump(clf, 'model\\knn_clf')

２.thresholdを最適にする
thresholdの数字を変え、
◆正例を入力データとする場合
    〇/△　△の値が学習に利用可能なファイル数から遠ざかるように調整する
◆負例を入力データとする場合
    〇/△　〇の値が学習に利用可能なファイル数に近づくように調整する
２．は次のようにプログラムを変更し、実行する
        clf = neighbors.KNeighborsClassifier(k, weights=weights)
#        clf = joblib.load('model\\knn_clf')
        clf.fit(inputs, label)
        joblib.dump(clf, 'model\\knn_clf')
        
上記の２つがお互いに最大になるthresholdを見つける
ここで作成したknn_clfをサーバ上に置き、最適なthresholdに書き換えることで、
サーバプログラム上で機械学習を利用できる

@author: student
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets, metrics
import random
import pywt
from sklearn.externals import joblib



#dir_name = ['02_05_open']
dir_name = ['02_05_clatter']


inputs = []
label = []
for class_name in dir_name:
	class_label = 0
	if class_name=='02_05_clatter':# 負例へ変更
		class_label = 1
	elif class_name=='bangbang':
		class_label = 1
#	dir_path = 'C:\\Users\\student\\Documents\\data\\'+class_name+'_wavelet\\'
	dir_path = 'C:\\Users\\student\\Documents\\data\\'+class_name+'_awavelet\\'
#      dir_path = 'C:\\Users\\student\\Documents\\data\\'+class_name+'_wavelet\\'

	files = os.listdir(dir_path)
#     print(files)
      # test_wavelet.pyを用いた場合
      # if row % 2 == 1: と row += 1のコメントを外し
      # その間のプログラムをインデントする
      # export_csv.pyを利用した場合は上記の操作は必要ない
	for file in files:
        		f = open(dir_path+file, 'r')
        		index = 0 
        		input = []
        		row = 1
        		for line in f:
#                          print("line:{}".format(line))
#                          if row % 2 == 1: 
                          values = line.strip().split(',')
#                                  print("values:{}".format(values))
                          values = list(map(float, values))
                          if len(values) >= 10:
                                  print(file+'/'+str(len(values)))
                                  input.extend(values[0:10])
#                                          print("len:{}".format(len(input)))
                          
#                          row += 1
        		inputs.append(input)
        		label.append(class_label)
        		f.close()
          
for i in range(len(inputs)-1,-1,-1):
    print(len(inputs[i]))
    if len(inputs[i]) != 30:
        inputs.pop(i)
        label.pop(i)



inputs = np.array(inputs)

print("学習に利用可能なファイル数:{}".format(len(inputs)))
label = np.array(label)
indices = np.random.permutation(len(inputs))
inputs_train = inputs[indices[:-40]]
label_train = label[indices[:-40]]
inputs_test = inputs[indices[-40:]]
label_test = label[indices[-40:]]


#########################################
k_list = [3] # k の数
weights_list =['distance']

#########################################


#result_listsp = [[],[],[]]
#result_listsn = [[],[],[]]

threshold = 120
i = 1 # subplot用

for weights in weights_list:
    for k in k_list:
#        clf = neighbors.KNeighborsClassifier(k, weights=weights)
        clf = joblib.load('model\\knn_clf')
#        clf.fit(inputs, label)
#        joblib.dump(clf, 'model\\knn_clf')
        
        distset = clf.kneighbors(inputs,k)[0]
        correct = 0
        incorrect = 0
        data_index = 0
        for dists in distset:
            data_index += 1
            for d in dists:
                print("distance：{}".format(d))
                if d > threshold:
#                     print(str(d))
                     if label[data_index-1] > 0:
			#異常検知の正解数不正解数を記録
                         correct += 1
                     else:
                         incorrect += 1
                     break                    
        print(str(correct)+'/'+str(incorrect))
             