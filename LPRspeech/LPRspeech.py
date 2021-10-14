import win32com.client
import math


speaker = win32com.client.Dispatch("SAPI.SpVoice")

def ensay(number):
	speaker.Speak("车牌号{}, 欢迎光临".format(number))

def exsay(number,time,fee):
	hour,minute = int(time//1),math.ceil((time%1)*60)
	speaker.Speak("车牌号{0},停车{1}时{2}分,收费{3}元,一路顺风".format(number,hour,minute,fee))

def paymentreminder():
	speaker.Speak("余额不足请充值")

def balance(number,payment):
	speaker.Speak("用户{0}，余额{1}".format(number,payment))

def say(word):
	speaker.Speak(word)