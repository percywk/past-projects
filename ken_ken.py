

def call_ken_ken_functions():
	ken_dict = {}
	create_board(ken_dict)
	set_clues(ken_dict)

	order_board(ken_dict, ken_dict['board_height'], ken_dict['board_width'])
	create_row_column_possibilities(ken_dict)


	#solve_ken_ken(ken_dict)
	#Testing out with better choose statement
	solve_v2(ken_dict)


	return ken_dict


def create_board(ken_dict):
	board_width = 6
	board_height = 6

	legal_numbers = [1,2,3,4,5,6]

	ken_dict['board_width'] = board_width
	ken_dict['board_height'] = board_height
	ken_dict['legal_numbers'] = legal_numbers

	index_possibilities = {}
	for index in range(0, board_width * board_height):
		index_possibilities[index] = legal_numbers

	ken_dict['index_possibilities'] = index_possibilities


def test_clue(ken_dict):
	number_of_items = 3
	equal_to = 8
	operation = 'addition'

	clue = Clue(equal_to, operation, number_of_items)
	winning = clue.check_possibilities()
	print ("Winning: ", winning)


	return

def set_clues(ken_dict):
	clue_1 = Clue(11, 'addition', 2, 0, 6)
	clue_2 = Clue(2, 'division', 2, 1, 2)
	clue_3 = Clue(20, 'multiplication',2, 3, 9)
	clue_4 = Clue(6, 'multiplication', 4, 4, 5, 11, 17)
	clue_5 = Clue(3, 'subtraction',2, 7,8)
	clue_6 = Clue(3, 'division', 2, 10, 16)
	clue_7 = Clue(240, 'multiplication', 4, 12, 13, 18, 19)
	clue_8 = Clue(6, 'multiplication', 2, 14, 15)
	clue_9 = Clue(6, 'multiplication', 2, 20, 26)
	clue_10 = Clue(7, 'addition', 3, 21,27,28)
	clue_11 = Clue(30, 'multiplication', 2, 22,23)
	clue_12 = Clue(6, 'multiplication', 2, 24, 25)
	clue_13 = Clue(9, 'addition', 2, 29, 35)
	clue_14 = Clue(8, 'addition', 3, 30, 31, 32)
	clue_15 = Clue(2, 'division', 2, 33, 34)

	all_clues = []
	all_clues.append(clue_1)
	all_clues.append(clue_2)
	all_clues.append(clue_3)
	all_clues.append(clue_4)
	all_clues.append(clue_5)
	all_clues.append(clue_6)
	all_clues.append(clue_7)
	all_clues.append(clue_8)
	all_clues.append(clue_9)
	all_clues.append(clue_10)
	all_clues.append(clue_11)
	all_clues.append(clue_12)
	all_clues.append(clue_13)
	all_clues.append(clue_14)
	all_clues.append(clue_15)
	ken_dict['all_clues'] = all_clues
	return

def order_board(ken_dict, number_of_rows, number_of_columns):
	column_dict = {}
	row_dict = {}

	alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	board_width = number_of_columns
	for index in range(number_of_rows*number_of_columns):
		row_index = index // board_width
		column_index = index % board_width
		column_letter = alphabet[column_index]

		if row_index not in row_dict.keys():
			row_dict[row_index] = [index]
		else:
			row_dict[row_index].append(index)

		if column_letter not in column_dict.keys():
			column_dict[column_letter] = [index]
		else:
			column_dict[column_letter].append(index)

	ken_dict['column_dict'] = column_dict
	ken_dict['row_dict'] = row_dict
	return

def choose(possibility_domain, number_items):
	total_possibilities = []
	counter = 0

	for item in possibility_domain:
		list_variable = [item]
		total_possibilities.append(list_variable)

	counter += 1
	while counter < number_items:
		new_possibilities = []

		for grouping in total_possibilities:
			for item in possibility_domain:
				if item not in grouping:
					list_variable = []
					for sub_item in grouping:
						list_variable.append(sub_item)
					list_variable.append(item)
					new_possibilities.append(list_variable)

		total_possibilities = new_possibilities
		counter += 1

	return total_possibilities

