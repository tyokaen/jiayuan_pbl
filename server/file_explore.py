# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 15:14:41 2016

@author: student
"""

import os
import re
            
            
def find_files(director):
    for root, dirs, files in os.walk(director):
        print ("root:%s" % root)
        print ("dirs:%s" % dirs)
        print ("files:%s" % files)
        yield root
        for file in files:
         yield os.path.join(root, file)
    
for file in find_files('c:/Users/student/.spyder-py3/'):
    target = r"\.csv"
    # targetと一致した文字列の最初の１つを返す
    match_string = re.search(target, file)
    if match_string:
        #print(match_string.group())
        print(file)
