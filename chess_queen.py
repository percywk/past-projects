

def call_chess_queen_functions():
	chess_dict = {}
	create_board(chess_dict)
	reset_queen_positions(chess_dict)

	intersecting_dict, remaining_dict = generate_possibilities(chess_dict)
	flag = check_data(intersecting_dict, remaining_dict)
	print ("Flag: ", flag)
	
	group_quadrants(chess_dict)

	
	winning_coordinates = book_combinatoric(chess_dict, intersecting_dict, remaining_dict)
	color_winning_coordinates(chess_dict, winning_coordinates)
	color_winning_intersections(chess_dict, intersecting_dict, winning_coordinates)

	#Using Rotated Squares winning combinations  should be +- 2 along path (ASSUMING)
	#choose_with_rotated_square(chess_dict['all_tiles'], 8, 8, 8)

	#analyze_quadrant(chess_dict, 1, intersecting_dict, remaining_dict)
	#quadrants = chess_dict['quadrants']
	#domain = quadrants[1]
	#exhausted = queen_combinatoric(domain, intersecting_dict, remaining_dict)
	#cleaned = clean_exhausted_combinations(exhausted)
	#winning_shape = analyze_quadrant_exhausted(cleaned, domain)
	
	
	#This is not what I want to be doing with the system
	#domain = chess_dict['all_tiles']
	#exhausted = queen_combinatoric(domain, intersecting_dict, remaining_dict)
	#cleaned = clean_full_domain(exhausted, 8)
	#print ("Cleaned: ", cleaned)
	return chess_dict

'''
Simply used for testing. Not important.
'''
def test_functions(chess_dict):
	possible_moves = find_intersecting_tiles(chess_dict, 0)
	print ("Possible Moves: ")
	print (possible_moves)

def test_table(chess_dict, intersecting_dict, remaining_dict):
	coordinate_dict = {}

	alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	for coordinate in chess_dict['all_tiles']:
		coordinate_string = ""
		column = alphabet[coordinate % chess_dict['board_width']]
		row = coordinate // chess_dict['board_width']
		coordinate_string = str(row) + "-" + column
		coordinate_dict[coordinate] = coordinate_string

	test_table = Table(coordinate_dict, chess_dict['all_tiles'], intersecting_dict, remaining_dict)
	test_table.add_position(0)
	test_table.display_table()

	return_val = test_table.get_full_column('A')
	print ("COLUMN: ", return_val)
	return_val = test_table.get_full_row('0')
	print ("ROW: ", return_val)

	test_table.pop_last_position()
	test_table.display_table()
	return

def create_board(chess_dict):
	chess_dict['board_width'] = 8
	chess_dict['board_height'] = 8
	chess_dict['number_of_queens'] = 8
	all_tiles = []
	for i in range(chess_dict['board_width'] * chess_dict['board_height']):
		all_tiles.append(i)

	chess_dict['all_tiles'] = all_tiles
	return

def reset_queen_positions(chess_dict):
	chess_dict['queen_positions'] = []
	return

def find_intersecting_tiles(chess_dict, starting_position):
	possible_positions = []

	increments = []
	#Go Up
	increments.append(-1 * chess_dict['board_width'])
	#Go Down
	increments.append(chess_dict['board_width'])
	#Go Left
	increments.append(-1)
	#Go Right
	increments.append(1)
	#Go UP-Left
	increments.append(-1 * chess_dict['board_width'] - 1)
	#Go Up-Right
	increments.append(-1 * chess_dict['board_width'] + 1)
	#Go Down-Left
	increments.append(chess_dict['board_width'] - 1)
	#Go Down-Right
	increments.append(chess_dict['board_width'] + 1)

	tile_range = chess_dict['board_width'] * chess_dict['board_height'] - 1
	possible_positions.append(starting_position)

	vertical_edges, left_vertical, right_vertical = get_vertical_edge_tiles(chess_dict)
	for index, increment in enumerate(increments):

		if starting_position in left_vertical:
			if index == 4 or index == 6 or index == 2:
				continue

		if starting_position in right_vertical:
			if index == 5 or index == 7 or index == 3:
				continue

		current_position = starting_position
		out_of_bounds = False
		while not out_of_bounds:
			current_position += increment

			if increment == 1 or increment == -1:
				if (current_position + 1) % chess_dict['board_width'] == 0:
					out_of_bounds = True
				elif current_position % chess_dict['board_width'] == 0:
					out_of_bounds = True

			if current_position < 0 or current_position > tile_range:
				out_of_bounds = True
				break

			if index > 3: 
				if current_position in vertical_edges:
					out_of_bounds = True

			possible_positions.append(current_position)

	possible_positions = make_list_unique(possible_positions)
	possible_positions = sort_list(possible_positions)
	return possible_positions

