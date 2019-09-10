
def call_quest_functions():
	quest_dict = {}
	quest_dict['empty_position'] = 10
	quest_dict = create_grid(quest_dict)
	quest_dict = create_tiles(quest_dict)


	quest_dict['path'] = check_path(quest_dict, "starting path")
	starting_position = quest_dict['initial_starting_position']
	ending_position = quest_dict['initial_ending_position']

	winning_path = find_winning_path(quest_dict, starting_position, quest_dict['initial_starting_direction'], ending_position, quest_dict['initial_ending_direction'] )
	quest_dict['initial_path'] = winning_path
	direction_path = find_winning_path_directions(quest_dict, winning_path, quest_dict['initial_starting_direction'], quest_dict['initial_ending_direction'])
	quest_dict['direction_path'] = direction_path

	second_winning_path = find_winning_path(quest_dict, quest_dict['second_starting_position'], quest_dict['second_starting_direction'], \
		quest_dict['second_ending_position'], quest_dict['second_ending_direction'])
	quest_dict['second_winning_path'] = second_winning_path
	second_direction_path = find_winning_path_directions(quest_dict, second_winning_path, quest_dict['second_starting_direction'], \
		quest_dict['second_ending_direction'])
	quest_dict['second_direction_path'] = second_direction_path

	quest_dict = move_unecessary_tiles(quest_dict, winning_path, direction_path)

	placed_tiles = []
	placed_tiles = find_next_piece(quest_dict, winning_path, direction_path, placed_tiles, "Forward")
	placed_tiles = find_next_piece(quest_dict, winning_path, direction_path, placed_tiles, "Backwards")
	placed_tiles = find_next_piece(quest_dict, winning_path, direction_path, placed_tiles, "Forward")
	placed_tiles = find_next_piece(quest_dict, winning_path, direction_path, placed_tiles, "Backwards")

	#Need to slot specific portions to clear enough room to clear the puzzle
	placed_tiles = find_next_piece(quest_dict, winning_path, direction_path, placed_tiles, 6)
	placed_tiles = find_next_piece(quest_dict, winning_path, direction_path, placed_tiles, 7)
	placed_tiles = find_next_piece(quest_dict, winning_path, direction_path, placed_tiles, 10)
	print ("PLACED TILES")
	print (placed_tiles)

	quest_dict['path'] = check_path(quest_dict, "starting path")
	path_complete  = False
	if quest_dict['path'][-1] == quest_dict['initial_ending_position'] and len(quest_dict['path']) == len(winning_path):
		for tile in quest_dict['tile_list']:
			if tile.return_position() == quest_dict['initial_ending_position']:
				for index, status in enumerate(tile.return_direction_list()):
					if index == 0 and status and quest_dict['initial_ending_direction'] == "UP":
						path_complete = True
					elif index == 1 and status and quest_dict['initial_ending_direction'] == "DOWN":
						path_complete = True
					elif index == 2 and status and quest_dict['initial_ending_direction'] == "LEFT":
						path_complete = True
					elif index == 3 and status and quest_dict['initial_ending_direction'] == "RIGHT":
						path_complete = True

	quest_dict['initial_path_complete'] = path_complete

	#Declare next starting position and ending position
	if path_complete:
		starting_position = quest_dict['second_starting_position']
		ending_position = quest_dict['second_ending_position']

		second_path = check_path(quest_dict, "second path")

		placed_tiles = []
		placed_tiles = find_next_piece(quest_dict, second_winning_path, second_direction_path, placed_tiles, "Forward")
		placed_tiles = find_next_piece(quest_dict, second_winning_path, second_direction_path, placed_tiles, "Forward")
		placed_tiles = find_next_piece(quest_dict, second_winning_path, second_direction_path, placed_tiles, "Backwards")
		placed_tiles = find_next_piece(quest_dict, second_winning_path, second_direction_path, placed_tiles, "Backwards")

		placed_tiles = find_next_piece(quest_dict, second_winning_path, second_direction_path, placed_tiles, 11)
		placed_tiles = find_next_piece(quest_dict, second_winning_path, second_direction_path, placed_tiles, 10)
		placed_tiles = find_next_piece(quest_dict, second_winning_path, second_direction_path, placed_tiles, 7)
		placed_tiles = find_next_piece(quest_dict, second_winning_path, second_direction_path, placed_tiles, 6)

		print ("Second placed tiles")
		print (placed_tiles)

	second_path = check_path(quest_dict, "second path")
	quest_dict['second_path'] = second_path
	second_path_complete  = False
	if second_path[-1] == quest_dict['second_ending_position'] and len(second_path) == len(second_winning_path):
		for tile in quest_dict['tile_list']:
			if tile.return_position() == quest_dict['second_ending_position']:
				for index, status in enumerate(tile.return_direction_list()):
					if index == 0 and status and quest_dict['second_ending_direction'] == "UP":
						second_path_complete = True
					elif index == 1 and status and quest_dict['second_ending_direction'] == "DOWN":
						second_path_complete = True
					elif index == 2 and status and quest_dict['second_ending_direction'] == "LEFT":
						second_path_complete = True
					elif index == 3 and status and quest_dict['second_ending_direction'] == "RIGHT":
						second_path_complete = True

	quest_dict['second_path_complete'] = second_path_complete
	return quest_dict

