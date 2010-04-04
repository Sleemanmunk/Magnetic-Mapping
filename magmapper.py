from nxt_common import *
import record_data_lib
import nxt.hicompass as hicompass

import curses as c
#Some notes about using curses:
#Curses creates a new window within the terminal.
#Everything you're working on will be temporarily erased
#and you will return to it when the program is finished.
#When in curses mode, instead of print, use screen.addstr


#Expected Values
X_NORTH = 0
X_EAST = 90
X_SOUTH = 180
X_WEST = 270

#Ports on NXT for sensors and a key for easy conversion to user-friendly output
SENSOR_PORTS = [PORT_1,PORT_2,PORT_3,PORT_4]
PORT_KEY = {PORT_1:"Port 1",PORT_2:"Port 2",PORT_3:"Port 3",PORT_4:"Port 4"}

#Constants for relevant keycodes
#Further keycodes may be determined with python's ord( char ) function
UP_ARROW=65
DOWN_ARROW=66
SPACEBAR=32
Q=113

BASE_SPEED=66

FORWARD=1  #This way FORWARD*BASE_SPEED makes the motors go forward
BACKWARD=-1#and BACKWARD*BASE_SPEED makes the motors go backward
STOPPED=0 

def get_key(screen):
	key = screen.getch()
	while key == '\x00' or key == '\xe0': # non ASCII key
		key = screen.getch() # fetch second character
	return key

def move(bot,direction):
	Motor(bot, PORT_ALL).run(direction*BASE_SPEED) #FORWARD=1 BACKWARD=-1
	return direction 

def stop(bot):
	Motor(bot, PORT_ALL).stop()
	return STOPPED

def record_data(bot):
	pass
#--MAIN--

bot = find_bot()

compasses = []
compass_ids = []

for port in SENSOR_PORTS:
	try:
		compass=hicompass.CompassSensor(bot,port)
		print "Testing",PORT_KEY[port]
		if compass.get_type() == "Compass ":#note that there's
							#an extra space
			print "Compass Detected in", PORT_KEY[port]
			compass_ids.append(raw_input("Compass_ID: "))
			compasses.append(compass)
	except hicompass.DirProtError:
		print "Could not communicate"	

screen = c.initscr() #begin the curses environment
c.noecho()#stop characters auto-echoing to screen
screen.addstr("Hit q to end...\n")
finished = False
movement = STOPPED

# Now mainloop runs until "finished"
while not finished:
	key = get_key(screen)
	if key == UP_ARROW:
		if movement != FORWARD:
			movement = move(bot,FORWARD)
		else:
			movement = stop(bot)
	elif key == DOWN_ARROW:
		if movement != BACKWARD:
			movement = move(bot,BACKWARD)
		else:
			movement = stop(bot)
	elif key == SPACEBAR:
		movement = stop(bot)
		record_data(bot)
	elif key == Q:
		finished = True

c.endwin() #This is critical!
#If the program exits before this function is called
#Terrible things will happen

stop_bot(bot)
