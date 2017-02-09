# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 03:48:54 2017
フーリエ変換したデータを入れ、svmを行うプログラム
データ形式3行
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
from sklearn.metrics import confusion_matrix


#--------------------------------------------------------------------------------------------#
                                    # 振動データの保存先を指定--start
#--------------------------------------------------------------------------------------------#

#dir_name = ['clatter_12_18_csv_fft','open_12_18_csv_fft']
#dir_name = ['open_12_18_csv_beforelinear_fft','clatter_12_18_csv_beforelinear_fft']
#dir_name = ['open_12_18_csv_afterlinear_fft','clatter_12_18_csv_afterlinear_fft']
#dir_name = ['ballpen_beforelinear_fft','pencil_beforelinear_fft']
#dir_name = ['ballpen_afterlinear_fft','pencil_afterlinear_fft']
#dir_name = ['sku445-753_finger_afterlinear_fft','sku469-657_finger_afterlinear_fft']
#dir_name = ['sku445-753_afterlinear_fft','sku469-657_afterlinear_fft', 'sku186-580_afterlinear_fft']
#dir_name = ['sku445-753_beforelinear_fft','sku469-657_beforelinear_fft', 'sku186-580_beforelinear_fft']
#dir_name = ['ballpen_afterlinear','marker_afterlinear','sharppen_afterlinear','sku445-753_afterlinear_fft','sku469-657_afterlinear_fft', 'sku186-580_afterlinear_fft']
#dir_name = ['sku445-753_afterlinear_fft','sku469-657_afterlinear_fft', 'sku186-580_afterlinear_fft','t480-4888_afterlinear_fft']#01
#dir_name = ['sku445-753_afterlinear_fft','sku469-657_afterlinear_fft', 'sku186-580_afterlinear_fft']#02
#dir_name = ['pen_csv_afterlinear2_fft2','tile_csv_afterlinear2_fft2'] #2class
#dir_name = ['ballpen','enpitsu','marker','sharppen']
dir_name = ['sku186-580','sku445-753','sku469-657','t480-4888']
#dir_name = ['ballpen','enpitsu','marker','sharppen','sku186-580','sku445-753','sku469-657','t480-4888']
#--------------------------------------------------------------------------------------------#
                                    # 振動データの保存先を指定--end
#--------------------------------------------------------------------------------------------#

#dir_p = ['01haptics']
#dir_p = ['pen_csv_afterlinear2_fft2']
#dir_p = ['tile_csv_afterlinear2_fft2']
dir_p = ['pen_tile']

datas = []
files = []
for dirname in dir_name:
    # 振動データ保存先ディレクトリ名を指定
#    dir_path = 'C:\\Users\\student\\Documents\\data\\'+dirname+'\\'
#    dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dirname+'\\'
#    dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_finger_csv\\'+dirname+'\\'
    dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name + '\\'
#    dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_p[0]+'\\'+dirname+'\\'

    datas.append(np.array(os.listdir(dir_path)))
#    files.extend(os.listdir(dir_path))
#print(datas[1])


dir_i = 0
save_dir = '_'.join(dir_name[dir_i].split('_')[1:5])

# 出力先ディレクトリ名を指定
out_dir_path = 'C:\\Users\\student\\Documents\\data\\' + save_dir + '_svm\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv' + save_dir + '_svm\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_finger_csv' + save_dir + '_svm\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_p[0]+'\\' + save_dir + '_svm\\'



# 出力先のディレクトリが存在しない場合生成
# 出力先のディレクトリが存在する場合削除して、初期化する
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
        row = 1
  
        
#        dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_p[0]+'\\'+dir_name[index]+'\\'
        dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[index]+'\\'
     

    #    print(str(file))
        file = open(dir_path+file, 'r')
        for line in file:
#            if row % 2 == 1:
            values = line.strip().split(',')
#            print("len(value):{}".format(len(values)))
#            print("file:{}".format(file))

            # フーリエ変換した値を50ずつ合計する
            SUM = 50
            values = list(map(float, values))
            devi = int(len(values) / SUM)
            for i in range(0, SUM):
                input.append(sum(values[i*devi:(i+1)*devi]))