def create_grid(quest_dict):
	width = 4
	height = 4

	position_list = []
	for i in range(1, (width * height + 1)):
		position_list.append(i)

	quest_dict['position_list'] = position_list
	quest_dict['width'] = width
	quest_dict['height'] = height
	quest_dict['initial_starting_position'] = 4
	quest_dict['initial_starting_direction'] = 'UP'
	quest_dict['initial_ending_position'] = 13
	quest_dict['initial_ending_direction'] = 'LEFT'
	quest_dict['second_starting_position'] = 13
	quest_dict['second_starting_direction'] = 'LEFT'
	quest_dict['second_ending_position'] = 16
	quest_dict['second_ending_direction'] = 'RIGHT'

	#Incase the the finder tile chooses a tile I want to be able to choose a different tile
	quest_dict['tried_new_tile'] = False
	quest_dict['move_history'] = []
	quest_dict['obstacle_list'] = []

	return quest_dict

def create_tiles(quest_dict):

	#LD 
	tile_1 = tile(False,True,True,False,1)
	tile_2 = tile(False,True,True,False,2)
	tile_3 = tile(False,True,True,False,5)

	#RD
	tile_4 = tile(False,True,False,True,3)
	tile_5 = tile(False,True,False,True,6)
	tile_6 = tile(False,True,False,True,15)

	#RU
	tile_7 = tile(True,False,False,True,4)
	tile_8 = tile(True,False,False,True,7)
	tile_9 = tile(True,False,False,True,9)
	tile_10 = tile(True,False,False,True,16)

	#LU
	tile_11 = tile(True,False,True,False,8)
	tile_12 = tile(True,False,True,False,11)
	tile_13 = tile(True,False,True,False,12)
	tile_14 = tile(True,False,True,False,13)

	#Blank Tile
	tile_15 = tile(False,False,False,False,14)

	tile_list = [tile_1,tile_2,tile_3,tile_4,tile_5,tile_6,tile_7,tile_8,tile_9,tile_10,tile_11,tile_12,tile_13,tile_14,tile_15]

	quest_dict['tile_list'] = tile_list

	return quest_dict

def find_winning_path(quest_dict, starting_position, starting_direction, ending_position, ending_direction):
	path_list = [[starting_position]]

	counter = 0
	#Not the limit of the path length might change depending on the problem
	path_limit_length = 8
	while counter < path_limit_length:
		new_paths = []
		for path in path_list:
			move_status = check_available_moves(quest_dict, path[-1])
			new_position_list = []
			for index, status in enumerate(move_status):
				if index == 0 and status:
					next_position = path[-1] - quest_dict['width']
					new_position_list.append(next_position)
				elif index == 1 and status:
					next_position = path[-1] + quest_dict['width']
					new_position_list.append(next_position)
				elif index == 2 and status:
					next_position = path[-1] - 1
					new_position_list.append(next_position)
				elif index == 3 and status:
					next_position = path[-1] + 1
					new_position_list.append(next_position)
				else:
					pass

			for position in new_position_list:
				if position not in path:
					path_variable = []
					for nested_position in path:
						path_variable.append(nested_position)

					path_variable.append(position)
					new_paths.append(path_variable)


		path_list = new_paths
		counter += 1


	winning_paths = analyze_paths(quest_dict, path_list, ending_position)
	winning_paths = find_possible_winning_paths(quest_dict, winning_paths, starting_position, starting_direction, ending_position, ending_direction)
	
	#Returning the first element in winning paths as it should be good enough
	return winning_paths[0]

