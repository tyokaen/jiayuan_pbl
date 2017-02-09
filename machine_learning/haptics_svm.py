# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 08:38:03 2017
haptics SVM
@author: student
"""




import os
import numpy as np
import pandas as pd
from sklearn import cross_validation
import time
from sklearn import svm
from sklearn.metrics import classification_report
import pickle
import random
import shutil
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import KernelPCA
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix


#dir_name = ['clatter_12_18_csv_fft','open_12_18_csv_fft']
#dir_name = ['open_12_18_csv_beforelinear_fft','clatter_12_18_csv_beforelinear_fft']
#dir_name = ['open_12_18_csv_afterlinear_fft','clatter_12_18_csv_afterlinear_fft']
#dir_name = ['ballpen_beforelinear_fft','pencil_beforelinear_fft']
#dir_name = ['ballpen_afterlinear_fft','pencil_afterlinear_fft']
#dir_name = ['sku445-753_finger_afterlinear_fft','sku469-657_finger_afterlinear_fft']
#dir_name = ['sku445-753_afterlinear_fft','sku469-657_afterlinear_fft', 'sku186-580_afterlinear_fft']
#dir_name = ['sku445-753_beforelinear_fft','sku469-657_beforelinear_fft', 'sku186-580_beforelinear_fft']
#dir_name = ['ballpen_afterlinear','marker_afterlinear','sharppen_afterlinear','sku445-753_afterlinear_fft','sku469-657_afterlinear_fft', 'sku186-580_afterlinear_fft']
#dir_name = ['sku445-753_afterlinear_fft','sku469-657_afterlinear_fft', 'sku186-580_afterlinear_fft']
#dir_name = ['sku445-753_afterlinear_fft','sku469-657_afterlinear_fft', 'sku186-580_afterlinear_fft','t480-4888_afterlinear_fft']#01
#dir_name = ['sku445-753_afterlinear_fft','sku469-657_afterlinear_fft', 'sku186-580_afterlinear_fft']#02

#dir_name = ['ballpen','enpitsu','marker','sharppen']
#dir_name = ['sku186-580','sku445-753','sku469-657','t480-4888']
#dir_name = ['ballpen','enpitsu','marker','sharppen','sku186-580','sku445-753','sku469-657','t480-4888']

#dir_p = ['01haptics']
#dir_p = ['02haptics']
#dir_p = ['01haptics_4-1']
#dir_p = ['pen_tile']
dir_name = ['clatter_12_18_csv_fft','open_12_18_csv_fft']



datas = []
files = []
for dirname in dir_name:
    dir_path = 'C:\\Users\\student\\Documents\\data\\'+dirname+'\\'
#    dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dirname+'\\'
#    dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_finger_csv\\'+dirname+'\\'
#    dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_p[0]+'\\'+dirname+'\\'

    datas.append(np.array(os.listdir(dir_path)))
#    files.extend(os.listdir(dir_path))
#print(datas[1])


dir_i = 0
save_dir = '_'.join(dir_name[dir_i].split('_')[1:5])

#dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i] + '\\'
out_dir_path = 'C:\\Users\\student\\Documents\\data\\' + save_dir + '_svm\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv' + save_dir + '_svm\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_finger_csv' + save_dir + '_svm\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_p[0]+'\\' + save_dir + '_svm\\'



if os.path.isdir(out_dir_path) is False:
    os.makedirs(out_dir_path)
    print("make dir")
else: 
    shutil.rmtree(out_dir_path)
    print("delete dir")
    os.makedirs(out_dir_path)
    print("make dir")



features = []
labels = []
# ディレクトリごとにラベルを付ける
for index,files in enumerate(datas):
    for file in files:
        print(file)
        label = []
        input = []
#        row = 1
#    
#        dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_p[0]+'\\'+dir_name[index]+'\\'
        dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[index]+'\\'

    #    print(str(file))
        file = open(dir_path+file, 'r')
        for line in file:
#            if row % 2 == 1:
            values = line.strip().split(',')
#            print("len(value):{}".format(len(values)))
#            print("file:{}".format(file))

            values = list(map(float, values))
            devi = int(len(values) / 50)
            for i in range(0, 50):
                input.append(sum(values[i*devi:(i+1)*devi]))
#            row += 1


        label.append(index)
            
                
        features.append(input)
        labels.append(label)
        file.close()

features = np.array(features)
#labels = np.array(label)
le = LabelEncoder()
labels = le.fit_transform(labels)

#labels = np.array(labels)
random = random.randint(1,10)
training_datas, test_datas, training_labels, test_labels = cross_validation.train_test_split(features, labels, test_size=0.3, random_state=random)

#normalization = MinMaxScaler()
#training_datas_norm = normalization.fit_transform(training_datas)
#test_datas_norm = normalization.transform(test_datas)



################################################################################
#                                   SVM
################################################################################
kpca = KernelPCA(n_components=None, kernel='rbf',gamma=15)
#kpca = KernelPCA(kernel='rbf',gamma=15)

training_datas_pca = kpca.fit_transform(training_datas)
test_datas_pca = kpca.fit_transform(test_datas)

#start = time.time()
#svm = svm.SVC(kernel='linear',class_weight="balanced",decision_function_shape="ovo",random_state=0)
#svm = svm.SVC(kernel='linear',class_weight="balanced",decision_function_shape="ovr",random_state=0)
#svm = svm.SVC(kernel='rbf', C=1.0 ,degree=3, random_state=0)

#svm = svm.SVC(kernel='poly', C=1.0 ,degree=3, random_state=0)
#svm = svm.SVC(kernel='poly', C=1.0 ,degree=4, random_state=0)
#svm = svm.SVC(kernel='poly')
#print(svm)

#svm = OneVsRestClassifier(svm) # コメントアウトするとone-against-one
#pipe_svc = Pipeline([('scl',MinMaxScaler()),('clf',SVC(random_state=1))])
#pipe_svc = Pipeline([('scl',StandardScaler()),('clf',SVC(random_state=1))])
#pipe_svc = Pipeline([('scl',MinMaxScaler()),('pca',KernelPCA(n_components=None)),('clf',SVC(random_state=1))])
pipe_svc = Pipeline([('clf',SVC(random_state=1))])

#param_range = [0.001,0.001,0.1,1.0,10.0]
param_range = []

#PARAM_NUM = 82
#r = round(PARAM_NUM / 2)
#for j in range(-r*25,r*25,25):
#    power =  j/100
##    print(power)
#    if power >= -10 and power <= 10:
#        print(power)
#        param_range.append(2**power)

PARAM_NUM = 20
r = round(PARAM_NUM / 2)
for j in range(10):
    power =  0.0001*10**j
#    print(power)
    if power > 0 and power <= 1000:
        print(power)
        param_range.append(power)
        
        
        
#param_range = [1.0,10.0]

#param_grid = [{'clf__C':param_range, 'clf__kernel':['poly']},
#              {'clf__C':param_range, 'clf__gamma':param_range,
#              'clf__kernel':['rbf']}]

param_grid = [{'clf__C':param_range, 'clf__gamma':param_range}]
#param_grid = [{'clf__C':param_range, 'clf__kernel':['poly']}]
gs = GridSearchCV(estimator=pipe_svc,
                  param_grid=param_grid,
                  scoring='accuracy',
                  cv=5,
                  n_jobs=-1)

#------------------------------------------------#
#                  ipython
#------------------------------------------------#
#gs = gs.fit(training_datas,training_labels)
#print(gs.best_score_)
#print(gs.best_params_)
#pred = gs.predict(test_datas)
#classification_report(test_labels,pred, target_names=dir_name)
#save_i = 1
#save_name = ['4class_pen_rbf_report.txt','4class_tile_rbf_report.txt','8class_pen_tile_rbf_report.txt']
#
#if os.path.isfile(out_dir_path + save_name[save_i]) is False:
#    f = open(out_dir_path + save_name[save_i], 'w')
#    f.write("make file")
#    f.close()
#    print("make file")
#
#
#
#
#cnf_matrix = confusion_matrix(pred,test_labels)
#
#f = open(out_dir_path + save_name[save_i], 'a')
#f.write('{}の分類（fft）：'.format(dir_name))
#f.write("\n")
#f.write("{}".format(param_grid))
#f.write("\n")
#f.write("パラメータ:{}".format(gs))
#f.write("\n")
#f.write('{}'.format(gs.best_params_))
#f.write("\n")
#f.write('{}'.format(param_range))
#f.write("\n")
#f.write('{}'.format(classification_report(test_labels,pred, target_names=dir_name)))
#f.write("\n")
#f.write('{}'.format(pd.DataFrame(cnf_matrix,index=dir_name,columns = dir_name)))
#f.write("\n")
#f.close()

#------------------------------------------------#



#線形svmのモデルにトレーニングデータを適合させる
#svm_fit = svm.fit(training_datas, training_labels) 
#processing_time = time.time() - start

#pickle.dump(svm_fit,open(out_dir_path+"pickle.dump","wb"))

#print('学習モデル：%s' % svm_fit) 

#test_datas = test_datas[0:300]  
#test_labels = test_datas[0:300] 
#     2値分類予測
#pred = svm_fit.predict(test_datas)


# 正例と負例を表示
#TP = 0
#TN = 0
#FP = 0
#FN = 0
#count = 0
#for i in range(0,len(test_labels)):
#    if pred[i] == test_labels[i][0]:
#        if pred[i] == 0:
#            TP += 1
#            continue
#        else:
#            TN += 1
#            continue
#        continue
#    else:
#        count += 1
#        if pred[i] == 1:
#            FP += 1
#            continue
#        else:
#            FN += 1
#            continue
#print(count)
#print("TN:{}/TP:{}/FP:{}/FN:{}".format(TN,TP,FN,FP))

#print('正解:%s' % test_labels)
#print('予測：%s' % pred)
#print('処理時間 : %f' % processing_time)


#target_names=['0','1']
#target_names=['0','1','2']
#------------------------------------------------------------------------------------------#
                                # クラスの数だけ以下を増やす --start
#------------------------------------------------------------------------------------------#

# 分類するクラス数分
#target_names=['0','1','2','3','4','5']
#target_names = dir_name
#------------------------------------------------------------------------------------------#
                                # クラスの数だけ以下を増やす　--end
#------------------------------------------------------------------------------------------#


#print('評価：%s' % classification_report(test_labels, pred, target_names=target_names))
#print('評価：%s' % classification_report(test_labels, pred))



#save_name = ['svm_fft_one_against_rest_report.txt','svm_fft_one_against_one_report.txt']
#
#------------------------------------------------------------------------------------------#
#                                 指定した名前でConfusion Matrixを保存する　--start
#------------------------------------------------------------------------------------------#
# save_i = 0　なら、　save_name[0,1]なので、svm6_fft_against_rest_report.txt
# save_i = 1　なら、 svm6_fft_one_against_one_report.txt
#
#save_i = 0
#save_name = ['svm6_fft_one_against_rest_report.txt','svm6_fft_one_against_one_report.txt']
#
#------------------------------------------------------------------------------------------#
#                                 クラスの数だけ以下を増やす　--end
#------------------------------------------------------------------------------------------#
#
#
#if os.path.isfile(out_dir_path + save_name[save_i]) is False:
#    f = open(out_dir_path + save_name[save_i], 'w')
#    f.write("make file")
#    f.close()
#    print("make file")
#
#
#f = open(out_dir_path + save_name[save_i], 'a')
##f.write('{}と{}の分類（fft）：'.format(dir_name[0],dir_name[1]))
#f.write('{}の分類（fft）：'.format(dir_name))
##f.write('{}'.format(classification_report(test_labels,pred, target_names=target_names)))
##f.write('処理時間:{}'.format(processing_time))
#f.close()


