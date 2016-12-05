#!/usr/bin/env python3


import sys
sys.stdout.write('Content-type: text/html; charset=UTF-8 \r\n')


################################################################################
# 				get_csv
################################################################################


#sys.stdout.write("hello")

import cgi
import os
import pandas as pd
import re
form = cgi.FieldStorage()
import cgitb
cgitb.enable()
import datetime
from sklearn import neighbors
import numpy as np
from sklearn.externals import joblib
import pywt


# fileName date
cd = "/home/orange/workspace/result/"

date= datetime.datetime.today()
year = str(date.year) + "_"
month = str(date.month)+ "_"
day = str(date.day)+ "_"
hour = str(date.hour) + "h"
minute = str(date.minute) + "m"
second = str(date.second) +"s"
microsecond = str(date.microsecond) + "ms"

num_str = year + month + day+hour + minute + second + microsecond
extension = ".csv"

#getName = cd + num_str + extension


dirName = "/home/orange/workspace/one/"
#fileName2 =  dirName + num_str + extension


#vibration = form['jiayuan'].value
#filename = form['jiayuan'].filename

#sys.stdout.write(vibration.decode('utf-8'))
#sys.stdout.write(len(vibration))

#if os.path.exists(dirName):
    #for root, dirs, files in os.walk(dirName):
    	#for file in files:
         #os.remove(os.path.join(root,file))
		#sys.stdout.write('deleteFileName:')
		#sys.stdout.write(file)
		#sys.stdout.write('</br>')

#getName = form['jiayuan'].filename
#sys.exit(getName)

#sys.stdout.write(form)
if not 'jiayuan' in form:
    sys.stdout.write("failure-jiayuan")
    sys.exit("failure-jiayuan")

if 'jiayuan' in form:
    #sys.stdout.write('hello')
    getName = cd + form['jiayuan'].filename
    time = form['jiayuan'].filename
    #sys.stdout.write("failure-jiayuan")(getName)

    filePath = open(getName, 'wb')
        
    #if os.path.isfile(fileName2):
        #one_vibration = open(fileName2, 'wb')
    #else:
        #sys.stdout.write("fairular-fileName2")
        #sys.exit()
        
    fileData = form['jiayuan'].value
    #sys.stdout.write(form['jiayuan'].getName)
    fileData2 = form['jiayuan'].value

    # write	
    filePath.write(fileData)
    #one_vibration.write(fileData2)

    filePath.close()
    #one_vibration.close()
    ################################################################################
    ################################################################################
    

    dirName = "/home/orange/workspace/result/"
    #file = os.listdir(dirName)
    #sys.stdout.write(file)
    
    #if os.path.exists(dirName + file[0]) is False:
    #    sys.stdout.write("error")
    #    sys.exit()
    
    #filePath = dirName + file[0]
    #filePath = getName
    #########################################################

    
    #fileName = filePath
    col_names = ['{:d}'.format(i) for i in range(33)]
    
    if os.path.isfile(getName):
        df = pd.read_csv(getName,names=col_names,header=None)
    else:
        sys.stdout.write("fairular-read_csv-getName")
        sys.exit("fairular-read_csv-getName")


	# ID check and Ascending
    ID_NUM = '[81022e10'
    cnt = 0
    indexs = []
    tmp = []
    # check id number
    for i in range(len(df)):
        if(df.loc[i]['0'] == ID_NUM):
            cnt += 1
            if len(df.loc[i].dropna()) >=4:
                indexs.append(i)
            
    #sys.stdout.write("id_numbers::{}".format(cnt))      
    
    # timestanmp is ascending isn't it ?
    sort = {'{:d}'.format(i):float(df.loc[i]['1']) for i in indexs}
    
    # timestamp is ascending
    sort_result = sorted(sort.items(), key=lambda x:x[1])
    
    # df is sorted by timestamp 
    ascending_df = []
    for key, value in sort_result :
        if len(df.loc[int(key)].dropna()) >= 4:
            ascending_df.append(df.loc[int(key)])
#            sys.stdout.write("Ascending***key:{},value:{}".format(key,value))
    
    # Delet the value compared to the number of seconds before a longer open time(1 second)
    for i in range(len(ascending_df)):
        if i == len(ascending_df)-1:
            break
        if float(ascending_df[i+1].loc['1']) - float(ascending_df[i].loc['1']) > 1000:

            tmp = ascending_df.pop(i)
