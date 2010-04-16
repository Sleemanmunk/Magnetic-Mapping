#!/usr/bin/python

import sys
import os
import re

args = sys.argv
files = args[1:]
line_regex = re.compile(r'(?P<id_1>[^,]*),(?P<id_2>[^,]*),(?P<id_3>[^,]*),(?P<id_4>[^,]*),(?P<room>[^,]*),(?P<time>[^,]*),(?P<x>[^,]*),(?P<y>[^,]*),(?P<exp_1>[^,]*),(?P<exp_2>[^,]*),(?P<exp_3>[^,]*),(?P<exp_4>[^,]*),(?P<act_1>[^,]*),(?P<act_2>[^,]*),(?P<act_3>[^,]*),(?P<act_4>[^,]*)')

for filename in files:
	read_file = open(filename, 'r')
	write_file = open(filename + '.tmp', 'w')
	for line in read_file: 
		line = line_regex.sub(r'\g<id_1>,\g<room>,\g<time>,\g<x>,\g<y>,\g<exp_1>,\g<act_1>\n\g<id_2>,\g<room>,\g<time>,\g<x>,\g<y>,\g<exp_2>,\g<act_2>\n\g<id_3>,\g<room>,\g<time>,\g<x>,\g<y>,\g<exp_3>,\g<act_3>\n\g<id_4>,\g<room>,\g<time>,\g<x>,\g<y>,\g<exp_4>,\g<act_4>', line)
		write_file.write(line)
	read_file.close()
	write_file.close()
	os.rename(filename + '.tmp', filename)
