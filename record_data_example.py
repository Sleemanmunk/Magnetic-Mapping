import time
import random
from record_data_lib import *

# Please make the filename something unique and descriptive
# so as not to have conflicts with other groups / bots.
# 
# It is entirely possible that you may have different data
# files for each room or even each data collecting session.
# The naming scheme should be determined by the Data Collection 
# group.

# open file for writing (append to already exisiting content)
data_file = open('bot-9_D128.dat', 'a')

# sensor IDs will probably be static for each bot
sensor_ids = ['sensor 1', 'sensor 2', 'sensor 3', 'sensor 4' ]

# The expected values will be bot dependent since the sensors 
# may not be oriented exactly 90 degrees from each
# other or some sensors may calibrte a stable number 
# of degrees from their actual orientation.
#
# This should be determined by the Robot group and the Testing/
# Automation/Refactoring group.
#
# The expected values may change based on the data collection
# algorithm (i.e. the bot may not always be facing North). This
# will be dicated by the Software group.
expected_values = [ 0, 90, 180, 270 ]

# This will be one of {D124, D128, D129}
room = 'D129'

# the software group will define the code structure that takes
# the compass sensor measurements. This is only an example for 
# testing purposes.

# arbitrary starting position
x_start = 5
y_start = 5

for x in range( x_start, x_start + 5 ):
  for y in range( y_start, y_start + 5 ):
    error = random.randint( 0, 5 ) # simulated error, yay!
    readings = [ 0+error, 90+error, 180+error, 270+error ]
    record_data( data_file, sensor_ids, room, time.time(), x, y, expected_values, readings )

data_file.close()

