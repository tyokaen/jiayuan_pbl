#!/usr/bin/env python

import os
from sklearn import neighbors
import numpy as np
from sklearn.externals import joblib
import random
import pywt

"""print('Content-type: text/html; charset=UTF-8\r\n')
print('Hello, World!\n')


dir_name = ['dondon', 'open']
inputs = []
label = []
dir_index = random.randint(0, 1)
dir_path = 'C:\\Users\\NakagawaMasafumi\\Documents\\data\\'+dir_name[dir_index]+'\\'
files = os.listdir(dir_path)

rnd = random.randint(1, 4)
line_for_rnd = 0
pos = 0
file_name = ''
for file in files:
	line_for_rnd += 1
	if line_for_rnd != rnd:
		continue
	file_name = file"""
f = open(dir_path+file, 'r')
acc_list = [[], [], []]
	"""pos = random.randint(0,175000)
	index = 0"""
for line in f:
		"""if index >= pos + 5000:
			break
		if index >= pos:
			#print (line)"""
	values = line.strip().split(',')
	acc_list[0].append(int(values[1]))
	acc_list[1].append(int(values[2]))
	acc_list[2].append(int(values[3]))

		#index = index + 1

f.close()

input = []
for i in range(0,3):
	coeffs = pywt.wavedec(acc_list[i], 'db1', level=7)
	input.extend(coeffs[0])

	"""index = 0
	input = []
	row = 1
	for line in f:
		if row % 2 == 1:
			values = line.strip().split(',')
			values = list(map(float, values))
			#if len(values) != 5:
			#	print(file+str(re)+'/'+str(len(values)))
			input.extend(values)
		row += 1"""
	#i=0
inputs.append(input)
	#label.append(class_label)
label.append(dir_index)
	#break;
	#f.close()

inputs = np.array(inputs)
label = np.array(label)
"""indices = np.random.permutation(len(inputs))
inputs_test = inputs[indices[-1:]]
label_test = label[indices[-1:]]"""
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
