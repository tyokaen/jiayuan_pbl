#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print('Content-type: text/html\n')

html='''
<!doctype html>
<html>                                                                                                                                                                                                    
  
<head>
<meta charset="utf-8"></meta>
<title>通知テスト（文字列+補間）</title>
</head>

<body> 
<h1>通知テスト</h1>
<h2>データ処理の流れ：（文字列⇒線形補間⇒ウェーブレット変換⇒k近傍法）</h2>
<fieldset>
<legend>通知テスト使い方</legend>
<h3>
	<ol>
	<li>「file」には、文字列の3軸加速度データを選択</li>
	<li>「send」を押してください</li>
	</ol>
</h3>
</fieldset>

<pre>


</pre>
<form name="Form" method="POST" enctype="multipart/form-data" action="form7.py">
file:<input type="file" size="30" name="jiayuan">
<input type="submit" value="send" name="button">
</form>
<pre>


</pre>
<hr>



<h3>「send」を押しても何も出力されない場合以下の原因が考えられます。</h3>
<ul>
	<li><b>IDが異なる場合</b></li>
	form7.pyのプログラムのmicon_idを変更する必要があります。
	<li><b>入力ファイルフォーマットが異なる場合</b></li>
	文字列データか確認をお願い致します。
	<li><b>データ数の不足</b></li>
	異なるファイルでお試しください。
</ul>
<hr>


</body>

</html>
'''

print(html)