#            row += 1

        label.append(index)
                 
        features.append(input)
        labels.append(label)
        file.close()

features = np.array(features)
#labels = np.array(label)
labels = np.array(labels)
random = random.randint(1,10)

# 交差検証
training_datas, test_datas, training_labels, test_labels = cross_validation.train_test_split(features, labels, test_size=0.3, random_state=random)




start = time.time() #計測開始
#------------------------------------------------------------------------------------------#
                                    # SVMの種類を選ぶ　--start
#------------------------------------------------------------------------------------------#


#svm = svm.SVC(kernel='linear',class_weight="balanced",decision_function_shape="ovo",random_state=0)
#svm = svm.SVC(kernel='linear',class_weight="balanced",decision_function_shape="ovr",random_state=0)
#svm = svm.SVC(kernel='rbf', C=1.0 ,degree=3, random_state=0)
#svm = svm.SVC(kernel='poly', C=1.0 ,degree=3, random_state=0)
#svm = svm.SVC(kernel='poly', C=1.0 ,degree=4, random_state=0)
svm = svm.SVC(kernel='poly')
#svm = svm.SVC(kernel='rbf')
#print(svm)

#svm = OneVsRestClassifier(svm) # コメントアウトするとone-against-one

#------------------------------------------------------------------------------------------#
                                    # SVMの種類を選ぶ　--end
#------------------------------------------------------------------------------------------#

#SVMの学習 
svm_fit = svm.fit(training_datas, training_labels) 
#svm_fit = svm.fit(training_datas_norm, training_labels) 



# 学習したモデルを保存
pickle.dump(svm_fit,open(out_dir_path+"pickle.dump","wb"))
#print('学習モデル：%s' % svm_fit) 


#　SVM予測
pred = svm_fit.predict(test_datas)
#pred = svm_fit.predict(test_datas_norm)

# 計測終了
processing_time = time.time() - start

#------------------------------------------------------------------------------------------#
                                    # 正例と負例を表示　--start
#------------------------------------------------------------------------------------------#
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
#------------------------------------------------------------------------------------------#
                                    # 正例と負例を表示　--end
#------------------------------------------------------------------------------------------#


print('正解:%s' % test_labels)
print('予測：%s' % pred)
print('処理時間 : %f' % processing_time)
print('評価：%s' % classification_report(test_labels, pred, target_names=dir_name))
#print('評価：%s' % classification_report(test_labels, pred))




#------------------------------------------------------------------------------------------#
                        # 指定した名前でConfusion Matrixを保存する　--start
#------------------------------------------------------------------------------------------#

save_i = 1 # save_name[save_i]
# save_name[0],save_name[1],save_name[2]
save_name = ['2class_poly.txt','4class_poly_report.txt','8class_poly_report.txt']

#------------------------------------------------------------------------------------------#
                        # 指定した名前でConfusion Matrixを保存する　--end
#------------------------------------------------------------------------------------------#


# ファイル名（save_name[save_i]）を生成
if os.path.isfile(out_dir_path + save_name[save_i]) is False:
    f = open(out_dir_path + save_name[save_i], 'w')
    f.write("make file")
    f.close()
    print("make file")
    


# cofusion matrixを生成
cnf_matrix = confusion_matrix(pred,test_labels)
    
# 次の4つの内容を保存
#　■　「分類している全ての振動データの保存先名」
#　■　「svmパラメータ」
#　■　「f値」
#　■　「confusion matrix」
f = open(out_dir_path + save_name[save_i], 'a')
#f.write('{}と{}の分類（fft）：'.format(dir_name[0],dir_name[1]))
f.write('{}の分類（fft_normal）：'.format(dir_name))
f.write("\n")
f.write('パラメータ{}*****'.format(svm))
f.write("\n")
f.write('{}'.format(classification_report(test_labels,pred, target_names=dir_name)))
f.write("\n")
f.write("{}".format(pd.DataFrame(cnf_matrix,index=dir_name,columns = dir_name)))
f.write("\n")
#f.write('処理時間:{}*****'.format(processing_time))
f.close()





