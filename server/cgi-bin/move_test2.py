#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print('Content-type: text/html\n')



html='''<html>
<head>
<meta charset="utf-8"></meta>
<title>Form test</title>
</head>

<body>
<h1>Python Form test</h1><hr> 
<form name="Form" method="POST" enctype="multipart/form-data" action="form6.py">
file:<input type="file" size="30" name="jiayuan">
<!-- name:<input type="text" size="30" name="name">-->
<input type="submit" value="send" name="button">
</form>
</body>
</html>
'''

print(html)
