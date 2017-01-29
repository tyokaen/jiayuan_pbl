"micom_light", "monostick_light"の両ディレクトリには、TWELITEを動かす上で特に重要なプログラムファイルをまとめた。

実際に、プログラムを修正し、TWELITEの挙動を変えるためには、
"_light"が付いていない"twelite"(中継器ソースコード), "twelite2525"（マイコンソースコード）の両ディレクトリをTWESDKへインポートすることになる。
インポートする方法などの環境構築やプログラミング開発方法はTWESDK付属のドキュメントに掲載されている。

このTWESDK付属のドキュメント(ToCoNet_SDK_manual_20xxxx-x.pdfのようなファイル名)でカバーされていない加速度計についての技術情報は以下のPDFに掲載されている
http://www.analog.com/media/jp/technical-documentation/data-sheets/ADXL345_jp.pdf  (*)
このPDFの26ページ（文書自体の23ページ）から29ページ（文書自体の26ページ）と、
https://github.com/tsukuba-pbl/16-1/blob/twesdk-src/twe-lite/twelite2525/micom/Source/ADXL345_LowEnergy.c
の87行目から記述されている関数"bADXL345_LowEnergy_Setting"の内容を見比べることで、あらゆるパラメーターを変更することができる。

その他、上記の資料から読み取りにくい実装方法について以下にまとめる。
1.測定周波数の変更について
マイコン本体と、加速度計の２つの周期を変更できる。
マイコン本体部ではsToCoNet_AppContext.u16TickHz（TWESDK付属のドキュメントに説明有）を変更する。
加速度計では上記の関数"bADXL345_LowEnergy_Setting"内で加速度レジスタアドレス0x2C（プログラム内では定数"ADXL345_BW_RATE"）の値を変更する（上のPDF(*)に説明有）。

2.加速度データをAndroidへ送信する際のモード（文字列｜バイナリ）について
現時点で正確に実装できていない。
Monostickからシリアル送信するためのライブラリ関数は文字列を送信するためのものである。
加速度は本来数値型であるが、この関数を使うために文字型(char)として扱った。
68バイトの加速度データ（10時刻分）を68バイトの文字列（char[68]）として送信している。
文字列では0x00が終端文字として扱われるために、加速度の値が０であるものは他の数値へ変換してから送信しなければならない。