def reorder_grouping(possibility_grouping):
	reordered_grouping = []
	index_range = range(0, len(possibility_grouping))


	for item in index_range:
		list_variable = [item]
		reordered_grouping.append(list_variable)

	counter = 1
	while counter < len( possibility_grouping):
		new_groupings = []

		for grouping in reordered_grouping:
			for index in index_range:
				if index not in grouping:
					list_variable = []
					for item in grouping:
						list_variable.append(item)
					list_variable.append(index)
					new_groupings.append(list_variable)

		reordered_grouping = new_groupings
		new_groupings = []
		counter += 1

	reordered = []
	for index_grouping in reordered_grouping:
		list_variable = []
		for index in index_grouping:
			list_variable.append(possibility_grouping[index])

		reordered.append(list_variable)

	return reordered

def create_row_column_possibilities(ken_dict):
	row_dict = ken_dict['row_dict']
	column_dict = ken_dict['column_dict']
	row_column_possibilities = {}
	for key, values in column_dict.items():
		board_width = len(values)
		break

	possibilities = []
	for index in range(1, board_width + 1):
		possibilities.append(index)

	for key, values in row_dict.items():
		row_column_possibilities[key] = possibilities

	for key, values in column_dict.items():
		row_column_possibilities[key] = possibilities

	ken_dict['row_column_possibilities'] = row_column_possibilities

class Clue():
	def __init__(self, equal_to, operation, number_of_items, *args):
		self.coordinates = []
		self.order_coordinates()
		for item in args:
			self.coordinates.append(item)

		self.equal_to = equal_to
		self.operation = operation
		self.number_possibilities = [1,2,3,4,5,6]
		self.number_of_items = number_of_items
		self.possible_winning = []

	def remove_possibility(self, taken_number):
		new_possibilities = []
		for item in self.number_possibilities:
			if item != taken_number:
				new_possibilities.append(item)

	def generate_possibilities(self):
		possibilities = choose(self.number_possibilities, self.number_of_items)
		new_possibilities = []
		#Clean the possibilities
		for index, grouping in enumerate(possibilities):
			add_to = True
			for sub_index, sub_grouping in enumerate(new_possibilities):
				all_true = True
				for item in grouping:
					if item not in sub_grouping:
						all_true = False
						break

				if all_true:
					add_to = False
					break

			if add_to:
				new_possibilities.append(grouping)

		return new_possibilities

	def check_possibilities(self):
		evaluation = self.equal_to
		operation = self.operation

		winning = []
		possibilities = self.generate_possibilities()
		for grouping in possibilities:
			valid = self.check_single_possibility(grouping)

			if valid:
				winning.append(grouping)

		self.possible_winning = winning
		return winning

	def check_single_possibility(self, possible_grouping):
		evaluation = self.equal_to
		operation = self.operation
		valid = True
		equal_to = 0
		if operation == 'addition':
			for item in possible_grouping:
				equal_to += item

			if equal_to != evaluation:
				valid = False

		elif operation == 'multiplication':
			equal_to = possible_grouping[0]
			for index in range(1, len(possible_grouping)):
				equal_to = equal_to * possible_grouping[index]

			if equal_to != evaluation:
				valid = False

		elif operation == 'subtraction':
			valid = False
			reordered_items = reorder_grouping(possible_grouping)
			for grouping in reordered_items:
				current_value = grouping[0]

				for index in range(1, len(grouping)):
					current_value = current_value - grouping[index]

				if current_value == evaluation:
					valid = True
					break

		elif operation == "division":
			valid = False
			reordered_items = reorder_grouping(possible_grouping)
			for grouping in reordered_items:
				current_value = grouping[0]

				for index in range(1, len(grouping)):
					current_value = current_value / grouping[index]

				if current_value == evaluation:
					valid = True
					break

		return valid



	def get_coordinates(self):
		return self.coordinates

	def display_clue(self):
		print ("COORDINATES ", self.coordinates)
		print ("OPERATION ", self.operation)
		print ("EQUAL TO ", self.equal_to)
		print ("WINNING ", self.possible_winning)
		return

	def get_possibiilities(self):
		return self.number_possibilities

	def set_possibilities(self, new_possibilities):
		self.number_possibilities = new_possibilities
		return

	def check_outside_possibilities(self, possible_groupings):
		winning = []
		for grouping in possible_groupings:
			valid = self.check_single_possibility(grouping)

			if valid:
				winning.append(grouping)

		self.possible_winning = winning
		return winning

	def get_possible_winning(self):
		return self.possible_winning

	def order_coordinates(self):
		new_coordinates = []
		while len(new_coordinates) != len(self.coordinates):
			lowest_index = None
			for item in self.coordinates:
				if item not in new_coordinates and lowest_index == None:
					lowest_index = item

				if item not in new_coordinates and item < lowest_index:
					lowest_index = item

			new_coordinates.append(lowest_index)

	def set_possible_winning(self, new_winning):
		self.possible_winning = new_winning
		return

