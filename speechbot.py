# -*- coding: utf-8 -*-
import socket
import time
import picamera
import subprocess
import jtalk
import random

host = 'localhost'
port = 10500

# Juliusに接続する準備
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

res = 	''
while True:
	# 音声認識の区切りである「改行+.」がくるまで待つ
	while (res.find('\n.') == -1):
		# Juliusから取得した値を格納していく
		res += sock.recv(1024)

	word = ''
	for line in res.split('\n'):
		# Juliusから取得した値から認識文字列の行を探す
		index = line.find('WORD=')
		# 認識文字列があったら...
		if index != -1:
			# 認識文字列部分だけを抜き取る
			line = line[index + 6 : line.find('"', index + 6)]
			# 文字列の開始記号以外を格納していく
			if line != '[s]':
				# note 最初はwordに[s]が入るので文字列認識条件文を通らない
				# その後のループは末尾に[/s]が着くので文字列認識条件文を通らない
				word = word + line
				print('🐛 word：' + word)

		# 文字列を認識したら...
		if word == 'おはよう':
			morning_word = [u'おはよう', u'おはまる', u'おはぴよ', u'おっはー']
			jtalk.jtalk(random.choice(morning_word))
			# jtalk.jtalk(u'睡眠の記録を終了したよ。')
			# jtalk.jtalk(u'今日も一日頑張っていきまっしょい。今日の情報を読み上げるね。')
			# jtalk.jtalk(u'今日の天気はxxxx 最高気温はxxxx 最低気温はxxxx。')
			# jtalk.jtalk(u'今日の予定はxxx時からxxx,xxx時からxxxだよ。')
			# jtalk.jtalk(u'今日のタスクはxxx, xxx, xxx だよ。')
		elif word == 'おやすみ':
			jtalk.jtalk(u'おやすみまる')
			# jtalk.jtalk('睡眠の記録を開始するよ。今日も1日お疲れ様！おやすみまる〜〜〜〜。')
		res = ''
