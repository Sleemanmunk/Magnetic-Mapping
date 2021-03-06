from nxt_common import *
import record_data_lib as rdlib
import nxt.hicompass as hicompass
from time import time
from spinner import *

import curses as c
#Some notes about using curses:
#Curses creates a new window within the terminal.
#Everything you're working on will be temporarily erased
#and you will return to it when the program is finished.
#When in curses mode, instead of print, use screen.addstr

def sound(bot):		#sound to be played upon successful exectution of a process.
	sleep(2)
	bot.play_tone(900, 100)
	bot.play_tone(800, 100)
	bot.play_tone(700, 100)
	bot.play_tone(600, 100)
	bot.play_tone(500, 100)
	bot.play_tone(400, 100)
	bot.play_tone(1000, 200)


#Ports on NXT for sensors and a key for easy conversion to user-friendly output
SENSOR_PORTS = [PORT_1,PORT_2,PORT_3,PORT_4]
PORT_KEY = {PORT_1:"Port 1",PORT_2:"Port 2",PORT_3:"Port 3",PORT_4:"Port 4"}

#Constants for relevant keycodes
#Further keycodes may be determined with python's ord( char ) function
UP_ARROW=65
DOWN_ARROW=66
SPACEBAR=32
Q=113
W=ord("w")
A=ord("a")
S=ord("s")
D=ord("d")

BASE_SPEED=66

FORWARD=1  #This way FORWARD*BASE_SPEED makes the motors go forward
BACKWARD=-1#and BACKWARD*BASE_SPEED makes the motors go backward
STOPPED=0 

def get_key(screen):
	key = screen.getch()
	while key == '\x00' or key == '\xe0': # non ASCII key
		key = screen.getch() # fetch second character
	return key

def record_data(datafile,compasses,compass_ids,expected_values,x,y,room):
	readings = []
	for compass in compasses:	
		readings.append(sense(compass,5))
	timestamp = time.time()
	rdlib.record_data(datafile,compass_ids,room,timestamp,x,y,expected_values,readings)
#--MAIN--

bot = find_bot()

compasses = []
compass_ids = []
expected_values = []
for port in SENSOR_PORTS:
	try:
		compass=hicompass.CompassSensor(bot,port)
		print "Testing",PORT_KEY[port]
		if compass.get_type() == "Compass ":#note that there's
							#an extra space
			print "Compass Detected in", PORT_KEY[port]
			compass_ids.append(raw_input("Compass_ID: "))
			expected_values.append(input("Expected_Value: "))
			compasses.append(compass)
	except hicompass.DirProtError:
		print "Could not communicate"	

x = input("x origin: ")
y = input("y origin: ")
room = raw_input("room ID {D124, D128, D129} : ")
while not ((room == "D124") or (room == "D128") or (room == "D129")):
	print "invalid room"
	room = raw_input("room ID {D124, D128, D129} : ")
	
filepath = raw_input ("Data File: ")
datafile = open(filepath,'w')

calibrate = raw_input("Calibrate?(default yes)").lower()
if ( not calibrate  == "n" ) and ( not calibrate == "no" ) :
	print "calibrating..."
	
	run_calibrator(compasses)

	print "calibration complete"
else:
	print "skipped calibration"

screen = c.initscr() #begin the curses environment
try:
	c.noecho()#stop characters auto-echoing to screen
	finished = False
	redraw = True
# Now mainloop runs until "finished"
	while not finished:
		if redraw:
			screen.clear()
			screen.addstr("current coordinates: (" + str(x) + "," + str(y) + ")\n")
			screen.addstr("Controls:\n")
			screen.addstr("Move coordinates:   w    Record Data: Spacebar  Quit: q\n")
			screen.addstr("                  a s d\n")
			redraw = False
		key = get_key(screen)
		if key == SPACEBAR:
			screen.addstr("Recording data...")
			record_data(datafile,compasses,compass_ids,expected_values,x,y,room)
			screen.addstr("Data Recorded")
			sound(bot)
		elif key == Q:
			finished = True
		elif key == W:
			y+=1
			redraw = True
		elif key == A:
			x-=1
			redraw = True
		elif key == S:
			y-=1
			redraw = True
		elif key == D:
			x+=1
			redraw = True
finally:
	c.endwin() #This is critical!
	#If the program exits before this function is called
	#Terrible things will happen

	datafile.close()
	stop_bot(bot)