'''
Solving Logic.

1) Look for immediately solvable
2) Solve those.
3) Remove from the possibility locations.
4) DO BLAH BLAH

'''

def solve_ken_ken(ken_dict):
	find_absolute_winning(ken_dict)
	refine_clues_to_indexed_possibilities(ken_dict)

def find_absolute_winning(ken_dict):
	all_clues = ken_dict['all_clues']
	legal_numbers = ken_dict['legal_numbers'] 
	for clue in all_clues:
		winning = clue.check_possibilities()

		if len(winning) == 1:
			remaining_numbers = []
			for grouping in winning:
				for item in grouping:
					remaining_numbers.append(item)

			remove_numbers = []
			for number in legal_numbers:
				if number not in remaining_numbers:
					remove_numbers.append(number)

			for number in remove_numbers:
				clue.remove_possibility(number)

			#Check for all in one column / row
			clue_coordinates = clue.get_coordinates()

			single_row, single_column = determine_if_single_row_column(ken_dict, clue_coordinates)
			if single_row:
				remove_possibilities(ken_dict, clue_coordinates, remaining_numbers, "row")
			elif single_column:
				remove_possibilities(ken_dict, clue_coordinates, remaining_numbers, "column")


	return

def determine_if_single_row_column(ken_dict, clue_coordinates):
	all_in_row = True
	all_in_column = True

	column_dict = ken_dict['column_dict']
	row_dict = ken_dict['row_dict']

	#Check if all in one row
	row = None
	for coordinate in clue_coordinates:
		if row == None:
			row = coordinate // ken_dict['board_width']
		else:
			if coordinate // ken_dict['board_width'] != row:
				all_in_row = False

	#Check if all in one column
	column = None
	for coordinate in clue_coordinates:
		if column == None:
			column = coordinate % ken_dict['board_width']
		else:
			if coordinate % ken_dict['board_width'] != column:
				all_in_column = False


	return all_in_row, all_in_column

def remove_possibilities(ken_dict, coordinates, taken_possibilities, row_or_column):
	all_clues = ken_dict['all_clues']
	#Get the intersecting positions
	intersecting_positions = get_intersecting_positions(ken_dict, coordinates, row_or_column)
	other_intersecting = []
	for position in intersecting_positions:
		if position not in coordinates:
			other_intersecting.append(position)


	#Remove possibilities from intersecting
	#row_column_index = get_row_column_index(ken_dict, coordinates, row_or_column)
	for position in other_intersecting:
		possible = ken_dict['index_possibilities'][position]
		list_variable = []
		for item in possible:
			if item not in taken_possibilities:
				list_variable.append(item)

		ken_dict['index_possibilities'][position] = list_variable


	unique_taken = []
	for item in taken_possibilities:
		if item not in unique_taken:
			unique_taken.append(item)

	for position in coordinates:
		ken_dict['index_possibilities'][position] = unique_taken

	return

def get_intersecting_positions(ken_dict, taken_coordinates, row_or_column):
	intersecting_positions = []
	column_dict = ken_dict['column_dict']
	row_dict = ken_dict['row_dict']
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	if row_or_column == 'column':
		if isinstance(taken_coordinates, list):
			column_position = taken_coordinates[0] % ken_dict['board_width']
		elif isinstance(taken_coordinates, int):
			column_position = taken_coordinates % ken_dict['board_width']

		column_letter = alphabet[column_position]
		intersecting_positions = column_dict[column_letter]
	elif row_or_column == 'row':
		if isinstance(taken_coordinates, list):
			row_position = taken_coordinates[0] // ken_dict['board_width']
		elif isinstance(taken_coordinates, int):
			row_position = taken_coordinates // ken_dict['board_width']

		intersecting_positions = row_dict[row_position]

	return intersecting_positions

def get_row_column_index(ken_dict, taken_coordinates, row_or_column):
	if row_or_column == 'row':
		if isinstance(taken_coordinates, list):
			index = taken_coordinates[0] // ken_dict['board_width']
		elif isinstance(taken_coordinates, int):
			index = taken_coordinates // ken_dict['board_width']

	elif row_or_column == 'column':
		alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		if isinstance(taken_coordinates, list):
			index = taken_coordinates[0] % ken_dict['board_width']
		elif isinstance(taken_coordinates, int):
			index = taken_coordinates % ken_dict['board_width']

		index = alphabet[index]

	return index


