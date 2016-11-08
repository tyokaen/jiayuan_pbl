#!/usr/bin/env python3

print('Contet-type: text/html; charset=UTF-8 \r\n')


html='''<html>
<head>
<meta charset="utf-8"></meta>
<title>Form test</title>
</head>

<body>
<h1>Python Form test</h1><hr> 
<form name="Form" method="POST" enctype="multipart/form-data" action="form.py">
file:<input type="file" size="30" name="file">
<!-- name:<input type="text" size="30" name="name">-->
<input type="submit" value="send" name="button">
</form>
</body>
</html>
'''

print(html)