def check_if_edge(chess_dict, current_position):
	edge_hit = False

	if (current_position + 1) % chess_dict['board_width']:
		edge_hit = True

	if current_position % chess_dict['board_width'] == 0:
		edge_hit = True

	if current_position // chess_dict['board_width'] == 0:
		edge_hit = True

	if current_position // chess_dict['board_width'] == (chess_dict['board_height'] - 1):
		edge_hit = True

	return edge_hit

def get_mirrored_positions(chess_dict, position):
	mirrored_positions = []

	return mirrored_positions

def check_data(intersecting_dict, remaining_dict):
	flag = "All Good"
	#This represents one of the winning combinations
	om_winning = [2,12,17,31,32,46,51,61]

	for position in om_winning:
		intersecting = intersecting_dict[position]
		for item in intersecting:
			if item == position:
				continue
			if item in om_winning:
				flag = "Intersection Error"

		remaining = remaining_dict[position]
		for sub_position in om_winning:
			if position == sub_position:
				continue

			if sub_position not in remaining:
				flag = "Remaining Error"
				print ("Position: ", position)
				print ("Failed: ", sub_position)
				print ("Remaining: ", remaining)
				print ("Intersecting: ", intersecting)

	return flag

def get_vertical_edge_tiles(chess_dict):
	board_width = chess_dict['board_width']
	vertical_edges = []
	left_vertical = []
	right_vertical = []

	for tile in chess_dict['all_tiles']:
		if tile % board_width == 0:
			vertical_edges.append(tile)
			left_vertical.append(tile)

		if (tile + 1) % board_width == 0:
			vertical_edges.append(tile)
			right_vertical.append(tile)

	return vertical_edges, left_vertical, right_vertical

def generate_possibilities(chess_dict):
	all_tiles = chess_dict['all_tiles']
	intersecting_dict = {}
	remaining_dict = {}
	for position in all_tiles:
		intersecting = find_intersecting_tiles(chess_dict, position)
		intersecting_dict[position] = intersecting

	for starting_position in all_tiles:
		intersecting = intersecting_dict[starting_position]
		remaining_positions = get_remaining(chess_dict, intersecting)
		remaining_dict[starting_position] = remaining_positions

	return intersecting_dict, remaining_dict

def get_remaining(chess_dict, intersecting):
	all_tiles = chess_dict['all_tiles']
	remaining = []
	for possibility in all_tiles:
		if possibility not in intersecting:
			remaining.append(possibility)

	return remaining


'''
Helper Functions
'''
def make_list_unique(list_parameter):
	new_list = []

	intermediate_set = set()
	for item in list_parameter:
		intermediate_set.add(item)

	for item in intermediate_set:
		new_list.append(item)

	return new_list

def make_list_unique_with_order(list_parameter):
	new_list = []

	for item in list_parameter:
		if item not in new_list:
			new_list.append(item)

	return new_list

def sort_list(list_parameter):
	list_unsorted = True
	while list_unsorted:
		list_unsorted = False

		for index in range(len(list_parameter) - 1):
			if list_parameter[index] > list_parameter[index + 1]:
				list_unsorted = True
				temp = list_parameter[index] + 1
				list_parameter[index] = list_parameter[index + 1]
				list_parameter[index + 1] = temp


	return list_parameter

def refine_list_to_domain(domain, list_parameter):
	refined_list = []

	for item in list_parameter:
		if item not in domain:
			continue
		else:
			refined_list.append(item)

	return refined_list

def refine_dict_to_domain(domain, dict_parameter):
	refined_dict = {}

	for key, value in dict_parameter.items():

		new_value = []
		for item in value:
			if item in domain:
				new_value.append(item)

		refined_dict[key] = new_value
	return refined_dict