def find_tile_path(quest_dict, starting_position, ending_position, placed_tiles, target_tile):
	path_list = [[starting_position]]
	counter = 0
	#Not the limit of the path length might change depending on the problem
	path_limit_length = 8
	while counter < path_limit_length:
		new_paths = []
		for path in path_list:
			move_status = check_available_moves(quest_dict, path[-1])
			new_position_list = []
			for index, status in enumerate(move_status):
				if index == 0 and status:
					next_position = path[-1] - quest_dict['width']
					new_position_list.append(next_position)
				elif index == 1 and status:
					next_position = path[-1] + quest_dict['width']
					new_position_list.append(next_position)
				elif index == 2 and status:
					next_position = path[-1] - 1
					new_position_list.append(next_position)
				elif index == 3 and status:
					next_position = path[-1] + 1
					new_position_list.append(next_position)
				else:
					pass

			for position in new_position_list:
				if position not in path:
					path_variable = []
					for nested_position in path:
						path_variable.append(nested_position)

					path_variable.append(position)
					new_paths.append(path_variable)


		path_list = new_paths
		counter += 1


	minimum_path = analyze_tile_path(quest_dict, path_list, ending_position, placed_tiles, target_tile)
	return minimum_path

def analyze_paths(quest_dict, path_list, ending_position):
	winning_paths = []
	for path in path_list:
		if ending_position in path:
			winning_paths.append(path)

	new_winning_paths = remove_extra_from_winning(quest_dict, winning_paths, ending_position)

	return new_winning_paths

def remove_extra_from_winning(quest_dict, winning_paths, ending_position):
	new_winning_paths = []
	for path in winning_paths:
		list_variable = []
		for item in path:
			if item == ending_position:
				list_variable.append(item)
				new_winning_paths.append(list_variable)
				break
			list_variable.append(item)

	return new_winning_paths

#def find_possible_winning_paths(quest_dict, winning_paths, starting_direction, starting_position, ending_position, ending_direction):
def find_possible_winning_paths(quest_dict, winning_paths, starting_position, starting_direction, ending_position, ending_direction):
	horizontal_counter = 0
	vertical_counter = 0
	new_winning_paths = []

	for tile in quest_dict['tile_list']:
		if tile.return_direction_list() == [True, True, False, False]:
			vertical_counter = vertical_counter + 1
		elif tile.return_direction_list() == [False, False, True, True]:
			horizontal_counter = horizontal_counter + 1

	for path in winning_paths:
		local_horizontal_counter = 0
		local_vertical_counter = 0 

		counter = 1
		while counter < len(path) - 1:
			if path[counter - 1] == path[counter + 1] - 2 or path[counter - 1] - 2 == path[counter + 1]:
				local_vertical_counter += 1

			if path[counter - 1] == (path[counter + 1] - 2 * quest_dict['width']) or (path[counter - 1] - 2 * quest_dict['width']) == path[counter + 1]:
				local_horizontal_counter += 1

			counter += 1

		if path[0] == path[1] - quest_dict['width'] and starting_direction == "UP":
			local_vertical_counter += 1
		elif path[0] == path[1] + quest_dict['width'] and starting_direction == "DOWN":
			local_vertical_counter += 1

		if path[0] == path[1] - 1 and starting_direction == "LEFT":
			local_horizontal_counter += 1
		elif path[0] == path[1] + 1 and starting_direction == "RIGHT":
			local_horizontal_counter += 1


		if path[-1] == path[-2] - quest_dict['width'] and ending_direction == "DOWN":
			local_vertical_counter += 1
		elif path[-1] == path[-2] + quest_dict['width'] and ending_direction == "UP":
			local_vertical_counter += 1

		if path[-1] == path[-2] - 1 and ending_direction == "LEFT":
			local_horizontal_counter += 1
		elif path[-1] == path[-2] + 1 and ending_direction == "RIGHT":
			local_horizontal_counter += 1

		append_status = True
		if local_horizontal_counter > horizontal_counter:
			append_status = False
		elif local_vertical_counter > vertical_counter:
			append_status = False

		if append_status:
			new_winning_paths.append(path)

	return new_winning_paths