'''
So I have a problem currently where clues may have a repeated digit in their solution.

1) Look for unique numbers within a clue set that are derived from a potential solution 
that is shared amongst other solutions.



I can technically place 5 at the 13 position 
'''
def refine_clues_to_indexed_possibilities(ken_dict):
	all_clues = ken_dict['all_clues']

	#refine clues to possibilities within index_possibilities
	for clue in all_clues:
		clue_coordinates = clue.get_coordinates()

		possible_numbers = []
		for position in clue_coordinates:
			possible = ken_dict['index_possibilities'][position]
			for item in possible:
				possible_numbers.append(item)

		possible_numbers = make_list_unique(possible_numbers)
		clue_possibilities = clue.get_possibiilities()

		for number in possible_numbers:
			if number not in clue_possibilities:
				clue.set_possibilities(possible_numbers)
				break

	return

def make_list_unique(list_parameter):
	new_list = []
	for item in list_parameter:
		if item not in new_list:
			new_list.append(item)

	return new_list

def choose_from_indexed_possibilities(ken_dict, coordinates):
	possibility_sequence = {}
	sequence_indexes = []
	possibiility_index = ken_dict['index_possibilities']

	counter = 0
	for index in coordinates:
		if counter == 0:
			first_item = index

		possibilities = possibiility_index[index]
		possibility_sequence[index] = (possibilities)
		sequence_indexes.append(index)
		counter += 1

	choose = []
	for item in possibility_sequence[first_item]:
		current_groupings = [[item]]
		considered_coordiantes = [first_item]
		new_groupings = current_groupings

		for index in range(1, len(sequence_indexes)):

			current_groupings = new_groupings
			new_groupings = []
			possibilities = possibility_sequence[sequence_indexes[index]]

			for grouping in current_groupings:
				bad_possibilities = remove_possibilities_if_shared(ken_dict, sequence_indexes[index], \
					considered_coordiantes, grouping)

				#Create our new possibilities
				new_possibilities = []
				for item in possibilities:
					if item not in bad_possibilities:
						new_possibilities.append(item)

				#Add to the new groupings
				for possibility in new_possibilities:
					list_variable = []
					for item in grouping:
						list_variable.append(item)

					list_variable.append(possibility)
					new_groupings.append(list_variable)



			considered_coordiantes.append(sequence_indexes[index])

		for grouping in new_groupings:
			choose.append(grouping)

	return choose

def remove_possibilities_if_shared(ken_dict, current_coordinate, considered_coordiantes, taken_values):

	#Determine if there is an intersection with considered coordinates
	#The considered coordinates maps one-to-one with the taken values
	intersecting_coordinates = []
	current_row = current_coordinate // ken_dict['board_width']
	current_column = current_coordinate % ken_dict['board_width']

	remove_values = []

	for coordinate in considered_coordiantes:
		con_row = coordinate // ken_dict['board_width']
		con_col = coordinate % ken_dict['board_width']

		if con_row == current_row  or con_col == current_column:
			intersecting_coordinates.append(coordinate)

	for coordinate in intersecting_coordinates:
		indexed_position = considered_coordiantes.index(coordinate)
		taken_value = taken_values[indexed_position]
		remove_values.append(taken_value)

	return remove_values

def display_board_state(ken_dict):
	all_clues = ken_dict['all_clues']
	index_pos = ken_dict['index_possibilities']
	for clue in all_clues:
		clue.display_clue()

	for index, possibilities in index_pos.items():
		print ("Position: ", index, " Poss: ", possibilities)
	return

