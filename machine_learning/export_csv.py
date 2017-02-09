# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 16:08:52 2017
サーバ上で取得した振動データには、***csvと***a.csvの2種類がある
***csvは、文字列振動データ　
***a.csvは、文字列振動データをウェーブレット変換したデータ
その中から、csvファイルのみを抽出し、_csvディレクトリにコピーするプログラム
@author: student
"""


import os
import shutil
import re 

# 正規表現
check = re.compile(r'a\.csv')


#--------------------------------------------------------------------------------------------#
                                    # 保存先を指定する --start
#--------------------------------------------------------------------------------------------#
# コピー元
#dir_i = 0
dir_i = 0
#dir_name = ['clatter_12_18_v2']
#dir_name = ['open_1_17','clatter_1_17']
#dir_name = ['02-01＿door-open','02-01_clatter']
dir_name = ['02_05_open','02_05_clatter']

dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\'

#--------------------------------------------------------------------------------------------#
                                    # 保存先を指定する --end
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
                                    # 出力先を指定する --start
#--------------------------------------------------------------------------------------------#
# コピー先
#mk_dir_i = 1
#mk_dir_name =  ['open_1_17_wavelet','clatter_1_17_wavelet']
#mk_dir_name =  ['open_1_17_csv']
#mk_dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'_wavelet\\'
mk_dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'_csv\\'

#--------------------------------------------------------------------------------------------#
                                    # 出力先を指定する --end
#--------------------------------------------------------------------------------------------#


files = os.listdir(dir_path)


#--------------------------------------------------------------------------------------------#
                                    # ウェーブレットのみを保存 --start
                                    # csvを保存したい場合は、コメントアウトする
#--------------------------------------------------------------------------------------------#
# ウェーブレット変換したa.csvファイルのみを抽出し、_waveletディレクトリにコピーするプログラム
#for file in files:
#    if not check.search(str(file)) is None:
#        if not os.path.isdir(mk_dir_path):
#            os.mkdir(mk_dir_path)
#            print("make dir")
#        shutil.copy(dir_path+file,mk_dir_path+file)
#        print(file)

#--------------------------------------------------------------------------------------------#
                                    # ウェーブレットのみを保存 --end
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
                                    # csvのみを保存 --start
                                    # ウェーブレットを保存したい場合は、コメントアウトする
#--------------------------------------------------------------------------------------------#

# csvファイルのみを抽出し、コピーするプログラム
for file in files:
    if check.search(str(file)) is None:
        if not os.path.isdir(mk_dir_path):
            os.mkdir(mk_dir_path)
        shutil.copy(dir_path+file,mk_dir_path+file)
        print(file)
#--------------------------------------------------------------------------------------------#
                                    # ウェーブレットのみを保存 --end
#--------------------------------------------------------------------------------------------#


        