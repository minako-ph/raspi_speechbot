#coding: utf-8
import subprocess
from datetime import datetime

def generate_jtalk(text, name):
    # 合成音声の作成
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/mei/mei_bashful.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow',name + '.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(text.encode('utf-8'))
    c.stdin.close()
    c.wait()

def speech_jtalk(name):
    # 音声の読み上げ
    aplay = ['aplay','-q',name + '.wav','-D','bluealsa']
    wr = subprocess.Popen(aplay)
    return wr

def say_datetime():
    d = datetime.now()
    text = u'%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
    jtalk(text)

if __name__ == '__main__':
    say_datetime()
