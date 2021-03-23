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
	print('🐛 debug１')
	print('🐛 res：' + res)

	# 音声認識の区切りである「改行+.」がくるまで待つ
	while (res.find('\n.') == -1):
		# Juliusから取得した値を格納していく
		res += sock.recv(1024)
		print('🐛 debug２')
		print('🐛 res：' + res)

	word = ''
	for line in res.split('\n'):
		print('🐛 debug３')
		print('🐛 res：' + res)
		print('🐛 line：' + line)

		# Juliusから取得した値から認識文字列の行を探す
		index = line.find('WORD=')
		# 認識文字列があった場合
		if index != -1:
			# 認識文字列部分だけを抜き取る
			line = line[index + 6 : line.find('"', index + 6)]
			print('🐛 debug４')
			print('🐛 line：' + line)

			# 文字列の開始記号以外を格納していく
			if line != '[s]':
				# Note: おはようの次はおはよう[/s]となる
				word = word + line
				print('🐛 debug５')
				print('🐛 word：' + word)

		if word == 'おはよう':
			print('🐛 debug６')
			time.sleep(2)

			# TODO: バラバラになってしまった💬の処理をまとめる

			# 💬挨拶の読み上げ
			morning_greet = u'おはよう！睡眠の記録を終了するよ。今日も一日頑張っていきまっしょい。'
			# jtalk.generate_jtalk(morning_greet, 'talk_morning') # NOTE: 静的ファイルなので初回のみ生成
			talk_morning = jtalk.speech_jtalk('talk_morning')

			# FIXME: debug用にコメントアウト
			# Toggl trackの記録を終了
			# id = toggl.get_running_time_entry()
			# if id is not None:
			# 	r = toggl.stop(id)

			# 💬次の音声の生成
			# jtalk.generate_jtalk(u'今日の天気や予定を読み上げるよ。調べるからちょっと待ってねぇ。', 'talk_announce') # NOTE: 静的ファイルなので初回のみ生成

			# 💬前の再生が終わるのを待って次の次のトークの読み上げ
			talk_morning.wait()
			talk_announce = jtalk.speech_jtalk('talk_announce')

			weather_text = ''
			# 日付の読み上げをセット
			dt = datetime.datetime.now()
			weather_text += str(dt.year) + u'年' + str(dt.month) + u'月' + str(dt.day) + u'日。'

			# 天気の読み上げをセット
			weather = open_weather.getWeather(weather_key)
			try:
				weather_text += weather['city']['name'] + u'の正午の天気は、'
				weather_text += weather['list'][0]['weather'][0]['description'] + u'。'
				weather_text += u'最高気温は、' + str(weather['list'][0]['main']['temp_max']) + u'度。'
				weather_text += u'最低気温は、' + str(weather['list'][0]['main']['temp_min']) + u'度。'
				weather_text += u'15時の天気は、' + weather['list'][1]['weather'][0]['description'] + u'だよ。'
			except TypeError:
				print('💥Error: open weather type error')
				pass
			
			# 💬次の音声の生成
			jtalk.generate_jtalk(weather_text, 'talk_weather')

			# 💬前の再生が終わるのを待って次の次のトークの読み上げ
			talk_announce.wait()
			talk_weather = jtalk.speech_jtalk('talk_weather')
			
			# カレンダーの読み上げをセット
			calendar_text = ''
			events = google_calender.get_events()
			calendar_text += u'今日の予定は、' + events + u'だよ。'

			# 💬次の音声の生成
			jtalk.generate_jtalk(calendar_text, 'talk_event')

			# 💬前の再生が終わるのを待って次の次のトークの読み上げ
			talk_weather.wait()
			talk_event = jtalk.speech_jtalk('talk_event')
			
			# 💬次の音声の生成
			# jtalk.generate_jtalk(u'おしまい。いってらっしゃーい！', 'talk_finish') # NOTE: 静的ファイルなので初回のみ生成

			# 💬前の再生が終わるのを待って次の次のトークの読み上げ
			talk_event.wait()
			talk_finish = jtalk.speech_jtalk('talk_finish')

			# 💬前の再生が終わるのを待つ
			talk_finish.wait()

		elif word == 'おやすみ':
			time.sleep(2)
			# 挨拶の読み上げ
			# jtalk.generate_jtalk(u'睡眠の記録を開始するよ。今日も1日お疲れ様！おやすみまる。', 'talk_night')  # NOTE: 静的ファイルなので初回のみ生成
			talk_night = jtalk.speech_jtalk('talk_night')

			# TODO: 仮でコメントアウト
			# Toggl trackに記録を開始
			# id = toggl.get_running_time_entry()
			# if id is not None:
			# 	r = toggl.stop(id)
			# toggl.start("睡眠", 168180846) # ベタがき

			# 💬前の再生が終わるのを待つ
			talk_night.wait()

		print('🐛 debug６')
		print('🐛 res：' + res)
		res = ''
		print('🐛 debug７')
		print('🐛 res：' + res)
