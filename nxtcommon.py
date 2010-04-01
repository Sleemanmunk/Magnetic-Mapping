import nxt.locator
from threading import Thread
from nxt.sensor import *
from nxt.motor import *
from time import sleep
import sys

BASE_SPEED=50

DEFAULT_TESTS=2

def find_bot(NXTmac='00:16:53:06:EA:61'):
	print 'Looking for brick ...'
	sock = nxt.locator.find_one_brick(host=NXTmac,name='NXT')
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
