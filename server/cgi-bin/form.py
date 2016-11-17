#!/usr/bin/env python3

print('Content-type: text/html; charset=UTF-8 \r\n')

html='''
<!DOCTYPE html>
<html><body>
<!--name: %s-->
</html></body>
'''

error_html='''
<!DOCTYPE html>
<html><body>
ERROR!
</html></body>
'''

import cgi
import os
print("os.getcwd()")
print(os.getcwd())
print('<br>')

form = cgi.FieldStorage()
import cgitb
cgitb.enable()

print("Content-Type: text/html\n")
print('<br>')

print("form['jiayuan']")
print(form['jiayuan'])
print('<br>')

print("form['jiayuan'].value")
print(form['jiayuan'].value)
print('<br>')

print("form['jiayuan'].name")
print(form['jiayuan'].name)
print('<br>')

print("form['jiayuan'].filename")
print(form['jiayuan'].filename)
print('<br>')

import datetime

cd = "/home/orange/workspace/result/result"
date= datetime.datetime.today()
year = str(date.year) + "_"
month = str(date.month)+ "_"
day = str(date.day)+ "_"
hour = str(date.hour)+ "h"
minute = str(date.minute)+"m"
second = str(date.second)+"s"

num_str = year + month + day+hour+minute+second
extension = ".csv"

fileName = cd + num_str + extension


from struct import unpack

if 'jiayuan' in form:
	print('has_key')
	print('<br>')

	item = form['jiayuan']
	print("item.file")
	print(item.file)
	print('<br>')

	if item.file:
		#print('before_open')
		filePath = open(fileName, 'wb')	
			
		#fileData = file.item.read()
		fileData = form['jiayuan'].value
		print("filePath")
		print(filePath)
		print('<br>')

		print("fileData")
		print(fileData)
		print('<br>')
		
		if os.path.exists(fileName):
			print("nameChange")
			
			
		filePath.write(fileData)
		#print('finish')
		filePath.close()

print('<br>')
print("getFileName:[")
print(form['jiayuan'].filename)
print("]")

print("-->")

print("saveFileName:[")
print(fileName)
print("]")


