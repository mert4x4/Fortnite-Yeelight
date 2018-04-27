from PIL import ImageGrab
from PIL import Image
import time
from yeelight import *
import json

with open('config.json') as json_data_file:
    data = json.load(json_data_file)
print(data)

bulb = Bulb(data['bulb_ip'])	#yeelight ip
def GetPixelData(xFrom,xTo,y,rval,gval,bval):
	im = ImageGrab.grab()
	rgb_im = im.convert('RGB')
	for x in reversed(range(xFrom, xTo)):
		r, g, b = rgb_im.getpixel((x, y))
		if g>=gval and r>=rval and b>=bval:
			return x

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

bulb.start_music()#to send more than 60 requests
print "music mode:",bulb.music_mode

def StartFlow(red,green,blue,dur):
	transitions = [
	    RGBTransition(red, green,blue,duration = dur)
	]
	flow = Flow(
	    count=1,
	    action=Flow.actions.recover,
	    transitions=transitions
	)
	bulb.start_flow(flow)

healthData = 0
armorData = 0

while True:
	healthData_ = healthData
	armorData_ = armorData
	time.sleep(data['sleep_time'])
	health = GetPixelData(756,1187,966,78,170,53)
	armor = GetPixelData(756,1187,938,53,118,235)
	if health == None:
		health = 756
	if armor == None:
		armor = 756
	armorData = map(armor,756,1187,0,100)
	healthData = map(health,756,1187,0,100)
	if healthData_ > healthData or armorData_ > armorData:
		print healthData,armorData
		StartFlow(255,0,0,1000)
	elif healthData_ < healthData:
		print healthData,armorData
		StartFlow(0,255,0,1000)
	elif armorData_ < armorData:
		print healthData,armorData
		StartFlow(0,0,255,1000)
