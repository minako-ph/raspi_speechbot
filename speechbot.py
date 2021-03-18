# -*- coding: utf-8 -*-
import socket
import time
import picamera
import subprocess
import jtalk
import random
from dotenv import load_dotenv
import os
import toggl_driver

# Toggl Trackの準備
load_dotenv()
toggl_token = os.getenv('TOGGL_API')
toggl = toggl_driver.TogglDriver(_token=toggl_token)

# Juliusに接続する準備
host = 'localhost'
port = 10500
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
		# 認識文字列があった場合
		if index != -1:
			# 認識文字列部分だけを抜き取る
			line = line[index + 6 : line.find('"', index + 6)]
			# 文字列の開始記号以外を格納していく
			if line != '[s]':
				# Note: おはようの次はおはよう[/s]となる
				word = word + line
				print('🐛 word：' + word)

		if word == 'おはよう':
			# 挨拶にランダムで使いたい文字列
			morning_greet = [u'おはよう', u'おはまる', u'おはぴよ', u'おっはー']
			jtalk.jtalk(random.choice(morning_greet) + u'！睡眠の記録を終了するよ。今日も一日頑張っていきまっしょい。')

			# Toggl trackに記録を終了
			id = toggl.get_running_time_entry()
			if id is not None:
				r = toggl.stop(id)

		elif word == 'おやすみ':
			# 挨拶にランダムで使いたい文字列
			goodnight_greet = [u'おやすみ', u'おやすみまる', u'おやすみだぴよ', u'おやすー']
			jtalk.jtalk(u'睡眠の記録を開始するよ。今日も1日お疲れ様！' + random.choice(goodnight_greet))

			# Toggl trackに記録を開始
			id = toggl.get_running_time_entry()
			if id is not None:
				r = toggl.stop(id)
			toggl.start("睡眠")

		res = ''
