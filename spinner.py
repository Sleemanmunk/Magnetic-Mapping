#!/usr/bin/env python

import nxt.locator
from nxt.sensor import *
from nxt.motor import *
from nxt.hicompass import *

PORT_A = 0x00
PORT_B = 0x01
PORT_C = 0x02
envLight = 0
beaconDir = 0

def run_calibrator(compasses):
	print 'Looking for brick 5 ...'
	sock = nxt.locator.find_one_brick(host='00:16:53:06:F2:8E', name='Group5')
	print 'Found brick 5 or timed-out ...'
	if sock:
		for compass in compasses:
			compass.calibrate_mode()
		b=sock.connect()
		motor1 = Motor(b, PORT_A)
		motor1.run(25)
		sleep(20)
		Motor(b,PORT_A).stop()
		sock.close()
		for compass in compasses:
			compass.measure_mode()
		exit         
	else:
		print 'No NXT bricks found'
		exit