def solve_v2(ken_dict):
	all_clues = ken_dict['all_clues']
	#Look for absolute winning combinations
	for clue in all_clues:
		clue_coordinates = clue.get_coordinates()
		possible_combinations = choose_from_indexed_possibilities(ken_dict, clue_coordinates)

		winning = clue.check_outside_possibilities(possible_combinations)
		if len(winning) == 1 or len(winning) == 2:
			#Remove the singular possibilites from winning combinations
			#IE first grouping removes 5,6 from 1st column

			#Find the taken
			taken_possibilities = []
			for grouping in winning:
				for item in grouping:
					taken_possibilities.append(item)

			single_row, single_col = determine_if_single_row_column(ken_dict, clue_coordinates)
			if single_row:
				remove_possibilities(ken_dict, clue_coordinates, taken_possibilities, "row")
			elif single_col:
				remove_possibilities(ken_dict, clue_coordinates, taken_possibilities, "column")

	for index in range(0, 8):
		refine_clue_winning_to_index_possibilities(ken_dict)
		find_absolute_winning_positions(ken_dict)
		refine_winning_possibilities_to_current(ken_dict)
		refine_index_possibilities_to_clues(ken_dict)
		remove_duplicate_index_poss(ken_dict)
		find_unique_numbers_row_col(ken_dict)

		finished = check_if_finished(ken_dict)

		if finished:
			break

	display_board_state(ken_dict)

	latin_square, row_fail, col_fail = check_if_latin_square(ken_dict)
	print ("LATIN SQUARE: ", latin_square)
	if not latin_square:
		print ("ROW FAILURE: ", row_fail)
		print ("COL FAILURE: ", col_fail)

	return


def find_unique_in_clues(ken_dict):
	indexed_possibilities = ken_dict['index_possibilities']
	all_clues = ken_dict['all_clues']

	for clue in all_clues:
		clue_coordinates = clue.get_coordinates()
		possible_winning = clue.get_possible_winning()

		#Probably won't work for these.
		if len(possible_winning) > 3 or len(possible_winning) == 1:
			continue

		for index, grouping in enumerate(possible_winning):
			for item_position, item in enumerate(grouping):
				consistent = True
				for sub_index, sub_grouping in enumerate(possible_winning):
					if index == sub_index:
						continue

					if sub_grouping[item_position] != item:
						consistent = False


				if consistent:
					winning_value = item
					winning_coordinate = clue_coordinates[item_position]

					#Set the value
					index_possibilities[winning_coordinate] = [winning_value]

def grab_all_other_intersecting(ken_dict, target_coordinate):
	other_intersecting = []
	target_row_index = target_coordinate // ken_dict['board_width']
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	target_col_index = alphabet[target_coordinate % ken_dict['board_width']]
	columns = ken_dict['column_dict']
	rows = ken_dict['row_dict']

	for position in columns[target_col_index]:
		if position != target_coordinate:
			other_intersecting.append(position)

	for position in rows[target_row_index]:
		if position != target_coordinate:
			other_intersecting.append(position)

	return other_intersecting

def remove_from_indexed_possibilities(ken_dict, target_coordinates, remove_possibility):
	for index, possibility_list in ken_dict['index_possibilities'].items():
		if index not in target_coordinates:
			continue

		list_variable = []
		for item in possibility_list:
			if item != remove_possibility:
				list_variable.append(item)

		ken_dict['index_possibilities'][index] = list_variable

	return

def refine_clue_winning_to_index_possibilities(ken_dict):
	#refine the clue's winning to current index possibilities
	for clue in ken_dict['all_clues']:
		clue_positions = clue.get_coordinates()
		clue_winning_possibilities = clue.get_possible_winning()

		new_groupings = []
		for possible_winning in clue_winning_possibilities:

			add_grouping = True
			for index, possibility in enumerate(possible_winning):
				corresponding_coordinate = clue_positions[index]

				if possibility not in ken_dict['index_possibilities'][corresponding_coordinate]:
					add_grouping = False

			if add_grouping:
				new_groupings.append(possible_winning)

		clue.set_possible_winning(new_groupings)

def find_absolute_winning_positions(ken_dict):
	all_clues = ken_dict['all_clues']

	for clue in all_clues:
		possible_winning = clue.get_possible_winning()
		if len(possible_winning) != 1:
			continue

		coordinates = clue.get_coordinates()
		winning = possible_winning[0]

		for index, taken_possibility in enumerate(winning):
			ken_dict['index_possibilities'][coordinates[index]] = [taken_possibility]

			intersecting_coordinates = grab_all_other_intersecting(ken_dict, coordinates[index])
			for intersecting in intersecting_coordinates:
				list_variable = [] 
				for possibility in ken_dict['index_possibilities'][intersecting]:
					if possibility != taken_possibility:
						list_variable.append(possibility)

				ken_dict['index_possibilities'][intersecting] = list_variable

	return


