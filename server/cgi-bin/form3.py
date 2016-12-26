#!/usr/bin/env python3

import sys
import cgi
import os
#import pandas as pd
import csv
#import re
form = cgi.FieldStorage()
import cgitb
cgitb.enable()
#import datetime
#from sklearn import neighbors
import numpy as np
from sklearn.externals import joblib
import pywt

#sys.stdout.write('Content-type: text/html; charset=UTF-8 \r\n')
sys.stdout.write('Content-type: text/html; charset=UTF-8\n')

#print(os.getcwd())
#save_dir = ['result']
#cwd = os.getcwd() +'\\'+ save_dir[0] + '\\'
#print(cwd)


cd = "/home/orange/workspace/result/"

if not 'jiayuan' in form:
    sys.exit("failure-jiayuan")


if 'jiayuan' in form:
    getName = cd + form['jiayuan'].filename
    file_name = form['jiayuan'].filename

    filePath = open(getName, 'wb')        
    fileData = form['jiayuan'].value
    filePath.write(fileData)
    filePath.close()

#    dirName = "/home/orange/workspace/result/"
 
#    for file in files:
#    file = getName
    f = open(getName, 'rb')
    acc_list = [[], [], []]

    for line in f:
        signal = str(line).replace('\\x00', "").split(',')[6:]
        if len(signal) == 27:
            #print(len(signal))
            signal[-1] = signal[-1].replace("\\r\\n", "").replace("]'", "").replace("'", "")

            for i in range(27):
                acc_list[i%3].append(signal[i])
    f.close()

    ACC_THRESHOLD = 900

    for i in acc_list:
        #sys.exit(str(len(i)))
        if len(i) <= ACC_THRESHOLD:
            sys.exit("acc_list <= " + str(ACC_THRESHOLD))


    dec = 0
    for i in range(3):
        for j in range(len(acc_list[i])):
            if j < len(acc_list[i])-dec:
                if not acc_list[i][j] or acc_list[i][j] =='-':
                    dec += j%3
                    for k in range(3):
                        acc_list[i].pop(j-j%3+k)


    f = open(getName[:-3]+"a.csv", 'w')
    csvWriter = csv.writer(f)

    inputs = []
    input = []
    for i in range(0,3):
        coeffs = pywt.wavedec(acc_list[i], 'db1', level=7)
        #sys.exit(coeffs[0])
        #input.extend(coeffs[0][0:9])
        input.extend(coeffs[0][0:10])
        #sys.exit(input)
        
        print(len(coeffs))
        #csvWriter.writerow(coeffs[0][0:9])
        csvWriter.writerow(coeffs[0][0:10])

    f.close()
    #sys.exit(input)


    inputs.append(input)
    
    inputs = np.array(inputs)
    
    clfPath = "/home/orange/workspace/model/knn_clf"
    
    if os.path.isfile(clfPath):
        clf = joblib.load(clfPath)
    else:
        sys.stdout.write("fairular-clf")
        sys.exit("fairular-clf")
        
    k = 3
    #sys.exit(inputs)
    distset = clf.kneighbors(inputs,k)[0]

    
    #threshold = 185 # model_10    
    threshold = 110 # 12_18_v2 model_10
    status = 'normal'
    dist=0
    for dists in distset:
        for d in dists:
            if d > threshold:
                status = 'warning'
                break
            dist = d
    #sys.exit('distset:'+ str(distset))
    #sys.exit('dist:'+ str(dist))

    
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
    if status == 'warning':
        data = {"registration_ids":["APA91bE5eguxZPbeXa12yZt0cHfa3yZJJ5MAqIiNTPl5VWgcrn_D55CoeCVd49OEDY7oEmZ3xHickGvD53_ZOvfg10KChSedHupsl7j38MZaJkMST9mWi5r3CVzTHQ5OlpUCGDBNF6kD"], "data":{"message":str(file_name) + 'warning'}}
        sys.stdout.write(html % 'warning')
        #sys.exit("warning!")
    else:
        data = {"registration_ids":["APA91bE5eguxZPbeXa12yZt0cHfa3yZJJ5MAqIiNTPl5VWgcrn_D55CoeCVd49OEDY7oEmZ3xHickGvD53_ZOvfg10KChSedHupsl7j38MZaJkMST9mWi5r3CVzTHQ5OlpUCGDBNF6kD"], "data":{"message":str(file_name) + 'door-open'}}
        sys.stdout.write(html %'door-open')
        #sys.exit("door-open")
     
    import json
    json_data = json.dumps(data).encode('utf8')
    with urllib.request.urlopen(req, json_data) as res:
        html = res.read().decode("utf-8")
        #sys.stdout.write(html)
