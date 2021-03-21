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
import datetime
import open_weather
import google_calender

# Toggl Trackの準備
load_dotenv()
toggl_token = os.getenv('TOGGL_API')
toggl = toggl_driver.TogglDriver(_token=toggl_token)

# Open Weatherの準備
weather_key = os.getenv('WEATHER_API')

# Juliusに接続する準備
host = 'localhost'
port = 10500
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

res = ''
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
			# 挨拶の読み上げをセット
			morning_greet = [u'おはよう']
			jtalk.jtalk(random.choice(morning_greet) + u'！' + u'睡眠の記録を終了するよ。今日も一日頑張っていきまっしょい。')

			# TODO: 仮でコメントアウト
			# Toggl trackの記録を終了
			# id = toggl.get_running_time_entry()
			# if id is not None:
			# 	r = toggl.stop(id)

			jtalk.jtalk(u'今日の天気や予定を読み上げるよ。調べるからちょっと待ってねえ。')

			speech_text = ''
			# 日付の読み上げをセット
			dt = datetime.datetime.now()
			speech_text += str(dt.year) + u'年' + str(dt.month) + u'月' + str(dt.day) + u'日。'

			# 天気の読み上げをセット
			weather = open_weather.getWeather(weather_key)
			try:
				speech_text += weather['city']['name'] + u'の正午の天気は、'
				speech_text += weather['list'][0]['weather'][0]['description'] + u'。'
				speech_text += u'最高気温は、' + str(weather['list'][0]['main']['temp_max']) + u'度。'
				speech_text += u'最低気温は、' + str(weather['list'][0]['main']['temp_min']) + u'度。'
				speech_text += u'15時の天気は、' + weather['list'][1]['weather'][0]['description'] + u'だよ。'
			except TypeError:
				print('💥Error: open weather type error')
				pass
			
			# カレンダーの読み上げをセット
			events = google_calender.get_events()
			speech_text += u'今日の予定は、' + events + u'だよ。'

			speech_text += u'おしまい。いってらっしゃーい！'

			jtalk.jtalk(speech_text)

		elif word == 'おやすみ':
			# 挨拶の読み上げ
			goodnight_greet = [u'おやすみまる']
			jtalk.jtalk(u'睡眠の記録を開始するよ。今日も1日お疲れ様！' + random.choice(goodnight_greet))

			# TODO: 仮でコメントアウト
			# Toggl trackに記録を開始
			# id = toggl.get_running_time_entry()
			# if id is not None:
			# 	r = toggl.stop(id)
			# toggl.start("睡眠", 168180846) # ベタがき

		res = ''
