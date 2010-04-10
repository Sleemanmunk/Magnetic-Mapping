<style type="text/css">
	table.legend { border: 1px solid #666 }
	table.legend td { border: 1px solid #CCC; padding: 3px }

	table.map { border: 2px solid #CCC; background-color: #EEE }
	table.map td { width: 20px; height: 20px; margin:0; padding: 0  }
	table.map td a { display:block; width: 20px; padding: 0; margin: 0; text-decoration: none }
	.good { background-color: #4B8A08; color: #DDD }
	.bad { background-color: #8A0808; color: #DDD }
	.suspect{ background-color: #D7DF01; }
	.unknown{ background-color: #FFF }
	.inaccessible { background-color: #DDD; }
	/* this is for marking the origin */
	.ul { border-right: 1px solid black; border-top: 1px solid black }
	.ur {border-right: 1px solid black; border-top: 1px solid black }
	.ll {border-left: 1px solid black; border-bottom: 1px solid black }
	.lr {border-left: 1px solid black; border-bottom: 1px solid black }
</style>
<h1>Lab 6 Room Mapping</h1>
<table class="legend">
	<caption>Legend</caption>
	<tr>
		<td class="good">good</td><td class="bad">bad</td><td class="suspect">suspect</td><td class="unknown">unknown</td><td class="inaccessible">inaccessible</td><td><a href="#" title="This is some text that I put here for you to see\nThere was a return there<br>There was a br there">&nbsp;</a>
	</tr>
</table>

<?php
///////////////////////////////////
// Values you might want to change
///////////////////////////////////

$data_dir = '/tmp/robotics/dat';
$debug = 0; // debugging messages {0=none, 1=sparse, 2=lots}
$room_list = Array( 
	'D124' => Array( 'xmin' => -12, 'xmax' => 12, 'ymin' => -14, 'ymax' => 14 ),
	'D128' => Array( 'xmin' => -11 , 'xmax' => 11 , 'ymin' => -14, 'ymax' => 14 ),
	'D129' => Array( 'xmin' => -6, 'xmax' => 7, 'ymin' => -8, 'ymax' => 7 ));
$acceptable_reading_range = 180; // -5 to +5 degrees
$bad_readings_means_bad_tile = 1;

///////////////////
// Setup Variables
///////////////////

// Tile states
$good_tile = 1;
$bad_tile = 2;
$suspect_tile = 3;
$inaccessible_tile = -1;

$correct_value_count = 16;

// Initialize Room Arrays
$room_names = array_keys( $room_list );
foreach( $room_names as $room ) {
	${$room} = Array( 'name' => $room );
}

/////////////
// Functions
/////////////

function throw_error( $msg ) {
	exit( "Error: $msg" );
}

function get_tile_stats( $expected_actual_array ) {
	global $debug, $acceptable_reading_range;
	$good_readings = 0;
	$bad_readings = 0;
	$total_error = 0;
	if( $expected_actual_array[0][0] == -1 ) {
		return( Array( 
			'good_count' => -1, 
			'bad_count' => -1, 
			'cumulative_error' => -1 ));
	}

	foreach( $expected_actual_array as $pair ) {
		list( $expected, $actual ) = $pair;

		// determine distance of each angle to due north
		$e_to_zero = min( $expected, 360 - $expected ); // (CW, CCW)
		$a_to_zero = min( $actual, 360 - $actual ); // (CW, CCW)

		// determine the difference between the two angles
		$error = min( abs( $expected - $actual ), ( $e_to_zero + $a_to_zero ));

		if( $debug > 1 ) {
			print( "Expected: $expected, Actual:$actual, Error: $error<br>\n" );
		}
		$total_error += $error;

		if( $error > $acceptable_reading_range / 2 ) {
			$bad_readings += 1;
			if( $debug > 1 ) {
				print( "bad reading ($bad_readings total for this tile)<br>\n");
			}
		} else { // good reading
			if( $debug > 1 ) {
				print( "good reading ($good_readings total for this tile)<br>\n");
			}
			$good_readings += 1;
		}
	}
	if( $debug > 0 ) {
		print( "good: $good_readings, bad: $bad_readings, cumulative_error: $total_error<br>\n" );
	}
	return( Array( 
		'good_count' => $good_readings, 
		'bad_count' => $bad_readings, 
		'cumulative_error' => $total_error ));
}

function determine_tile_status( $stats_array ) {
	global $good_tile, $bad_tile, $suspect_tile, $inaccessible_tile, $bad_readings_means_bad_tile;
	if( $stats_array['good_count'] == -1 ) {
		return $inaccessible_tile;
	} elseif ( $stats_array['bad_count'] >= $bad_readings_means_bad_tile ) {
		return $bad_tile;
	} else {
		return $good_tile;
		// todo add more infiromation to display here
	}
}

function print_map( $room ) {
	global $room_list, $good_tile, $bad_tile, $suspect_tile, $inaccessible_tile;
	$name = $room['name'];

	$xmin = abs( $room_list[$name]['xmin'] );
	$xmax = $room_list[$name]['xmax']; 
	$ymin = abs( $room_list[$name]['ymin'] ); 
	$ymax = $room_list[$name]['ymax']; 

	$xrange = range( 0, $xmax + $xmin );
	$yrange = range( 0, $ymax + $ymin );
	echo "<table class=\"map\">\n";
	foreach( $yrange as $y ) {
		if( $y != $ymin ) {
			echo "<tr>\n";
			foreach( $xrange as $x ) {
				if( $x != $xmin ) {
					if( isset( $room[$x][$y] )) {
						/* Mark the origin 
						if( $x == $xmin - 1 and $y == $ymax - 1 ) {
							$border = ' lr';
						} elseif ( $x == $xmin + 1 and $y == $ymax -1 ) {
							$border = ' ll';
						} elseif ( $x == $xmin - 1 and $y == $ymax + 1 ) {
							$border = ' ur';
						} elseif ( $x == $xmin + 1 and $y == $ymax + 1) {
							$border = ' ul';
						} else {
							$border = '';
						}
						*/
						$status = $room[$x][$y]['status'];
						if( $status == $good_tile ) {
							echo "<td class=\"good$border\">&nbsp;</td>\n";
						} elseif( $status == $bad_tile ) { 
							echo "<td class=\"bad$border\">&nbsp;</td>\n";
						} elseif( $status == $suspect_tile ) { 
							echo "<td class=\"suspect$border\">&nbsp;</td>\n";
						} elseif( $status == $inaccessible_tile ) { 
							echo "<td class=\"inaccessible$border\">&nbsp;</td>\n";
						} else { 
							throw_error( "$status is not a valid tile state" );
						}
					} else { // (x,y) is not set
						echo "<td class=\"unknown\">&nbsp;</td>\n";
					} 
				}
			}
			echo "</tr>\n";
		}
	}
	echo '</table>';
}

/////////////////////////
// Read and Process Data
/////////////////////////
if( is_dir( $data_dir )) {
    if( $data_dh = opendir( $data_dir )) {
        while(( $input_file = readdir( $data_dh )) !== false ) {
						$in_fh = fopen( "$data_dir/$input_file", 'r' ) or die( "Can't open input file" );
						$raw_data .= fread( $in_fh, filesize( "$data_dir/$input_file" ));
						fclose( $in_fh );
        }
        closedir($data_dh);
    }
}

$lines = explode( "\n", $raw_data );

// Expected values format
// [0] => sensor 1 id
// [1] => sensor 2 id
// [2] => sensor 3 id
// [3] => sensor 4 id
// [4] => room id
// [5] => timestamp
// [6] => x position
// [7] => y position
// [8] => sensor 1 expected
// [9] => sensor 2 expected
// [10] => sensor 3 expected
// [11] => sensor 4 expected
// [12] => sensor 1 actual
// [13] => sensor 2 actual
// [14] => sensor 3 actual
// [15] => sensor 4 actual

foreach( $lines as $line ) {
	$values = explode( ",", $line );
	if( count( $values ) != $correct_value_count ) {
		if( $debug > 0 ) {
			print "Ignoring line with incorrect number of values in line (" . count( $values ) . " instead of $correct_value_count)<br>\n";
			if( debug > 1 ) {
				print "skipped line:\n";
				print_r( $values );
				print( "<br>\n" );
			}
		} 
	} else { // line has correct number of values
		$room = $values[4];
		if( !in_array( $room, $room_names )) {
			if( $debug > 0 ) {
				print( "ignoring line bacause $room is not a valid room<br>\n" );
			}
		} else { // valid room
			$x = intval( $values[6] );
			$y = intval( $values[7] );
			if(( $x < $room_list[$room]['xmin'] ) or ( $x > $room_list[$room]['xmax'] )) {
				if( $debug > 0 ) {
					print "Ignoring line with x value ($x) outside of range (" . $room_list[$room]['xmin'] . ' through ' . $room_list[$room]['xmax'] . ")<br>\n";
					if( $debug > 1 ) {
						print "skipped line:<br>\n";
						print_r( $values );
						print( "<br>\n" );
					}
				} 
			} elseif(( $y < $room_list[$room]['ymin'] ) or ( $y > $room_list[$room]['ymax'] )) {
				if( $debug > 0 ) {
					print "Ignoring line with y value ($y) outside of range (" . $room_list[$room]['ymin'] . ' through ' . $room_list[$room]['ymax'] . ")<br>\n";
					if( $debug > 1 ) {
						print "skipped line:\n";
						print_r( $values );
						print( "<br>\n" );
					}
				} 
			} else { // valid x and y coordinates

				$tile_stats = get_tile_stats( Array( 
					Array( $values[8], $values[12] ), // expected, actual sensor 1
					Array( $values[9], $values[13] ), // expected, actual sensor 2
					Array( $values[10], $values[14] ), // expected, actual sensor 3
					Array( $values[11], $values[15] ) // expected, actual sensor 4
					));

				// todo check to see if it's already been recorded
				$tile_stats['status'] = determine_tile_status( $tile_stats );
				$col_pos = $x + abs( $room_list[$room]['xmin'] );
				$row_pos = $room_list[$room]['ymax'] - $y;
				${$room}[$col_pos][$row_pos] = $tile_stats; 
			}
		}
	}
}

print( '<p> To be considered a good tile, the sensor readings must be within +-( ' . strval( $acceptable_reading_range / 2 ) . ' degrees ) and ' . strval( 4 - $bad_readings_means_bad_tile + 1) . "/4 sensors must read good.</p>\n" );

foreach( $room_names as $room ) {
	print "<h2>Room: $room</h2>\n";
	print_map( ${$room} );
}


?>