def group_quadrants(chess_dict):
	quadrant_dict = {}
	quadrant_dict[1] = []
	quadrant_dict[2] = []
	quadrant_dict[3] = []
	quadrant_dict[4] = []

	all_tiles = chess_dict['all_tiles']
	board_width = chess_dict['board_width']
	board_height = chess_dict['board_height']

	horizontal_divider = board_width // 2
	vertical_divider = board_width // 2

	for horizontal_index in range(board_height):
		for width_index in range(board_width):
			position = horizontal_index * board_width + width_index

			if width_index < horizontal_divider:
				left = True
			else:
				left = False

			if horizontal_index >= vertical_divider:
				down = True
			else:
				down = False

			#Quadrant 1
			if left and not down:
				quadrant_dict[1].append(position)
			#Quadrant 2
			elif not left and not down:
				quadrant_dict[2].append(position)
			#Quadrant 3
			elif left and down:
				quadrant_dict[3].append(position)
			else:
				quadrant_dict[4].append(position)

	chess_dict['quadrants'] = quadrant_dict
	return quadrant_dict

def analyze_quadrant(chess_dict, quadrant_index, intersecting_dict, remaining_dict):
	quadrant_dict = chess_dict['quadrants']
	quadrant_domain = quadrant_dict[quadrant_index]

	for position in quadrant_domain:

		intersecting_positions = intersecting_dict[position]
		remaining_positions = remaining_dict[position]

		intersecting_positions = refine_list_to_domain(quadrant_domain, intersecting_positions)
		remaining_positions = refine_list_to_domain(quadrant_domain, remaining_positions)

		print ("I & R for : ", position)
		print (intersecting_positions)
		print (remaining_positions)

	return

def queen_combinatoric(domain, intersecting_dict, remaining_dict):
	all_combinations = []

	intersecting_dict = refine_dict_to_domain(domain, intersecting_dict)
	remaining_dict = refine_dict_to_domain(domain, remaining_dict)

	for position in domain:
		intersecting_positions = intersecting_dict[position]
		remaining_positions = remaining_dict[position]
		
		#Layout for our combinations
		initial_grouping = [[position], remaining_positions]
		all_combinations.append(initial_grouping)

	#Combinations that can't be worked
	exhausted_combinations = []
	while True:
		new_combinations = []
		if len(all_combinations) == 0:
			break

		for grouping in all_combinations:
			if len(grouping[1]) == 0:
				exhausted_combinations.append(grouping)
				continue

			for remaining_position in grouping[1]:
				intersecting_positions = intersecting_dict[remaining_position]
				new_remaining = refine_new_remaining(grouping[1], intersecting_positions)

				#Append to the new combinations
				list_variable = []
				taken_positions = []
				for item in grouping[0]:
					taken_positions.append(item)

				taken_positions.append(remaining_position)
				list_variable.append(taken_positions)
				list_variable.append(new_remaining)
				new_combinations.append(list_variable)
		

		all_combinations = new_combinations

	print ("Exhausted: ")
	print (exhausted_combinations)

	return exhausted_combinations

def refine_new_remaining(original_remaining, new_intersecting):

	#From the original if it exists in the intersecting remove it
	new_remaining = []
	for position in original_remaining:
		if position not in new_intersecting:
			new_remaining.append(position)

	return new_remaining

def clean_exhausted_combinations(exhausted_combinations):
	cleaned_combinations = []

	for grouping in exhausted_combinations:
		taken_tiles = grouping[0]
		#Completely useless discard
		empty_list = grouping[1]
		add_grouping = True
		for sub_grouping in cleaned_combinations:
			exists = compare_lists(taken_tiles, sub_grouping)
			if exists:
				add_grouping = False
				break

		if add_grouping:
			cleaned_combinations.append(taken_tiles)

	return cleaned_combinations

#Should only be used if I decide to use the full combinatoric
def clean_full_domain(exhausted, number_placed):
	winning = []
	for grouping in exhausted:
		placed_objects = grouping[0]
		if len(placed_objects) >= number_placed:
			winning.append(placed_objects)

	return winning


