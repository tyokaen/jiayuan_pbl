#!/usr/bin/env python

import os
from sklearn import neighbors
import numpy as np
from sklearn.externals import joblib
import random
import pywt

#todo modelのパスを合わせる

f = open(dir_path+file, 'r')
acc_list = [[], [], []]
for line in f:
	values = line.strip().split(',')
	acc_list[0].append(int(values[1]))
	acc_list[1].append(int(values[2]))
	acc_list[2].append(int(values[3]))

f.close()

input = []
for i in range(0,3):
	coeffs = pywt.wavedec(acc_list[i], 'db1', level=7)
	input.extend(coeffs[0])

inputs.append(input)
label.append(dir_index)

inputs = np.array(inputs)
label = np.array(label)
clf = joblib.load('model\\knn_clf')
k = 3
distset = clf.kneighbors(inputs,k)[0]

threshold = 120
status = 'normal'
dist=0
for dists in distset:
    #data_index += 1
    for d in dists:
        #print(str(d) + "\n")

        if d > threshold:
            status = 'warning!'
            break
        dist = d

print(status+': '+ str(dir_index)+' dist: '+str(d)+"\n")
print('file: '+ file_name +' position: '+str(pos)+"\n")

import cgi
form=cgi.FieldStorage()

import urllib.request, urllib.parse

req = urllib.request.Request("https://android.googleapis.com/gcm/send")
req.add_header("Authorization", "key=AIzaSyCO3NJALjY_0HAUHA_yIn7Hhe4QFRTvFY4")
req.add_header("Content-Type", "application/json")
data = {"registration_ids":["APA91bHm4beFO0ULZqXhjNib153b9Fvq93hWA9oOL2yeSQyEWl9DXoHYAOdTNpHsj-DriZzLHqM20BKDND_J899SZY7h0prBbrap18Wf4S3FtZF6Q6ExqsP3ig2xT1EI2ea0iEos2B0h"], "data":{"message":'class: '+dir_name[result[0]]+' file: '+ file_name +' position: '+str(pos)}}
import json
json_data = json.dumps(data).encode('utf8')
#data = urllib.parse.urlencode({}).encode("utf-8")
with urllib.request.urlopen(req, json_data) as res:
    html = res.read().decode("utf-8")
    print(html)
#print (form['data'].value)
