import nxt_common as nxtc
import record_data_lib
import hicompass

import curses as c
#Some notes about using curses:
#Curses creates a new window within the terminal.
#Everything you're working on will be temporarily erased
#and you will return to it when the program is finished.
#When in curses mode, instead of print, use screen.addstr

#Constants for relevant keycodes
#Further keycodes may be determined with python's ord( char ) function
UP_ARROW=65
DOWN_ARROW=66
SPACEBAR=32
Q=113

BASE_SPEED=127

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
		else
			movement = stop(bot)
	elif key == DOWN_ARROW:
		if movement != BACKWARD:
			movement = move(bot,BACKWARD)
		else
			movement = stop(bot)
	elif key == SPACEBAR:
		movement = stop(bot)
		record_data()
	elif key == Q:
		finished = True

c.endwin() #This is critical!
#If the program exits before this function is called
#Terrible things will happen