#            sys.stdout.write("compare the values next to each other. After that, if the difference value is more than 1 second, remove the value:{}".format(tmp))

    df_indexs = [] 
    df_indexs = range(len(ascending_df))
        
    new_df = pd.DataFrame(ascending_df,index=df_indexs)
    
    if len(df) <= 50:
        sys.stdout.write("failure-threshold")
        sys.exit("failure:<=500")
    
    ID = float(81022e10)
    # all_xyz = []
    df_drop = []
    df_union = []
    data_sets = []
    x = []
    y = []
    z = []
    xx = []
    yy = []
    zz = []
    xxx = []
    yyy = []
    zzz = []

    count_zz = 0
    count_zzz = 0

    # Store df_drop values that except nan
    for i in range(len(new_df)):
        df_drop.append(new_df.loc[i].dropna())
                
#                a = df.loc[i].dropna()               
#                all_xyz.append(len(a))     
            
#            for i in all_xyz:
#                if i == 33:
#                    count_33 += 1
#                else:
#                    count_n33 += 1                        
#            
#            sys.stdout.write("missing values number/total values number:{}/{}".format(count_n33,len(df)))
#            sys.stdout.write("non missing values numbe / total values number:{}/{}".format(count_33,len(df)))

################################################################################
#                                xyz33
###############################################################################


    for i in range(len(new_df)):
        df_drop_len = len(df_drop[i])
        
        ### when data is no loss
        if df_drop_len == 33:
            
            df_union = list(df_drop[i])
        
            # delete
            extract_df_0 = df_union.pop(0)
#                    sys.stdout.write("timestamp:{}".format(timestamp))
            timestamp = float(df_union.pop(0))
#                    sys.stdout.write("extract_2:{}".format(extract_2))
            extract_df_2 = df_union.pop(0)
#                    sys.stdout.write("extract_3:{}".format(extract_3))
           
            # delete
            extract_df_3 = df_union.pop()
#                    sys.stdout.write("extract_4:{}".format(extract_4))

            p1 = re.search(r"\[", extract_df_0)
            p2 = re.search(r"\]", extract_df_3)
            
            if p1 is None or p2 is None:
                continue
            
            # store id
            add_string1 = float(extract_df_0[p1.start()+1:])
            data_sets.append({'id':add_string1,'timestamp':timestamp, 'data':df_union})

            # append the value except for [
            add_string2 = float(extract_df_3[0:p2.start()])
            df_union.append(add_string2)
                   
            for j in range(0,30,3):
                x.append(float(df_union[j]))
                
            for j in range(1,30,3):
                y.append(float(df_union[j]))
        
            for j in range(2,30,3):
                z.append(float(df_union[j]))
        
        ### when data is broken
        else:
            

            df_drop_i_len = len(df_drop[i])
            
            if not df_drop_i_len >= 4:
                continue
            
            df_union2 = list(df_drop[i])
            
            
            extract_front = df_union2[0]
            target_front = r"\["
            regular_front = re.compile(target_front)
            
            extract_end = df_union2[df_drop_i_len-1]                 
            target_end = r"\]"
            regular_end = re.compile(target_end)
            
            target_D = r"D"
            regular_D = re.compile(target_D)
            
            target_hyphen = r"-"
            regular_hyphen = re.compile(target_hyphen)
                               
            
            hit_front = regular_front.search(str(extract_front))
            hit_end = regular_end.search(str(extract_end))

            
            # [ and ]
            if hit_end is None and hit_front is None:
################################################################################
                continue
            
            # x,y,z]
            elif not hit_end is None:
                extract_end = df_union2.pop()
#                        sys.stdout.write("extract_end:{}".format(extract_end))

                if len(extract_end)>2:
                    continue

                # except for ]
                add_string3 = float(extract_end[0:hit_end.start()])
                df_union2.append(add_string3)

                df_union2_lenlen = len(df_union2)
                

                # extract x,y,z
                for j in range(df_union2_lenlen-1,-1,-3):
                    hit_D_xxx = regular_D.search(str(df_union2[j]))
                    hit_hyphen_xxx = regular_hyphen.search(str(df_union2[j]))                          

                    if hit_D_xxx is None and hit_hyphen_xxx is None:
                        xxx.append(float(df_union2[j]))
            
                for j in range(df_union2_lenlen-2,-1,-3):
                    hit_D_yyy = regular_D.search(str(df_union2[j]))
                    hit_hyphen_yyy = regular_hyphen.search(str(df_union2[j]))                          

                    if hit_D_yyy is None and hit_hyphen_yyy is None:
                        yyy.append(float(df_union2[j]))
    
                for j in range(df_union2_lenlen -3,-1,-3):
                    hit_D_zzz = regular_D.search(str(df_union2[j]))
                    hit_hyphen_zzz = regular_hyphen.search(str(df_union2[j]))

                    if hit_D_zzz is None and hit_hyphen_zzz is None:
                        zzz.append(float(df_union2[j]))                                 
                                               
                count_zzz += 1
                
                list_num2 = []
                list_num2.append(len(xxx))
                list_num2.append(len(yyy))
                list_num2.append(len(zzz))
                list_min = min(list_num2)
                
                xxx = xxx[:list_min]
                yyy = yyy[:list_min]
                zzz = zzz[:list_min]