def check_available_moves(quest_dict, position):
	#No obstacles are checked currently
	#UP DOWN LEFT RIGHT
	move_status = []
	if position - quest_dict['width'] > 0:
		move_status.append(True)
	else:
		move_status.append(False)

	if position + quest_dict['width'] <= quest_dict['width'] * quest_dict['height']:
		move_status.append(True)
	else:
		move_status.append(False)

	if (position - 1) % quest_dict['width'] != 0:
		move_status.append(True)
	else:
		move_status.append(False)

	if position % quest_dict['width'] != 0:
		move_status.append(True)
	else:
		move_status.append(False)

	return move_status

def check_path(quest_dict, path):
	if path == "starting path":
		starting_position = quest_dict['initial_starting_position'] 
		starting_direction = quest_dict['initial_starting_direction']

	elif path == "second path":
		starting_position = quest_dict['second_starting_position']
		starting_direction = quest_dict['second_starting_direction']

	path = []
	tile_list = quest_dict['tile_list']
	for tile in tile_list:
		if tile.return_position() == starting_position:
			current_tile = tile
			#If the tile at the starting path doens't connect with the starting position we return []
			already_connected_direction = 100 
			if current_tile.return_up_direction() == True and starting_direction == "UP":
				already_connected_direction = 0
				path.append(current_tile.return_position())
			elif current_tile.return_left_direction() == True and starting_direction == "LEFT":
				already_connected_direction = 2
				path.append(current_tile.return_position())
			elif current_tile.return_right_direction() == True and starting_direction == "RIGHT":
				already_connected_direction = 3
				path.append(current_tile.return_position())
			elif current_tile.return_down_direction() == True and starting_direction == "DOWN":
				already_connected_direction = 1
				path.append(current_tile.return_position())

			#Find out where the other direction goes
			if already_connected_direction < 5:
				direction_list = current_tile.return_direction_list()
				for index, status in enumerate(direction_list):
					if status == True and index != already_connected_direction:
						if index == 0:
							next_direction = "Up"
						elif index == 1:
							next_direction = "Down"
						elif index == 2:
							next_direction = "Left"
						else:
							next_direction = "Right"
			else:
				return path

			break

	loop_status = True 
	counter = 0
	while loop_status:
		last_index = path[-1]
		loop_status = False
		if next_direction == "Up":
			#Looking for a down connector
			for tile in tile_list:
				if tile.return_position() == last_index - quest_dict['width']:
					direction_list = tile.return_direction_list()
					if direction_list[1]:
						path.append(tile.return_position())
						loop_status = True
						#find next direction
						for index, status in enumerate(direction_list):
							if status == True and index != 1:
								if index == 0:
									next_direction = "Up"
								elif index == 1:
									next_direction = "Down"
								elif index == 2:
									next_direction = "Left"
								else:
									next_direction = "Right"

		elif next_direction == "Down":
			for tile in tile_list:
				if tile.return_position() == last_index + quest_dict['width']:
					direction_list = tile.return_direction_list()
					if direction_list[0]:
						path.append(tile.return_position())
						loop_status = True
						#find next direction
						for index, status in enumerate(direction_list):
							if status == True and index != 0:
								if index == 0:
									next_direction = "Up"
								elif index == 1:
									next_direction = "Down"
								elif index == 2:
									next_direction = "Left"
								else:
									next_direction = "Right"

		elif next_direction == "Left":
			for tile in tile_list:
				if tile.return_position() == last_index - 1 and (last_index - 1) % quest_dict['width'] != 0:
					direction_list = tile.return_direction_list()
					if direction_list[3]:
						path.append(tile.return_position())
						loop_status = True
						#find next direction
						for index, status in enumerate(direction_list):
							if status == True and index != 3:
								if index == 0:
									next_direction = "Up"
								elif index == 1:
									next_direction = "Down"
								elif index == 2:
									next_direction = "Left"
								else:
									next_direction = "Right"

		elif next_direction == "Right":
			for tile in tile_list:
				if tile.return_position() == last_index + 1 and last_index % quest_dict['width'] != 0:
					direction_list = tile.return_direction_list()
					if direction_list[2]:
						path.append(tile.return_position())
						loop_status = True
						#find next direction
						for index, status in enumerate(direction_list):
							if status == True and index != 2:
								if index == 0:
									next_direction = "Up"
								elif index == 1:
									next_direction = "Down"
								elif index == 2:
									next_direction = "Left"
								else:
									next_direction = "Right"

		counter += 1

	return path


