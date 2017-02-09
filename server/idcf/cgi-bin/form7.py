#!/usr/bin/env python3

import sys
import cgi
import os
import pandas as pd
import csv
import re
form = cgi.FieldStorage()
import cgitb
cgitb.enable()
#import datetime
import numpy as np
from sklearn.externals import joblib
import pywt

sys.stdout.write('Content-type: text/html; charset=UTF-8\n')

save_dir = ['result','model']
cd = os.getcwd() +'/'+ save_dir[0] + '/'

pattern = [r"^-?[0-9]{1,3}"]
r = re.compile(pattern[0])

def decideDelete(index,delete_idx,signal): 
    tmp_acc_list[index%3].append(1111) 
    if index%3 == 0:
        delete_idx += (index,index+1,index+2)
    elif index%3 == 1:
        delete_idx += (index-1,index,index+1)
    else:
        delete_idx += (index-2,index-1,index)
    # print("signal:{}------>del_index:{}".format(signal,delete_idx))
    return(delete_idx)

def deleteProcessing(delete_idx,tmp_acc_list,tmp_timestamps):
    # print("before_acc_list:{}".format(tmp_acc_list))                
    
    for i in delete_idx:
        # print("i:{}".format(i))
        del_idx = tmp_acc_list[i%3].pop(int(i/3))
        # print("acc_list_del:{}".format(del_idx))
        
        if i%3 == 0:
            # print("tmp_times:{}".format(tmp_timestamps))
            tmp_timestamps.pop(int(i/3))
    #         print("tmp_times:{}".format(tmp_timestamps))      
    # print("after_acc_list:{}".format(tmp_acc_list))
    
       
RANGE = 10
# linear_interpolation 
def linear(arg,axis):
    time = []
    y = []
    for j in range(0,int(len(acc_list[arg])/10)):     
        for i in range(0,RANGE):
    
            if j ==  int(len(acc_list[arg])/10)-1 and i == RANGE-1:
                y.append(acc_list[arg][i+(j*RANGE)])
                break
            
            # 2 degree equation
            # y1 = ax1 + b
            # y2 = ax2 + b
            # y = ax + b
            y1 = acc_list[arg][i +(j*RANGE)]
            y2 = acc_list[arg][i+1 + (j*RANGE)]
            x1 = timestamps[i+(j*(RANGE))]
            x2 = timestamps[i+1 + (j*(RANGE))]
                        
            a = (y1-y2) / (x1-x2)
            b = ((y2*x1) - (y1*x2)) / (x1-x2)

            tmp = timestamps[i+(j*(RANGE))] 
            
            for k in range(0,timestamps[i+1 + (j*RANGE)] - timestamps[i +(j*RANGE)]):
                y.append(round(a * tmp + b))
                tmp += 1
    
    data = []     
    time = []
    for i in range(0,len(y),3):
        data.append(y[i])
        time.append(timestamps[0]+i)
    
    return (time,data)


if not 'jiayuan' in form:
    sys.exit("failure-jiayuan")

if 'jiayuan' in form:
    getName = cd + form['jiayuan'].filename
    file_name = form['jiayuan'].filename

    filePath = open(getName, 'wb')        
    fileData = form['jiayuan'].value
    filePath.write(fileData)
    filePath.close()

    f = open(getName, 'rb')
    acc_list = [[], [], []] # acc_list[[x],[y],[z]] all data
    timestamps = [] # timestamps[time[ms]] all data 

    for line in f:
        tmp_acc_list = [[],[],[]] # tmp_acc_list = [[x],[y],[z]] 1 row data
        tmp_timestamps = []  # tmp_timestamps[time[ms]] 1 row data
        delete_idx = ()    # delete_idx(index)
        signal = str(line).replace(r'\x00', "").split(',') #signal= [id,timestamps,status,x,y,z,...,x,y,z] length=33 
        print(len(signal))
        
        if signal[0] == "b'[8102178b" and len(signal) > 2: # ID check               
            timestamp = int(signal[1])
            signal = signal[3:] 
                   
            if len(timestamps) > 0 and abs(timestamps[-1] - timestamp) > 1000: # timestamps (1000ms = 1s)
                timestamps = []
                acc_list = [[],[],[]]                    

            if len(signal)%3 != 0:
                print("before_signal_pop:{}".format(signal))
                for d in range(len(signal)%3):
                    sig_pop = signal.pop()
                print("after_signal_pop:{}".format(signal))
                  
            
            for i in range(len(signal)): # all value check            
                if i%3 == 0: # timestamps
                    tmp_timestamps.append(timestamp)
                    timestamp += 3

                match = r.search(signal[i])
                if not match is None: # value