def compare_lists(list_one, list_two):
	if len(list_one) != len(list_two):
		return False

	equal = True
	for item in list_one:
		if item not in list_two:
			equal = False
			break

	return equal


def find_best_formation(chess_dict, domain, cleaned):
	winning = []

	'''
	Part of the idea is that I want to analyze the formation generated on a singular quadrant

	Can some rule be applied to the formation of the solution from the quadrant?

	Answering such a question may prove invaluable for understanding the heuristics of this problem.
	'''

	#Find the highest scoring
	max_positions = 0
	for grouping in cleaned:
		placed_objects = grouping[0]
		if len(placed_objects) > max_positions:
			max_positions = len(placed_objects)

	#Group the highest scoring together.
	most_placed = []
	for grouping in cleaned:
		placed_objects = grouping[0]
		if len(placed_objects) == max_positions:
			most_placed.append(placed_objects)



	return winning

#So I want to try and guess the general shape of the object from it's coordinates
def analyze_coordinates(domain_width, domain_height, domain, taken_coordinates):
	shape = "undefined"

	#Don't care about these.
	if len(taken_coordinates) == 1:
		shape = "dot"
		return shape
	elif len(taken_coordinates) == 2:
		shape = "line"
		return shape
	elif len(taken_coordinates) == 3:
		shape = "triangle"
		return shape

	row_dict = {}
	counter = 0
	sub_counter = 0
	for coordinate in domain:
		if counter in row_dict.keys():
			row_dict[counter].append(coordinate)
		else:
			row_dict[counter] = [coordinate]

		sub_counter += 1
		if sub_counter == domain_width:
			sub_counter = 0
			counter += 1

	#Square / rotated square
	#Scoring the coordinates
	row_column_score = {}
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	for row, column in row_dict.items():
		key = "" 
		key = key + str(row)

		for index, item in enumerate(column):
			row_column_score[key + "-" + alphabet[index]] = 0


	for coordinate in taken_coordinates:
		column_position = coordinate % domain_width
		#Not sure about this
		while column_position >= domain_width:
			column_position = column_position - domain_width

		column_letter = alphabet[column_position]

		#Not sure about this either
		for row_index, coordinates in row_dict.items():
			if coordinate in coordinates:
				row_position = row_index
				break

		key = str(row_position) + "-" + column_letter
		row_column_score[key] += 1

	shape = analyze_score_dict(row_column_score)
	return shape

def analyze_score_dict(score_dict):
	shape = "undefined"
	rows_unique = True
	columns_unique = True

	#All rows & columns unique?
	for key, occurrence in score_dict.items():
		if occurrence == 0:
			continue

		split_key = key.split("-")
		row = split_key[0]
		column = split_key[1]

		for sub_key, sub_occurrence in score_dict.items():
			if sub_occurrence == 0 or key == sub_key:
				continue

			split_sub_key = sub_key.split("-")
			sub_row = split_sub_key[0]
			sub_column = split_sub_key[1]

			if row == sub_row:
				rows_unique = False

			if column == sub_column:
				columns_unique = False


	#Are all rows and columns exhausted?
	row_dict = {}
	column_dict = {}
	for key, occurrence in score_dict.items():
		split_key = key.split("-")
		row = split_key[0]
		column = split_key[1]

		if row not in row_dict.keys():
			row_dict[row] = 0

		if column not in column_dict.keys():
			column_dict[column] = 0


	for key, occurrence in score_dict.items():
		if occurrence == 0:
			continue

		split_key = key.split("-")
		row_dict[split_key[0]] += 1
		column_dict[split_key[1]] += 1

	exhausted_rows = True
	exhausted_columns = True

	for key, value in row_dict.items():
		if value == 0:
			exhausted_rows = False

	for key, value in column_dict.items():
		if value == 0:
			exhausted_columns = False

	if rows_unique and exhausted_rows and columns_unique and exhausted_columns:
		shape = "rotated-square"

	return shape

