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
form = cgi.FieldStorage()
import cgitb
cgitb.enable()

print("Content-Type: text/html\n")
print('<br>')

print("form['file']")
print(form['file'])
print('<br>')

print("form['file'].value")
print(form['file'].value)
print('<br>')

print("form['file'].name")
print(form['file'].name)
print('<br>')

print("form['file'].filename")
print(form['file'].filename)
print('<br>')

fileName = "result.txt"

from struct import unpack
if 'file' in form:
	print('has_key')
	print('<br>')

	item = form['file']
	print("item.file")
	print(item.file)
	print('<br>')

	if item.file:
		#print('before_open')
		filePath = open(fileName, 'wb')		
		#fileData = file.item.read()
		fileData = form['file'].value
		print("filePath")
		print(filePath)
		print('<br>')

		print("filePath")
		print(fileData)
		print('<br>') 

		filePath.write(fileData)
		#print('finish')
		filePath.close()

print('<br>')
print("getFileName:[")
print(fileName)
print("]")
print("-->")
print("saveFileName:[")
print(form['file'].filename)
print("]")


