import mynxtlib
import curses as c

keyBindings = {65:"UpArrow",66:"DownArrow"}

def KeyEvent(key):
    if key == '\x00' or key == '\xe0': # non ASCII key
       key = screen.getch() # fetch second character
    if key != 65 and key != 66:
    	screen.addstr(str(key)+' ')
    else:
	screen.addstr(str(keyBindings[key])+' ')

# clear the screen of clutter, stop characters auto 
# echoing to screen and then tell user what to do to quit

screen = c.initscr()
c.noecho()
screen.addstr("Hit space to end...\n")
finished = False

# Now mainloop runs until "finished"
while not finished:
     ky = screen.getch()
     if ky != -1:
       # send events to event handling functions
       	if ky == ord(" "): # check for quit event
       		finished = True
	else: 
	 	KeyEvent(ky)
c.endwin()