def find_winning_path_directions(quest_dict, winning_path, starting_direction, ending_direction):
	tile_path = []
	#I Need to find the equivalent tiles corresponding to the path
	#Going to try and find the closest tile not already in the tile_path

	#Find initial starting tile
	tile_direction = [False, False, False, False]
	if starting_direction == "UP":
		tile_direction[0] = True
	elif starting_direction == "DOWN":
		tile_direction[1] = True
	elif starting_direction == "LEFT":
		tile_direction[2] = True
	else:
		tile_direction[3] = True

	if winning_path[0] == winning_path[1] - 1:
		tile_direction[3] = True
	elif winning_path[0] == winning_path[1] + 1:
		tile_direction[2] = True
	elif winning_path[0] == winning_path[1] - quest_dict['width']:
		tile_direction[1] = True
	elif winning_path[0] == winning_path[1] + quest_dict['width']:
		tile_direction[0] = True

	#Now I have the initial starting direction. let's find the next direction and then assign a tile to the tile list.
	next_direction = find_next_direction(starting_direction, tile_direction)
	tile_path.append(tile_direction)

	counter = 1 
	while counter < len(winning_path) - 1:
		tile_direction = [False, False, False, False]
		if next_direction == "UP":
			tile_direction[0] = True
		elif next_direction == "DOWN":
			tile_direction[1] = True
		elif next_direction == "LEFT":
			tile_direction[2] = True
		else:
			tile_direction[3] = True

		if winning_path[counter] == winning_path[counter + 1] - 1:
			tile_direction[3] = True
		elif winning_path[counter] == winning_path[counter + 1] + 1:
			tile_direction[2] = True
		elif winning_path[counter] == winning_path[counter + 1] - quest_dict['width']:
			tile_direction[1] = True
		elif winning_path[counter] == winning_path[counter + 1] + quest_dict['width']:
			tile_direction[0] = True

		tile_path.append(tile_direction)
		next_direction = find_next_direction(next_direction, tile_direction)

		counter += 1

	#Get the last tiles directions
	tile_direction = [False, False, False, False]
	if next_direction == "UP":
		tile_direction[0] = True
	elif next_direction == "DOWN":
		tile_direction[1] = True
	elif next_direction == "LEFT":
		tile_direction[2] = True
	else:
		tile_direction[3] = True

	if ending_direction == "UP":
		tile_direction[0] = True
	elif ending_direction == "DOWN":
		tile_direction[1] = True
	elif ending_direction == "LEFT":
		tile_direction[2] = True
	else:
		tile_direction[3] = True

	tile_path.append(tile_direction)

	return tile_path

def find_next_direction(starting_direction, tile_direction):
	if starting_direction == "UP":
		if tile_direction[1]:
			next_direction = "UP"
		elif tile_direction[2]:
			next_direction = "RIGHT"
		elif tile_direction[3]:
			next_direction = "LEFT"

	elif starting_direction == "DOWN":
		if tile_direction[0]:
			next_direction = "DOWN"
		elif tile_direction[2]:
			next_direction = "RIGHT"
		elif tile_direction[3]:
			next_direction = "LEFT"

	elif starting_direction == "LEFT":
		if tile_direction[0]:
			next_direction = "DOWN"
		elif tile_direction[1]:
			next_direction = "UP"
		elif tile_direction[3]:
			next_direction = "LEFT"

	elif starting_direction == "RIGHT":
		if tile_direction[0]:
			next_direction = "DOWN"
		elif tile_direction[1]:
			next_direction = "UP"
		elif tile_direction[2]:
			next_direction = "RIGHT"

	return next_direction

