html='''<html>
<head>
<meta charset="utf-8"></meta>
<title>Form test</title>
</head>

<body>
<h1>Python Form test</h1><hr> 
<form name="Form" method="POST" action="form.py">
name:<input type="text" size="30" name="name">
mail:<input type="text" size="30" name="mail">
<input type="submit" value="send" name="button">
</form>
</body>
</html>
'''
print(html)