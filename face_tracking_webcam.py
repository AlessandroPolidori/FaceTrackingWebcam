

import jetson.inference
import jetson.utils
import time
from adafruit_servokit import ServoKit



net = jetson.inference.detectNet("facenet-120", threshold=0.5)
camera = jetson.utils.videoSource("/dev/video0")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0")     # 'my_video.mp4' for file
window = 10
kit = ServoKit(channels=16)
width = 1280
height = 720
pan =100
tilt=140
kit.servo[0].angle = pan
kit.servo[1].angle = tilt

while display.IsStreaming():

	img = camera.Capture()
	detections = net.Detect(img)
	display.Render(img)
	
	if len(detections) > 0 and detections[0].ClassID==0 :
		
		
		c_x,c_y=detections[0].Center
		errPan = c_x - (width/2)
		errTilt = c_y - (height/2)
		if abs(errPan)>30:
			pan = pan-errPan/75
		if abs(errTilt)>30:
			tilt = tilt- errTilt/75
		if pan > 180:
			pan = 100
			tilt = 140
			time.sleep(1)
			print("pan out of range")
		if pan < 0:
			pan = 100
			tilt = 140
			time.sleep(1)
			print("pan out of range")
		if tilt > 180:
			pan = 100
			tilt = 140
			time.sleep(1)
			print("tilt out of range")
		if tilt < 0:
			pan = 100
			tilt = 140
			time.sleep(1)
			print("tilt out of range")
		kit.servo[0].angle = pan
		kit.servo[1].angle = tilt
