"micom_light", "monostick_light"の両ディレクトリには、TWELITEを動かす上で特に重要なプログラムファイルをまとめた。<br><br>

実際に、プログラムを修正し、TWELITEの挙動を変えるためには、<br>
"_light"が付いていない"twelite"(中継器ソースコード), "twelite2525"（マイコンソースコード）の両ディレクトリをTWESDKへインポートすることになる。<br>
インポートする方法などの環境構築やプログラミング開発方法はTWESDK付属のドキュメントに掲載されている。<br>

このTWESDK付属のドキュメント(ToCoNet_SDK_manual_20xxxx-x.pdfのようなファイル名)でカバーされていない加速度計についての技術情報は以下のPDFに掲載されている。<br>
(*) http://www.analog.com/media/jp/technical-documentation/data-sheets/ADXL345_jp.pdf <br>
このPDFの26ページ（文書自体の23ページ）から29ページ（文書自体の26ページ）と、<br>
https://github.com/tsukuba-pbl/16-1/blob/twesdk-src/twe-lite/twelite2525/micom/Source/ADXL345_LowEnergy.c <br>
の87行目から記述されている関数"bADXL345_LowEnergy_Setting"の内容を見比べることで、あらゆるパラメーターを変更することができる。<br><br>

その他、上記の資料から読み取りにくい実装方法について以下にまとめる。<br>
1.測定周波数の変更について<br>
マイコン本体と、加速度計の２つの周期を変更できる。<br>
マイコン本体部ではsToCoNet_AppContext.u16TickHz（TWESDK付属のドキュメントに説明有）を変更する。<br>
加速度計では上記の関数"bADXL345_LowEnergy_Setting"内で加速度レジスタアドレス0x2C（プログラム内では定数"ADXL345_BW_RATE"）の値を変更する（上のPDF(*)に説明有）。
<br><br>
2.加速度データをAndroidへ送信する際のモード（文字列｜バイナリ）について<br>
現時点で正確に実装できていない。<br>
Monostickからシリアル送信するためのライブラリ関数は文字列を送信するためのものである。<br>
加速度は本来数値型であるが、この関数を使うために文字型(char)として扱った。<br>
68バイトの加速度データ（10時刻分）を68バイトの文字列（char[68]）として送信している。<br>
文字列では0x00が終端文字として扱われるために、加速度の値が０であるものは他の数値へ変換してから送信しなければならない。<br>
