1. 	pip install opencv-python
	pip install numpy
	pip install pillow --upgrade
	pip install pyocr
	pip install oauth2client
	pip install gspread
	pip install configparser

2.Tesseractをインストールする（Japanese Scriptは4種チェックしておく）

3. config.iniに設定を記述

4. './.working'に作業したいファイルを入れる

5. main.pyの254行目のSPREAD_SHEET_KEY変数にスプレッドシートアクセストークンキーを入れる

6. 実行


※※注意※※
1. config.iniの中は'と"も単純な文字列として取得してしまう
2. 処理したいパスに日本語が含まれていると処理ができない（Pythonのバージョン上がった事によって現在は発生しないと思われる。）
3. 更新していないので動作はだいぶ想定とは違った結果となる可能性
4. ディレクトリ操作関連がごちゃついています。

作成時期：2021/04～2021/07
処女作です。
