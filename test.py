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
				word = word + line
				print('🐛 word：' + word)

		# 文字列を認識したら...
		if word == 'おはよう':
			morning_word = [u'おはよう', u'おはまる', u'おはぴよ', u'おっはー']
			jtalk.jtalk(random.choice(morning_word))
		elif word == 'おやすみ':
			jtalk.jtalk(u'おやすみまる')
		res = ''