def find_next_piece(quest_dict, winning_path, direction_path, placed_tiles, bridge_piece):
	if bridge_piece == "Forward":
		counter = 0
		while counter < len(winning_path):
			if winning_path[counter] not in placed_tiles:
				target_position = winning_path[counter]
				target_index = counter
				break
			counter += 1
	elif bridge_piece == "Backwards":
		target_index = - 1
		counter = len(winning_path) - 1
		while counter >= 0:
			if winning_path[counter] not in placed_tiles:
				target_position = winning_path[counter]
				target_index = counter
				break
			counter = counter - 1
	else:
		target_position = bridge_piece
		counter = 0
		while counter < len(winning_path):
			if winning_path[counter] == bridge_piece and bridge_piece not in placed_tiles:
				target_index = counter

			counter += 1

		
	#Checking if the tile is currently in place
	for tile in quest_dict['tile_list']:
		if tile.return_position() == target_position:
			if tile.return_direction_list() == direction_path[target_index]:
				placed_tiles.append(tile.return_position())
				return placed_tiles

	#find tiles that match the direction list
	direction_list = direction_path[target_index]
	possible_tiles = []
	for tile in quest_dict['tile_list']:
		if tile.return_direction_list() == direction_list:
			if tile not in placed_tiles and tile.return_position() not in placed_tiles:
				possible_tiles.append(tile)

	#Choose the tile whose position is closest to the 
	target_tile = possible_tiles[0]

	target_horizontal_counter = 0
	moved_target_position = target_position
	while moved_target_position % quest_dict['width'] != 0:
		moved_target_position = moved_target_position + 1
		target_horizontal_counter += 1
		
	possible_horizontal_counter = 0
	moved_possible_position = possible_tiles[0].return_position()
	while moved_possible_position % quest_dict['width'] != 0:
		moved_possible_position = moved_possible_position + 1
		possible_horizontal_counter += 1

	vertical_counter = 0
	if moved_possible_position > moved_target_position:
		while moved_possible_position != moved_target_position:
			moved_possible_position = moved_possible_position - quest_dict['width']
			vertical_counter += 1
	elif moved_possible_position < moved_target_position:
		while moved_possible_position != moved_target_position:
			moved_possible_position = moved_possible_position + quest_dict['width']
			vertical_counter += 1

	minimum_distance = abs(target_horizontal_counter - possible_horizontal_counter) + vertical_counter

	for tile in possible_tiles:
		possible_horizontal_counter = 0
		moved_possible_position = target_tile.return_position()
		while moved_possible_position % quest_dict['width'] != 0:
			moved_possible_position = moved_possible_position + 1
			possible_horizontal_counter += 1

		vertical_counter = 0
		if moved_possible_position > moved_target_position:
			while moved_possible_position != moved_target_position:
				moved_possible_position = moved_possible_position - quest_dict['width']
				vertical_counter += 1
		elif moved_possible_position < moved_target_position:
			while moved_possible_position != moved_target_position:
				moved_possible_position = moved_possible_position + quest_dict['width']
				vertical_counter += 1

		test_minimum_distance = abs(target_horizontal_counter - possible_horizontal_counter) + vertical_counter

		if test_minimum_distance < minimum_distance:
			minimum_distance = test_minimum_distance
			target_tile = tile

	#Initiate a move cycle to get the target tile into the slot
	placed_tiles = move_cycle(quest_dict, winning_path, placed_tiles, target_tile, target_index)
	#Recursive call to the parent function with updated quest_dict and placed tiles thing
	return placed_tiles

def move_cycle(quest_dict, winning_path, placed_tiles, target_tile, target_index):
	#Find a path for the tile that won't interfere with tiles placed inside the placed tiles

	#Find the path that the target tile must take to get to the target_position
	length_of_placed_tiles = len(placed_tiles)
	target_position = winning_path[target_index]

	ending_position = winning_path[target_index]
	starting_position = target_tile.return_position()

	quest_dict = initiate_tile_move(quest_dict, starting_position, ending_position, target_tile, placed_tiles)

	if target_tile.return_position() == ending_position:
		placed_tiles.append(ending_position)
	else:
		#starting_position = target_tile.return_position()
		#quest_dict = initiate_tile_move(quest_dict, starting_position, ending_position, target_tile, placed_tiles)
		if quest_dict['break_recursion_status'] == False:
			placed_tiles = move_cycle(quest_dict, winning_path, placed_tiles, target_tile, target_index)
		else:
			#call choose new target tile
			if quest_dict['tried_new_tile'] == False:
				placed_tiles = choose_new_target_tile(quest_dict, winning_path, placed_tiles, target_tile, target_index)
			quest_dict['tried_new_tile'] = False
			print ("RECURSION IS BREAKING")
	
	return placed_tiles

def analyze_tile_move(quest_dict, starting_position, ending_position, target_tile, target_path):
	status = "Move Empty"

	if quest_dict['empty_position'] in target_path:
		if abs(target_tile.return_position() - quest_dict['empty_position']) == 1 or abs(target_tile.return_position() - quest_dict['empty_position']) == quest_dict['width']:
			status = "Move Into Empty"


	return status