################################################################################
            # [x,y,z
            elif not hit_front is None: 
                micom_id = df_union2.pop(0)
                timestamp2 = float(df_union2.pop(0))
                extract_2 = df_union2.pop(0)
#                        sys.stdout.write("micom_id:{}".format(micom_id))
#                        sys.stdout.write("timestamp:{}".format(timestamp))
#                        sys.stdout.write("extract_2:{}".format(extract_2))
                
                                      
                # store id
                add_string4 = float(micom_id[hit_front.start()+1:])
                data_sets.append({'id':add_string4,'timestamp':timestamp2, 'data':df_union2})
                
                df_union2_len = len(df_union2)
                

                # extract x,y,z
                for j in range(0,df_union2_len,3):
                    hit_D_xx = regular_D.search(str(df_union2[j]))
                    hit_hyphen_xx = regular_hyphen.search(str(df_union2[j]))

                    if hit_D_xx is None and hit_hyphen_xx is None:
                        xx.append(float(df_union2[j]))
                    
                for j in range(1,df_union2_len,3):
                    hit_D_yy = regular_D.search(str(df_union2[j]))
                    hit_hyphen_yy = regular_hyphen.search(str(df_union2[j]))

                    if hit_D_yy is None and hit_hyphen_yy is None:
                        yy.append(float(df_union2[j]))
           
            
                for j in range(2,df_union2_len,3):
                    hit_D_zz = regular_D.search(str(df_union2[j]))
                    hit_hyphen_zz = regular_hyphen.search(str(df_union2[j]))

                    if hit_D_zz is None and hit_hyphen_zz is None:
                        zz.append(float(df_union2[j]))
                    
                list_num = []
                list_num.append(len(xx))
                list_num.append(len(yy))
                list_num.append(len(zz))
                list_min = min(list_num)
                xx = xx[:list_min]
                yy = yy[:list_min]
                zz = zz[:list_min]
                count_zz += 1
                
        #sys.stdout.write("left to right:%s" % count_zz)
        #sys.stdout.write("right to left:%s" % count_zzz)


        x_len = len(x) + len(xx) + len(xxx)
        y_len = len(y) + len(yy) + len(yyy)
        z_len = len(z) + len(zz) + len(zzz)
        #sys.stdout.write("extract_quantity_x:{}".format(x_len))
        #sys.stdout.write("extract_quantity_y:{}".format(y_len))
        #sys.stdout.write("extract_quantity_z:{}".format(z_len))

        a = []
        b = []
        c = []
        a.extend(x)
        a.extend(xx)
        a.extend(xxx)

        b.extend(y)
        b.extend(yy)
        b.extend(yyy)

        c.extend(z)
        c.extend(zz)
        c.extend(zzz)

    sum_x = []
    sum_y = []
    sum_z = []
    if len(a) >= 800 and len(b) >= 800 and len(c) >= 800:	
        sum_x = a[0:800]
        sum_y = b[0:800]
        sum_z = c[0:800]
    
        df_union_d = pd.DataFrame({"x":sum_x,
                                   "y":sum_y,
                                   "z":sum_z})
           
        fileProsessing = "/home/orange/workspace/result/processing.csv"
        df_union_d.to_csv(fileProsessing, mode='w',header=None)
    else:
        sys.exit("fairular:<=800")
      
    #########################################################
    if os.path.isfile(fileProsessing):
        filePros = "/home/orange/workspace/result/processing.csv"
        f = open(filePros, 'r')
    else:
        sys.exit("failure-filePros")
        
    
     
    acc_list = [[], [], []]
    for line in f:
        values = line.strip().split(',')
        acc_list[0].append(float(values[1]))
        acc_list[1].append(float(values[2]))
        acc_list[2].append(float(values[3]))
    
    f.close()
    
    
    inputs = [ ]
    input = []
    for i in range(0,3):
        coeffs = pywt.wavedec(acc_list[i], 'db1', level=7)
        input.extend(coeffs[0])
    
    inputs.append(input)
    #label.append(dir_index)
    
    inputs = np.array(inputs)
    #label = np.array(label)
    
    clfPath = "/home/orange/workspace/model/knn_clf"
    
    if os.path.isfile(clfPath):
        clf = joblib.load(clfPath)
        #sys.stdout.write(clf)
    else:
        sys.stdout.write("fairular-clf")
        sys.exit("fairular-clf")
        
    k = 3
    distset = clf.kneighbors(inputs,k)[0]
    
    threshold = 120
    status = 'normal'
    dist=0
    for dists in distset:
        #data_index += 1
        for d in dists:
            #sys.stdout.write(str(d) + "\n")
    
            if d > threshold:
                status = 'warning'
                break
            dist = d
    
    #sys.stdout.write(status+': '+ str(dir_index)+' dist: '+str(d)+"\n")
    #sys.stdout.write('file: '+ file_name +' position: '+str(pos)+"\n")
    
    html="""
    <html>
    <head>
    <title>knn_clf</title>
    <meta charset='utf-8'></meta>
    </head>
    <body>
    %s
    </body>
    </html>
    """
    
    import urllib.request, urllib.parse
    
    req = urllib.request.Request("https://android.googleapis.com/gcm/send")
    req.add_header("Authorization", "key=AIzaSyCO3NJALjY_0HAUHA_yIn7Hhe4QFRTvFY4")
    req.add_header("Content-Type", "application/json")
    #data = {"registration_ids":["APA91bHm4beFO0ULZqXhjNib153b9Fvq93hWA9oOL2yeSQyEWl9DXoHYAOdTNpHsj-DriZzLHqM20BKDND_J899SZY7h0prBbrap18Wf4S3FtZF6Q6ExqsP3ig2xT1EI2ea0iEos2B0h"], "data":{"message":'class: '+dir_name[result[0]]+' file: '+ file_name +' position: '+str(pos)}}
    if status == 'warning':
        data = {"registration_ids":["APA91bHfTgUAVoSOqtLFijXSwthbX8XsXeIUW3IZRHfustGLp1MNylf8txWJhwisqJJEVele6ap-yPw4gBtEKlpbUJ6fr0KNWrw7E171KpYgTsIgflUKeb6Tn9D38EnPTlLDx7KugZR7"], "data":{"message":str(time) + 'warning'}}
        sys.stdout.write(html % 'warning')
        #sys.exit("warning!")

    else:
        data = {"registration_ids":["APA91bHfTgUAVoSOqtLFijXSwthbX8XsXeIUW3IZRHfustGLp1MNylf8txWJhwisqJJEVele6ap-yPw4gBtEKlpbUJ6fr0KNWrw7E171KpYgTsIgflUKeb6Tn9D38EnPTlLDx7KugZR7"], "data":{"message":str(time) + 'door-open'}}
        sys.stdout.write(html %'door-open')
        #sys.exit("door-open")
    #data = {"registration_ids":["APA91bGy0YPLE6jUQx9nkJRT-YzNqKWTB234Oi38qheK0d7AskRcEwR5AJndbJgpeFTMy4Iou-9ZhoGGyRovlIeAK50pTojCRWWiHviUgOkr7RlW3HHodgxAOU9woXGAjXrHdUATEFdk", "APA91bGgf-tkVGS9R-8FkqB0NTnmS_4roosZfsZXoPVBDzue095WpbmvsecRYbIe3qao1KlyPMwlg-T9uHq_2UlKhWA7ZRSRJ1w1UyOSSp8qTTZe8RYaNpkpUf8anUs6jJCXq1uaVjmC"], "data":{"message":'class: '+class_name[result[0]]+' file: '+ file_name +' position: '+str(pos)}}
    
   
    
    import json
    json_data = json.dumps(data).encode('utf8')
    #data = urllib.parse.urlencode({}).encode("utf-8")
    with urllib.request.urlopen(req, json_data) as res:
        html = res.read().decode("utf-8")
        #sys.stdout.write(html)

#import logging
#logging.basicConfig(filename='example.log',level=logging.INFO)
#logging.info("TAG",str(form))
#logging.info("aaaaaaa")
