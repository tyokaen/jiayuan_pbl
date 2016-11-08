#!/usr/bin/env python3


html='''
<!DOCTYPE html>
<html><body>
name: %s
mail:%s
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

print("Content-Type: text/html\n")
#if not getvalue('name','not found') and not getvalue('name', 'not found'):
print(html % (form['name'].value, form['mail'].value))

# ファイル書き込み処理

file = open("result/test.txt",'w')
file.write(form['name'].value + ','+ form['mail'].value)
file.close()
print('write')