#                            print("match:{}".format(match.group()))
                    tmp_acc_list[i%3].append(int(match.group()))                     
                else: # not value (decide the delete index)
                    delete_idx = decideDelete(i,delete_idx,signal)
                
            if len(delete_idx) != 0: # is delete_idx
                del_idx = list(delete_idx)
                del_idx.sort(reverse=True)
                deleteProcessing(del_idx,tmp_acc_list,tmp_timestamps)            
                
            for i in range(3):
                acc_list[i%3].extend(tmp_acc_list[i])
            timestamps.extend(tmp_timestamps)
    
    x_data = []
    y_data = []
    z_data = []
    t = []
    datas = [[],[],[]]
    
    t,x_data = linear(0,"x")
    t,y_data = linear(1,"y")
    t,z_data = linear(2,"z")
    
    datas[0].extend(x_data)
    datas[1].extend(y_data)
    datas[2].extend(z_data)

    #sys.exit(datas)
    acc_list = datas
    
    # out_f = open(cd + "linear_" + file_name, 'w')         
    # df = pd.DataFrame({"x":x_data,
    #                    "y":y_data,
    #                    "z":z_data}).T
    
    # df.to_csv(out_f,header=None,index=None)
    # out_f.close() 
                 
    f.close()

    ACC_THRESHOLD = 800

    for i in acc_list:
        #sys.exit(str(len(i)))
        if len(i) <= ACC_THRESHOLD:
            #sys.exit(strlen(i))
            sys.exit("acc_list"+ str(len(i)) +"<=" + str(ACC_THRESHOLD))

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
    
   #clfPath = "/home/orange/workspace/model/knn_clf"
    clfPath = os.getcwd() +'/' + save_dir[1] + '/knn_clf'
    #sys.exit(clfPath)

    
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

    import json
    import urllib.request
    
    APPNO = 'e3538b500de44713bbe6f33a5279f185'
    APIKEY = 'baa0c2564c1c4506b2a5f46120f72b69'
    endpoint = 'https://api.push7.jp/api/v1/{}/send'.format(APPNO)   
    header_send = {'Content-Type':'application/json'}
    method = 'POST'
    '''
    move_dirPath = "/root/workspace/movie/setting.txt"
    movefile = open(move_dirPath, "r")
    moveName = ""
    for filename in movefile:
        moveName = filename

    movePath = "http://215.129.63.215:8080/movie/" + moveName
    movefile.close()
    '''
    #sys.exit(movePath)
    
    if status == 'warning':
        data = {"registration_ids":["APA91bHnUBZDrqSbEeRhZ07q7CiIMUDU-WdXobTROb4G-JlLkmYjAR_RNuCxy20aS_qaJeT5Y0QrEelI7oK1z1qQTnJQQLFbYVryRkHSZMc_v1SnaF31IXVIxVA_tWT7S-TKEBLsnSyd"], "data":{"message":str(file_name) + 'warning'}}

        payload = {
                "apikey":APIKEY,
                "url":"http://210.129.63.215:8080/cgi-bin/hello.py",
                "icon":"http://210.129.63.215:8080/cgi-bin/orange_icon.jpg",
                "body":"warning",
                "title":"orange"
                }      
        json_data = json.dumps(payload,indent=4).encode("utf-8")
        request = urllib.request.Request(endpoint,data=json_data, method=method,headers=header_send)

        sys.stdout.write(html % 'warning')
        #sys.exit("warning!")
    else:
        data = {"registration_ids":["APA91bHnUBZDrqSbEeRhZ07q7CiIMUDU-WdXobTROb4G-JlLkmYjAR_RNuCxy20aS_qaJeT5Y0QrEelI7oK1z1qQTnJQQLFbYVryRkHSZMc_v1SnaF31IXVIxVA_tWT7S-TKEBLsnSyd"], "data":{"message":str(file_name) + 'door-open'}}
        sys.stdout.write(html % 'door-open')
        payload = {
                "apikey":APIKEY,
                "url":"http://210.129.63.215:8080/cgi-bin/form6.py",
                "icon":"http://210.129.63.215:8080/cgi-bin/orange_icon.jpg",
                "body":"door-open",
                "title":"orange"
                }    
        json_data = json.dumps(payload,indent=4).encode("utf-8")
        request = urllib.request.Request(endpoint,data=json_data, method=method,headers=header_send)

        #sys.exit("door-open")
     
    import json
    json_data = json.dumps(data).encode('utf8')
    with urllib.request.urlopen(req, json_data) as res:
        html = res.read().decode("utf-8")
        #sys.stdout.write(html)

    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        #print("response_body:{}".format(response_body))

        
