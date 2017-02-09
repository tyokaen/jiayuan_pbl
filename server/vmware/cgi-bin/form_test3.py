#!/usr/bin/env python3

print('Content-type: text/html; charset=UTF-8 \r\n')


html='''
<!doctype html>
<html>
<head>
<meta charset="utf-8"></meta>
<title>通知テスト（バイナリ）</title>
</head>
<body>
<h1>通知テスト</h1>
<h2>データ処理の流れ：（バイナリ⇒線形補間⇒ウェーブレット変換⇒k近傍法）</h2>
<fieldset>
<legend>通知テスト使い方</legend>
<h3>
	<ol>
	<li>「file」には、バイナリの3軸加速度データを選択</li>
	<li>「send」を押してください</li>
	</ol>
</h3>
</fieldset>

<pre>


</pre>
<form name="Form" method="POST" enctype="multipart/form-data" action="form8.py">
file:<input type="file" size="30" name="jiayuan">
<input type="submit" value="send" name="button">
</form>
<pre>


</pre>
<hr>



<h3>「send」を押しても何も出力されない場合以下の原因が考えられます。</h3>
<ul>
	<li><b>IDが異なる場合</b></li>
	form8.pyのプログラムのmicon_idを変更する必要があります。
	<li><b>入力ファイルフォーマットが異なる場合</b></li>
	バイナリデータか確認をお願い致します。
	<li><b>データ数の不足</b></li>
	異なるファイルでお試しください。
</ul>
<hr>
</form>
</body>
</html>
'''

print(html)