def refine_winning_possibilities_to_current(ken_dict):
	for clue in ken_dict['all_clues']:
		possible_winning = clue.get_possible_winning()
		coordinates = clue.get_coordinates()

		new_winning = []
		for winning_grouping in possible_winning:
			add_grouping = True
			for index, possibility in enumerate(winning_grouping):
				current_coordinate = coordinates[index]
				if possibility not in ken_dict['index_possibilities'][current_coordinate]:
					add_grouping = False
					break

			if add_grouping:
				new_winning.append(winning_grouping)

		clue.set_possible_winning(new_winning)

	return

def refine_index_possibilities_to_clues(ken_dict):
	for clue in ken_dict['all_clues']:
		possible_winning = clue.get_possible_winning()
		coordinates = clue.get_coordinates()

		for index, coordinate in enumerate(coordinates):
			possible_values = []

			for grouping in possible_winning:
				possible_values.append(grouping[index])

			possible_values = make_list_unique(possible_values)
			ken_dict['index_possibilities'][coordinate] = possible_values

	return

def remove_duplicate_index_poss(ken_dict):
	for coordinate, possibilities in ken_dict['index_possibilities'].items():
		if len(possibilities) == 1:
			#Grab all intersecting position
			remove_value = possibilities[0]
			intersecting_coordinates = grab_all_other_intersecting(ken_dict, coordinate)

			for intersecting in intersecting_coordinates:
				possibilities = ken_dict['index_possibilities'][intersecting]
				list_variable = []
				for possibility in possibilities:
					if possibility != remove_value:
						list_variable.append(possibility)

				ken_dict['index_possibilities'][intersecting] = list_variable

	return

def find_unique_numbers_row_col(ken_dict):
	row_dict = ken_dict['row_dict']
	column_dict = ken_dict['column_dict']

	row_or_column = {}
	for row_index, row_coordinates in row_dict.items():
		row_or_column[row_index] = row_coordinates

	for col_index, col_coordinates in column_dict.items():
		row_or_column[col_index] = col_coordinates

	for index, coordinates in row_or_column.items():
		possibility_count = generate_possibility_count()

		for coordinate in coordinates:
			possibilities = ken_dict['index_possibilities'][coordinate]

			if len(possibilities) == 1:
				possibility_count[possibilities[0]] += 20
				continue

			for number in possibilities:
				possibility_count[number] += 1

		winning, winning_keys = check_possibility_count(possibility_count)

		if winning:
			for coordinate in coordinates:
				for key in winning_keys:
					if key in ken_dict['index_possibilities'][coordinate]:
						ken_dict['index_possibilities'][coordinate] = [key]

	return




def check_if_finished(ken_dict):
	finished = True
	for index, possibilities in ken_dict['index_possibilities'].items():
		if len(possibilities) > 1:
			finished = False
			break

	return finished

def check_if_latin_square(ken_dict):
	row_dict = ken_dict['row_dict']
	column_dict = ken_dict['column_dict']
	latin_square = True

	row_failure = False
	col_failure = False

	for row_index, row_coordinates in row_dict.items():
		possibility_count = generate_possibility_count()

		for coordinate in row_coordinates:
			for key in ken_dict['index_possibilities'][coordinate]:
				possibility_count[key] += 1

		clean_count  = check_clean_possibility_count(possibility_count)

		if not clean_count:
			row_failure = True
			latin_square = False
			break

	for col_index, col_coordinates in column_dict.items():
		possibility_count = generate_possibility_count()

		for coordinate in col_coordinates:
			for key in ken_dict['index_possibilities'][coordinate]:
				possibility_count[key] += 1

		clean_count = check_clean_possibility_count(possibility_count)

		if not clean_count:
			col_failure = True
			latin_square = False
			break

	return latin_square, row_failure, col_failure



























'''
************
Helpers
************
'''

def generate_possibility_count():

	possibility_count = {}
	possibility_count[1] = 0
	possibility_count[2] = 0
	possibility_count[3] = 0
	possibility_count[4] = 0
	possibility_count[5] = 0
	possibility_count[6] = 0
	return possibility_count

def check_clean_possibility_count(possibility_count):
	all_one = True
	for key, count in possibility_count.items():
		if count != 1:
			all_one = False

	return all_one



def check_possibility_count(possibility_count):
	winning_indexes = []
	winning = False
	for key, count in possibility_count.items():
		if count == 1:
			winning = True
			winning_indexes.append(key)

	return winning, winning_indexes