def analyze_tile_path(quest_dict, path_list, ending_position, placed_tiles, target_tile):
	winning_paths = []
	snipped_winning_paths = []
	#For paths that don't interfere with placed tiles
	clear_winning_paths = []

	for path in path_list:
		if ending_position in path:
			winning_paths.append(path)

	#snip the paths to remove extra after the ending_position has been reached
	for path in winning_paths:
		counter = 0
		list_variable = []
		while counter < len(path):
			list_variable.append(path[counter])
			if path[counter] == ending_position:
				snipped_winning_paths.append(list_variable)
				break
			counter += 1

	for path in snipped_winning_paths:
		counter = 0
		append_status = True
		while counter < len(path):
			if path[counter] in placed_tiles:
				append_status = False

			elif path[counter] == target_tile.return_position() and counter != 0:
				append_status = False
			counter += 1

		if append_status:
			clear_winning_paths.append(path)

	try:
		minimum_path = clear_winning_paths[0]
		for path in clear_winning_paths:
			if len(path) < len(minimum_path):
				minimum_path = path
	except:
		print ("BIG ERROR ")
		minimum_path = [target_tile.return_position()]
		#Here I should call a function to get a more complex shuffler 


	return minimum_path

def initiate_tile_move(quest_dict, starting_position, ending_position, target_tile, placed_tiles):
	target_position = target_tile.return_position()
	target_path = find_tile_path(quest_dict, target_position, ending_position, placed_tiles, target_tile)
	status = analyze_tile_move(quest_dict, starting_position, ending_position, target_tile, target_path)
	quest_dict['break_recursion_status'] = False
	if status == "Move Into Empty":
		#Find the starting_position and then move into the tile
		for tile in quest_dict['tile_list']:
			#if tile.return_position() == starting_position:
			if tile == target_tile:
				list_variable = []
				holder = quest_dict['empty_position']
				list_variable.append(holder)
				quest_dict['empty_position'] = tile.return_position()
				list_variable.append(tile.return_position())
				tile.set_new_position(holder)
				quest_dict['move_history'].append(list_variable)

				return quest_dict
	else:
		#Create a new path for the target tile
		empty_position = quest_dict['empty_position']

		#These are just my catchers
		if len(target_path) == 1:
			quest_dict['break_recursion_status'] = True
			return quest_dict

		empty_path = find_tile_path(quest_dict, empty_position, target_path[1], placed_tiles, target_tile)

		#These are just my catchers
		if len(empty_path) == 1:
			quest_dict['break_recursion_status'] = True
			return quest_dict

		counter = 1
		while counter < len(empty_path):
			for tile in quest_dict['tile_list']:
				if tile.return_position() == empty_path[counter]:
					#Swap em
					list_variable = []
					holder = quest_dict['empty_position']
					list_variable.append(holder)
					quest_dict['empty_position'] = tile.return_position()
					list_variable.append(tile.return_position())
					tile.set_new_position(holder)
					quest_dict['move_history'].append(list_variable)

			counter += 1

		quest_dict = initiate_tile_move(quest_dict, starting_position, ending_position, target_tile, placed_tiles)
		
	return quest_dict