def analyze_quadrant_exhausted(exhausted, domain):
	domain_width = 4
	domain_height = 4

	shape_dict = {}
	for grouping in exhausted:
		coordinates = grouping
		shape = analyze_coordinates(domain_width, domain_height, domain, coordinates)

		if shape in shape_dict.keys():
			shape_dict[shape] += 1
		else:
			shape_dict[shape] = 1

	winning_shape = "None"
	shape_sides = {"None":0, "triangle":3, "rotated-square":4, "square":4}

	for shape, occurrence in shape_dict.items():
		if shape_sides[shape] > shape_sides[winning_shape]:
			winning_shape = shape

	return

def choose_with_rotated_square(domain, rows, columns, number_of_placed):
	'''
	All I want to do is visualize a square within the system. 
	1: The square will occupy all points within the connected line
	2: The square will extend into every column/row
	3: The square will then have points chosen from inside of it
	'''

	#Create our row/column.
	#Coordiantes is a list with [1-A, 2-A, 1-B etc.]
	coordinates = []
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	counter = 0
	for index, position in enumerate(domain):
		if index % columns == 0:
			counter += 1

		column_position = position % columns
		grid_position = str(counter) + "-" + alphabet[column_position]
		coordinates.append(grid_position)

	#Row dict is the more useful version as I can maintain position
	row_dict = {}
	for index, position in enumerate(domain):
		row = position // columns

		if row in row_dict.keys():
			row_dict[row].append(position)
		else:
			row_dict[row] = [position]

	lowest_row = None
	for row_index, positions in row_dict.items():
		if lowest_row is None:
			lowest_row = row_index

		if row_index < lowest_row:
			lowest_row = row_index

	first_row = row_dict[lowest_row]
	print ("First Row: ", first_row)

	squares = {}
	for starting_position in first_row:
		rotated_square = create_rotated_square(domain, rows, columns, starting_position)
		squares[starting_position] = rotated_square


	print ("All Squares: ", squares)
	return

def create_rotated_square(coordinates, rows, columns, starting_position):
	#Assume starting position is at the top.
	rotated_square = []
	edge_hit = False

	width = columns
	rotated_square.append(starting_position)

	#Go Down Right
	current_position = starting_position
	if (current_position + 1) % columns == 0:
		edge_hit = True
	else:
		edge_hit = False

	while not edge_hit:
		current_position = current_position + width + 1
		rotated_square.append(current_position)
		if (current_position + 1) % columns == 0:
			edge_hit = True


	#Go Down Left
	if current_position // columns == (rows - 1):
		edge_hit = True
	else:
		edge_hit = False

	while not edge_hit:
		current_position = current_position + width - 1
		rotated_square.append(current_position)
		if (current_position) // columns == (rows - 1):
			edge_hit = True

	#Go Up Left
	if current_position % columns == 0:
		edge_hit = True
	else:
		edge_hit = False

	while not edge_hit:
		current_position = current_position - width - 1
		rotated_square.append(current_position)
		if current_position % columns == 0:
			edge_hit = True

	#Go Up Right
	if current_position // columns == 0:
		edge_hit = True
	else:
		edge_hit = False

	while not edge_hit:
		current_position = current_position - width + 1
		rotated_square.append(current_position)
		if current_position // columns == 0:
			edge_hit = True

	rotated_square = make_list_unique_with_order(rotated_square)
	return rotated_square


'''

BOOK TALKS ABOUT ~2100 Possible states originating from column based selection that greatly simplifies the problem?
OK --> Apparently they are only placing the queen in the first available column. Reducing the complexity then.

These heuristics can seem so random and hard to identify. If that works how would I have stumbled upon it?

Now that I have my squares I need to start trying to create subtle permutations of the square.
	1) Don't choose any squares in the initial diagonals.
	2) Choose squares that may appear to create a square.
	3) 

'''

def book_combinatoric(chess_dict, intersecting_dict, remaining_dict):
	coordinate_dict = {}

	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	for position in chess_dict['all_tiles']:
		row = position // chess_dict['board_width']
		column = position % chess_dict['board_width']

		key = str(position) + "-" + alphabet[column]
		coordinate_dict[position] = key

	#Row and column 0 indexed
	first_row = grab_from_coordinate_dict(coordinate_dict, "column", 0)

	table = Table(coordinate_dict, chess_dict['all_tiles'], intersecting_dict, remaining_dict)

	#Table Combinatoric
	table, winner_status = table_combinatoric(table)

	winning_coordinates = []
	if winner_status:
		print ("Grab Winning Information")
		winning_coordinates = table.grab_winning_information()

	return winning_coordinates

