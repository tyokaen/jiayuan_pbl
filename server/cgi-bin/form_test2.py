#!/usr/bin/env python3

print('Content-type: text/html; charset=UTF-8 \r\n')


html='''<html>
<head>
<meta charset="utf-8"></meta>
<title>Form test</title>
</head>
<body>
<h1>通知テスト</h1><hr> 
<form name="Form" method="POST"enctype="multipart/form-data" action="form3.py">
file:<input type="file" size="30" name="jiayuan">
<input type="submit" value="send" name="button">
</form>
</body>
</html>
'''

print(html)
