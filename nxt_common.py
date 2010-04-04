# Allow us to locate the robot
import nxt.locator
# Allow multithreading
from threading import Thread
# Allow use of sensors
from nxt.sensor import *
# Allow use of motors
from nxt.motor import *
# Allow the robot to wait for certain time increments
from time import sleep
#
import sys
# Import everything relevant about the current bot
from bot_id import *

# 
BASE_SPEED=50

#
DEFAULT_TESTS=2

def find_bot(NXTmac):
	print 'Looking for brick ...'
	sock = nxt.locator.find_one_brick(host=NXTmac,name=NXTname)
	print 'Found brick or timed-out ...'
	if sock:
		print 'Connecting to the brick ...'
		bot = sock.connect()
		print 'Connected to the brick or timed-out ...'
		if bot:
			return bot
		else:
			print 'Could not connect to NXT brick'
			exit            
	else:
		print 'No NXT bricks found'
		exit

def stop_motors(bot):
	Motor(bot, PORT_ALL).stop(False)

def stop_bot(bot):
	stop_motors(bot)
	bot.sock.close()

def sense(sensor, tests = DEFAULT_TESTS):
	gathered = 0
	for i in range(0,tests):
		gathered += sensor.get_sample()
	return (gathered/tests)

def breakpoint(dodie,bot):
	if dodie:
		stop_bot(bot)
		exit()