def grab_from_coordinate_dict(coordinate_dict, index_type, number):
	coordinates = []
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if index_type == "column":
		search_item = alphabet[number]
	else:
		search_item = str(number)

	for key, coordinate in coordinate_dict.items():

		if search_item in coordinate:
			coordinates.append(key)

	return coordinates


def table_combinatoric(table):
	table_complete = False
	winnner_status = False
	counter = 0
	while not table_complete:
		next_position = table.find_first_in_next_column()
		if next_position == None:
			table.pop_last_position()
		else:
			table.add_position(next_position)


		#table.display_table()
		table_complete = table.check_if_done()

		counter += 1
		if counter == 2000:
			break
		elif table_complete:
			print ("WINNER WINNER CHICKEN DINNER")
			print ("Counter status ", counter)
			winner_status = True

	return table, winner_status


def color_winning_coordinates(chess_dict, winning_coordinates):
	colors = ['red']
	color_dict = {}
	for item in winning_coordinates:
		color_dict[item] = colors[0]
	chess_dict['colored_winning'] = color_dict
	return



'''
Sorta doesn't do anything important.
Values can be intersected together. IE Postion 0 intersect every time with the last columns intersecting.
'''
def color_winning_intersections(chess_dict, intersecting_dict, winning_coordinates):
	intersecting_count_dict = {}
	colored_intersecting_dict = {}
	colors = ['purple', 'green', 'blue', 'cyan', 'lime', 'blueviolet', 'tan', 'yellow']

	for winning in winning_coordinates:
		intersecting_positions = intersecting_dict[winning]

		for position in intersecting_positions:
			if position == winning:
				continue

			if position not in intersecting_count_dict.keys():
				intersecting_count_dict[position] = 0
			else:
				intersecting_count_dict[position] += 1

	for position, occurrence in intersecting_count_dict.items():
		colored_intersecting_dict[position] = colors[occurrence]

	chess_dict['colored_intersecting_dict'] = colored_intersecting_dict
	return