def move_unecessary_tiles(quest_dict, winning_path, direction_path):
	'''
	I may need to consider moving the second part of the puzzle and completing a portion before starting still

	'''
	#Find unecessary tiles that will clutter the board.

	second_path = quest_dict['second_direction_path']
	second_length = len(quest_dict['second_direction_path'])
	midpoint = int(second_length / 2) 
	blank_counter = 0
	clutter_tiles = []
	for tile in quest_dict['tile_list']:
		if tile.return_direction_list() == [False,False,False,False]:
			blank_tile = tile
			clutter_tiles.append(tile)
			blank_counter += 1
		elif tile.return_direction_list() not in direction_path and tile.return_direction_list() not in second_path:
			clutter_tiles.append(tile)
		#Since I am looking for tiles that are more near the middle I just want to check if its somewhere near
		elif tile.return_direction_list() not in direction_path and (tile.return_direction_list() == second_path[midpoint] \
			or tile.return_direction_list() == second_path[midpoint + 1] or tile.return_direction_list() == second_path[midpoint - 1]):
			clutter_tiles.append(tile)

	#Locate suitable corner
	safe_positions = []
	corner_tiles = [1, quest_dict['width'], quest_dict['width']*quest_dict['width'],quest_dict['width']*quest_dict['width'] - quest_dict['width']+1]

	point_1 = quest_dict['initial_starting_position']
	point_2 = quest_dict['initial_ending_position']
	point_3 = quest_dict['second_ending_position']

	counter = 0
	while counter < len(corner_tiles):
		if counter == 0:
			horizontal_increment = 1
			vertical_increment = quest_dict['width']
		elif counter == 1:
			horizontal_increment = -1
			vertical_increment = quest_dict['width']
		elif counter == 2:
			horizontal_increment = -1
			vertical_increment = -quest_dict['width']
		else:
			horizontal_increment = 1
			vertical_increment = - quest_dict['width']

		position = corner_tiles[counter]
		if position + horizontal_increment in winning_path or position + vertical_increment in winning_path:
			pass
		else:
			if position == point_1 or position + horizontal_increment == point_1 or position + vertical_increment == point_1:
				pass
			elif position == point_2 or position + horizontal_increment == point_2 or position + vertical_increment == point_2:
				pass
			elif position == point_3 or position + horizontal_increment == point_3 or position + vertical_increment == point_3:
				pass
			else:
				safe_positions.append(position)
				safe_positions.append((position + horizontal_increment))
				safe_positions.append((position + vertical_increment))

		counter += 1
	'''
	Basically just take this portion and start writing a little bit for it to move the unecessary out of the way
	'''
	placed_tiles = []
	placed_clutter_tiles = []
	for index, end_position in enumerate(safe_positions):
		if index < blank_counter:
			#Find a blank tile and move it to the position
			for tile in clutter_tiles:
				if tile.return_direction_list() == [False,False,False,False] and tile not in placed_clutter_tiles:
					target_tile = tile
					target_position = target_tile.return_position()
					ending_position = end_position
					tile_path = find_tile_path(quest_dict, target_position, ending_position, placed_tiles, target_tile)
					while target_tile.return_position() != ending_position:
						target_position = target_tile.return_position()
						quest_dict = initiate_tile_move(quest_dict, target_position, ending_position, target_tile, placed_tiles)

					placed_clutter_tiles.append(tile)
					break
		else:
			for tile in clutter_tiles:
				if tile not in placed_clutter_tiles:
					target_tile = tile
					target_position = target_tile.return_position()
					ending_position = end_position
					tile_path = find_tile_path(quest_dict, target_position, ending_position, placed_tiles, target_tile)
					while target_tile.return_position() != ending_position:
						target_position = target_tile.return_position()
						quest_dict = initiate_tile_move(quest_dict, target_position, ending_position, target_tile, placed_tiles)

					placed_clutter_tiles.append(tile)
					break

	return quest_dict

def choose_new_target_tile(quest_dict, winning_path, placed_tiles, target_tile, target_index):
	quest_dict['tried_new_tile'] = True
	target_direction_list = target_tile.return_direction_list()
	old_target_position = target_tile.return_position()

	possible_other_tiles = []
	for tile in quest_dict['tile_list']:
		if tile.return_direction_list() == target_direction_list and tile.return_position() != old_target_position:
			if tile.return_position() not in placed_tiles:
				possible_other_tiles.append(tile)
	
	if len(possible_other_tiles) > 0:
		placed_tiles = move_cycle(quest_dict, winning_path, placed_tiles, possible_other_tiles[0], target_index)
	
	return placed_tiles
class tile():
	def  __init__(self, up_status, down_status, left_status, right_status, position):
		self.up_status = up_status
		self.down_status = down_status
		self.left_status = left_status
		self.right_status = right_status
		self.position = position

	def set_new_position(self, new_position):
		self.position = new_position

	def return_direction_list(self):
		direction_list = [self.up_status, self.down_status, self.left_status, self.right_status]
		return direction_list

	def return_position(self):
		return self.position

	def return_up_direction(self):
		return self.up_status

	def return_down_direction(self):
		return self.down_status

	def return_left_direction(self):
		return self.left_status

	def return_right_direction(self):
		return self.right_status

	def return_blank_status(self):
		blank_status = False
		if self.up_status == False and self.down_status == False and self.left_status == False and self.right_status == False:
			blank_status = True

		return blank_status



