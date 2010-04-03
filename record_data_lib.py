def record_data( data_file, sensor_ids, room, timestamp, x, y, expected_values, readings ):

	# note: this code assumes that strings do not contain quotation marks, newlines or commas

  if ( len( sensor_ids ) != len( expected_values )) or ( len( expected_values ) != len( readings )):
    print 'Error: The number of sensors (' + str( len( sensor_ids )) + '), expected values (' + str( len( expected_values )) + '), and readings (' + str( len( readings )) + ') must be the same'
    exit()

  csv_line = ''
  for sensor in sensor_ids:
    csv_line += str( sensor ) + ','
  csv_line += str( room ) + ','
  csv_line += str( timestamp ) + ','
  csv_line += str( x ) + ','
  csv_line += str( y ) + ','
  for value in expected_values:
    csv_line += str( value ) + ','
  for value in readings:
    csv_line += str( value ) + ','

  # change last comma to a newline
  csv_line = csv_line[0:len(csv_line)-1] + "\n"

  data_file.write( csv_line )