class Table():

	def __init__(self, coordinate_dict, all_positions, intersecting_dict, remaining_dict):
		self.coordinate_dict = coordinate_dict
		self.all_positions = all_positions
		self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

		self.current_available = self.all_positions
		self.taken_coordinates = []
		self.tried_coordinates = []

		self.intersecting_dict = intersecting_dict
		self.remaining_dict = remaining_dict
		self.board_width = self.find_board_width()

	def add_position(self, new_position):
		self.taken_coordinates.append(new_position)
		self.tried_coordinates.append(new_position)
		
		intersecting_positions = self.intersecting_dict[new_position]

		new_available = []
		for position in self.current_available:
			if position not in intersecting_positions:
				new_available.append(position)

		self.current_available = new_available

	def pop_last_position(self):
		try:
			last_coordinate = self.taken_coordinates[-1]
		except:
			self.clear_all()
			return

		current_column = self.get_column_from_coordinate(last_coordinate)

		last_in_column = self.check_if_last_in_column()
		if last_in_column:
			self.clear_tried_from_current_column()

		new_coordinates = []
		for item in self.taken_coordinates:
			if item != last_coordinate:
				new_coordinates.append(item)
		self.taken_coordinates = new_coordinates
		
		new_intersecting = set()
		for taken in new_coordinates:
			intersecting = self.intersecting_dict[taken]
			for coordinate in intersecting:
				new_intersecting.add(coordinate)

		remaining_coordinates = []
		for coordinate in self.all_positions:
			if coordinate not in new_intersecting:
				remaining_coordinates.append(coordinate)

		self.current_available = remaining_coordinates

		if last_in_column:
			self.pop_last_position()
		return

	def clear_all(self):
		self.taken_coordinates = []
		self.tried_coordinates = []
		self.current_available = []

		return


	def find_first_in_next_column(self):
		#Find last column taken
		if len(self.taken_coordinates) == 0:
			target_column = None
		else:
			target_column = 'A'
			target_index = 0
			for coordinate in self.taken_coordinates:
				row_column = self.coordinate_dict[coordinate]
				split_row_column = row_column.split("-")
				column = split_row_column[-1]
				column_index = self.alphabet.index(column)
				if column_index > target_index:
					target_index = column_index
					target_column = self.alphabet[column_index]


		#Find first in self.current_available
		if target_column == None:
			target_column = self.get_full_column('A')
		else:
			next_column_index = self.alphabet.index(target_column) + 1
			next_column = self.alphabet[next_column_index]
			target_column = self.get_full_column(next_column)
			#Clear advanced tried
			self.remove_advanced_tried(target_column[0])

		winning_position = None
		for position in target_column:
			if position in self.current_available and position not in self.tried_coordinates:
				winning_position = position
				break

		return winning_position

	def display_table(self):
		print ("Taken: ", self.taken_coordinates)
		print ("Available: ", self.current_available)
		print ("Tried: ", self.tried_coordinates)
		#print ("Coordinate Dict: ", self.coordinate_dict)


	def get_full_column(self, column_letter):
		column = []
		for key, coordinate in self.coordinate_dict.items():
			split_coord = coordinate.split('-')
			if split_coord[-1] == column_letter:
				column.append(key)

		return column

	def get_full_row(self, row_number):
		row = []
		if not isinstance(row_number, str):
			row_number = str(row_number)

		for key, coordinate in self.coordinate_dict.items():
			split_coord = coordinate.split('-')
			if split_coord[0] == row_number:
				row.append(key)

		return row

	def get_column_from_coordinate(self, position):
		row_column = self.coordinate_dict[position]
		split = row_column.split("-")
		column_letter = split[-1]
		return self.get_full_column(column_letter)

	def check_if_done(self):
		table_complete = False

		if len(self.taken_coordinates) == 8:
			table_complete = True


		return table_complete

	def check_if_last_in_column(self):
		#self.taken_coordinates = []
		last_position = self.tried_coordinates[-1]
		column = self.get_column_from_coordinate(last_position)

		found_counter = 0
		for position in column:
			if position in self.tried_coordinates or position in self.taken_coordinates:
				found_counter += 1

		found_counter = 0
		for index in range(len(column) - 1, 0, -1):
			current_position = column[index]
			if current_position == last_position and found_counter == 0:
				return True

			if current_position not in self.tried_coordinates or current_position not in self.taken_coordinates:
				return False

		if found_counter == len(column):
			return True
		else:
			return False

	def clear_tried_from_current_column(self):
		new_tried = []
		last_position = self.tried_coordinates[-1]
		column = self.get_column_from_coordinate(last_position)
		for position in self.tried_coordinates:
			if position not in column:
				new_tried.append(position)

		self.tried_coordinates = new_tried


	def remove_advanced_tried(self, next_position):
		max_column_index = next_position % self.board_width
		remove_items = False
		for item in self.tried_coordinates:
			if (item % self.board_width) > max_column_index:
				remove_items = True
				break

		if not remove_items:
			return

		current_position = next_position + 1
		new_tried = []
		next_columns = []
		while current_position % self.board_width != 0:
			current_column = self.get_column_from_coordinate(current_position)

			for item in current_column:
				next_columns.append(item)
			current_position += 1

		for item in self.tried_coordinates:
			if item not in next_columns:
				new_tried.append(item)

		self.tried_coordinates = new_tried

	def find_board_width(self):
		alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		max_index = 0
		alphabet_index = 0
		for key, coordinate in self.coordinate_dict.items():
			if key > max_index:
				max_index = key

		row_column = self.coordinate_dict[max_index]
		split_row_column = row_column.split("-")
		final_letter = split_row_column[-1]
		alphabet_index = alphabet.index(final_letter) + 1

		return alphabet_index

	def grab_winning_information(self):
		if len(self.taken_coordinates) == 8:
			return self.taken_coordinates
		else:
			return None
































'''
DANCING LINKS ALGORITHMN? WHAT IS IT and IS IT A SOLUTION TO MEMORY ISSUES?


1) Recursive Table Search.
	a) Create table iterate through initial table
	b) Recursive create new table when determining new item --> iterate through that

2) Errors cause pop back
3) Not that sure it's a great idea but whatever.

'''
