# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 18:32:45 2016
# ウェーブレット変換したa.csvファイルのみを抽出し、_waveletディレクトリにコピーするプログラム
@author: student
"""

import os
import shutil
import re 

check = re.compile(r'a\.csv')

# コピー元
dir_i = 1
#dir_name = ['clatter_12_18_v2']
dir_name = ['open_1_17','clatter_1_17']
dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\'

# コピー先
mk_dir_i = 1
mk_dir_name =  ['open_1_17_wavelet','clatter_1_17_wavelet']
#mk_dir_name =  ['open_1_17_csv']
mk_dir_path = 'C:\\Users\\student\\Documents\\data\\'+mk_dir_name[mk_dir_i]+'\\'

files = os.listdir(dir_path)

# ウェーブレット変換したa.csvファイルのみを抽出し、_waveletディレクトリにコピーするプログラム
for file in files:
    if not check.search(str(file)) is None:
        if not os.path.isdir(mk_dir_path):
            os.mkdir(mk_dir_path)
            print("make dir")
        shutil.copy(dir_path+file,mk_dir_path+file)
        print(file)

# csvファイルのみを抽出し、コピーするプログラム
#for file in files:
#    if check.search(str(file)) is None:
#        shutil.copy(dir_path+file,mk_dir_path+file)



        