# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 03:48:54 2017
フーリエ変換したデータを入れ、svmを行うプログラム
データ形式3行
@author: student
"""



import os
import numpy as np
from sklearn import cross_validation
import time
from sklearn import svm
from sklearn.metrics import classification_report
import pickle
import random
import shutil
from sklearn.multiclass import OneVsRestClassifier

#dir_name = ['clatter_12_18_csv_fft','open_12_18_csv_fft']
#dir_name = ['open_12_18_csv_beforelinear_fft','clatter_12_18_csv_beforelinear_fft']
#dir_name = ['open_12_18_csv_afterlinear_fft','clatter_12_18_csv_afterlinear_fft']
#dir_name = ['ballpen_beforelinear_fft','pencil_beforelinear_fft']
#dir_name = ['ballpen_afterlinear_fft','pencil_afterlinear_fft']
#dir_name = ['sku445-753_finger_afterlinear_fft','sku469-657_finger_afterlinear_fft']
#dir_name = ['sku445-753_afterlinear_fft','sku469-657_afterlinear_fft', 'sku186-580_afterlinear_fft']
#dir_name = ['sku445-753_beforelinear_fft','sku469-657_beforelinear_fft', 'sku186-580_beforelinear_fft']
dir_name = ['ballpen_afterlinear','marker_afterlinear','sharppen_afterlinear','sku445-753_afterlinear_fft','sku469-657_afterlinear_fft', 'sku186-580_afterlinear_fft']




datas = []
files = []
for dirname in dir_name:
#    dir_path = 'C:\\Users\\student\\Documents\\data\\'+dirname+'\\'
#    dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dirname+'\\'
#    dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_finger_csv\\'+dirname+'\\'
    dir_path = 'C:\\Users\\student\\Documents\\data\\haptics3_csv\\'+dirname+'\\'

    datas.append(np.array(os.listdir(dir_path)))
#    files.extend(os.listdir(dir_path))
#print(datas[1])


dir_i = 0
save_dir = '_'.join(dir_name[dir_i].split('_')[1:5])

#dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i] + '\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\' + save_dir + '_svm\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv' + save_dir + '_svm\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_finger_csv' + save_dir + '_svm\\'
out_dir_path = 'C:\\Users\\student\\Documents\\data\\haptics3_csv\\' + save_dir + '_svm\\'



if os.path.isdir(out_dir_path) is False:
    os.makedirs(out_dir_path)
    print("make dir")
#else:
#    shutil.rmtree(out_dir_path)
#    print("delete dir")
#    os.makedirs(out_dir_path)
#    print("make dir")



features = []
labels = []
# ディレクトリごとにラベルを付ける
for index,files in enumerate(datas):
    for file in files:
        print(file)
        label = []
        input = []
        row = 1
#    
#        if index == 0:
#           dir_i = 0
##           dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\'
##           dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dir_name[dir_i]+'\\'
#           dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_finger_csv\\'+dir_name[dir_i]+'\\'
#
#        else:
#            dir_i = 1
##            dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\' 
##            dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dir_name[dir_i]+'\\'
#            dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_finger_csv\\'+dir_name[dir_i]+'\\'
#            
    
#        if index == 0:
#           dir_i = 0
##           dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\'
##           dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dir_name[dir_i]+'\\'
#           dir_path = 'C:\\Users\\student\\Documents\\data\\haptics3_csv\\'+dir_name[dir_i]+'\\'
#
#        elif index == 1:
#            dir_i = 1
##            dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\' 
##            dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dir_name[dir_i]+'\\'
#            dir_path = 'C:\\Users\\student\\Documents\\data\\haptics3_csv\\'+dir_name[dir_i]+'\\'
#        else:
#            dir_i = 2
#            dir_path = 'C:\\Users\\student\\Documents\\data\\haptics3_csv\\'+dir_name[dir_i]+'\\'

        if index == 0:
           dir_i = 0
#           dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\'
#           dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dir_name[dir_i]+'\\'
           dir_path = 'C:\\Users\\student\\Documents\\data\\haptics3_csv\\'+dir_name[dir_i]+'\\'

        elif index == 1:
            dir_i = 1
#            dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\' 
#            dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dir_name[dir_i]+'\\'
            dir_path = 'C:\\Users\\student\\Documents\\data\\haptics3_csv\\'+dir_name[dir_i]+'\\'
        elif index == 2:
            dir_i = 2
            dir_path = 'C:\\Users\\student\\Documents\\data\\haptics3_csv\\'+dir_name[dir_i]+'\\'  
        elif index == 3:   
           dir_i = 3
#           dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\'
#           dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dir_name[dir_i]+'\\'
           dir_path = 'C:\\Users\\student\\Documents\\data\\haptics3_csv\\'+dir_name[dir_i]+'\\'

        elif index == 4:
            dir_i = 4
#            dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\' 
#            dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dir_name[dir_i]+'\\'
            dir_path = 'C:\\Users\\student\\Documents\\data\\haptics3_csv\\'+dir_name[dir_i]+'\\'
        else:
            dir_i = 5
            dir_path = 'C:\\Users\\student\\Documents\\data\\haptics3_csv\\'+dir_name[dir_i]+'\\'        

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
#        if index == 0:
#            label.append(0)
#        else:
#            label.append(1)
            
#        if index == 0:
#            label.append(0)
#        elif index == 1:
#            label.append(1)
#        else:
#            label.append(2)

        if index == 0:
            label.append(0)
        elif index == 1:
            label.append(1)
        elif index == 2:
            label.append(2)
        elif index == 3:
            label.append(3)
        elif index == 4:
            label.append(4)
        else:
            label.append(5)
            
            
                
        features.append(input)
        labels.append(label)
        file.close()

features = np.array(features)
#labels = np.array(label)
labels = np.array(labels)
random = random.randint(1,10)
training_datas, test_datas, training_labels, test_labels = cross_validation.train_test_split(features, labels, test_size=0.3, random_state=random)

#fix = 100
#training_datas, test_datas, training_labels, test_labels = cross_validation.train_test_split(features, labels, test_size=0.3, random_state=fix)


################################################################################
#                                   SVM
################################################################################



start = time.time()
#svm = svm.SVC(kernel='linear',class_weight="balanced",decision_function_shape="ovo",random_state=0)
#svm = svm.SVC(kernel='linear',class_weight="balanced",decision_function_shape="ovr",random_state=0)
#svm = svm.SVC(kernel='rbf', C=10.0 ,degree=3, random_state=0)
#svm = svm.SVC(kernel='poly', C=1.0 ,degree=3, random_state=0)
#svm = svm.SVC(kernel='poly', C=1.0 ,degree=4, random_state=0)
svm = svm.SVC(kernel='poly')
#print(svm)

#svm = OneVsRestClassifier(svm) # コメントアウトするとone-against-one


#線形svmのモデルにトレーニングデータを適合させる
svm_fit = svm.fit(training_datas, training_labels) 
processing_time = time.time() - start

pickle.dump(svm_fit,open(out_dir_path+"pickle.dump","wb"))

print('学習モデル：%s' % svm_fit) 

#test_datas = test_datas[0:300]  
#test_labels = test_datas[0:300] 
#     2値分類予測
pred = svm_fit.predict(test_datas)


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

print('正解:%s' % test_labels)
print('予測：%s' % pred)
print('処理時間 : %f' % processing_time)


#target_names=['0','1']
#target_names=['0','1','2']
target_names=['0','1','2','3','4','5']

print('評価：%s' % classification_report(test_labels, pred, target_names=target_names))
#print('評価：%s' % classification_report(test_labels, pred))



#save_name = ['svm_fft_one_against_rest_report.txt','svm_fft_one_against_one_report.txt']
save_name = ['svm6_fft_one_against_rest_report.txt','svm6_fft_one_against_one_report.txt']

save_i = 0


if os.path.isfile(out_dir_path + save_name[save_i]) is False:
    f = open(out_dir_path + save_name[save_i], 'w')
    f.write("make file")
    f.close()
    print("make file")


f = open(out_dir_path + save_name[save_i], 'a')
#f.write('{}と{}の分類（fft）：'.format(dir_name[0],dir_name[1]))
f.write('{}と{}と{}の分類（fft）：'.format(dir_name[0],dir_name[1],dir_name[2]))

f.write('{}'.format(classification_report(test_labels,pred, target_names=target_names)))
f.write('処理時間:{}'.format(processing_time))
f.close()

