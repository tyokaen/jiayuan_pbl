#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print('Content-type: text/html\n')

html='''
<!doctype html>
<html>                                                                                                                                                                                                    
  
<head>
<meta charset="utf-8"></meta>
<title>Form test</title>
</head>

<body> 
<h1>線形補間テスト</h1><hr>
<form name="Form" method="POST" enctype="multipart/form-data" action="form7.py">
file:<input type="file" size="30" name="jiayuan">
<input type="submit" value="send" name="button">
</form>
</body>

</html>
'''

print(html)

