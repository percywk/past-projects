
'''
Re-doing some of the cram functions
'''
def call_cram_rewrite_functions():
	cram_dict = {}
	#test_classes()

	create_board(cram_dict)
	create_objects(cram_dict)
	reset_object_positions(cram_dict)

	#place_object(cram_dict, cram_dict['object_list'][0], 18)

	possibility_dict, winning = generate_possibilities(cram_dict)
	associated_objs = find_obj_from_coordinates(possibility_dict, winning)

	print ("Associated")
	print (associated_objs)

	place_objects(cram_dict, associated_objs)

	color_placed_objects(cram_dict)
	return cram_dict


def test_classes():
	new_obj = Object(4, 3)
	new_obj.set_obstacles([0, 2])
	print ("Initial Stage")
	new_obj.display()
	print ("Rotating")
	new_obj.rotate()
	new_obj.display()
	new_obj.rotate()
	new_obj.display()
	new_obj.rotate()
	new_obj.display()
	new_obj.rotate()
	new_obj.display()
	return

def create_board(cram_dict):
	board = []
	#Width = 11, Height = 7
	width = 11
	height = 7
	total_tiles = width * height
	for i in range(0, total_tiles):
		board.append(i)

	#Incluede Obstacles
	obstacles = [0,1,2,3,4,5,6,10,11,12,13,14,44,45,46,47,48,55,56,57,58,59,65,66,67,68,69,70,71,72,76]

	cram_dict['all_tiles'] = board
	cram_dict['obstacles'] = obstacles
	cram_dict['width'] = width
	cram_dict['height'] = height

	all_tiles = []
	for index in range(width * height):
		all_tiles.append(index)

	legal_tiles = []
	for tile in all_tiles:
		if tile in cram_dict['obstacles']:
			continue
		legal_tiles.append(tile)

	cram_dict['legal_tiles'] = legal_tiles
	return 

def create_objects(cram_dict):
	object_list = []
	#Good
	#lever
	obj_1 = Object(2, 4)
	obj_1.set_obstacles([0,2,4])
	obj_1.set_name("lever")
	object_list.append(obj_1)
	#Good
	#barrel
	obj_2 = Object(5,3)
	obj_2.set_obstacles([0,1,2,3])
	obj_2.set_name("barrel")
	object_list.append(obj_2)
	#???
	#grinder
	obj_3 = Object(3,2)
	obj_3.set_obstacles([0])
	obj_3.set_name("grinder")
	object_list.append(obj_3)
	#Good
	#stock
	obj_4 = Object(3,3)
	obj_4.set_obstacles([0,2])
	obj_4.set_name("stock")
	object_list.append(obj_4)
	#Good
	#feeder
	obj_5 = Object(4,4)
	obj_5.set_obstacles([1,2,3])
	obj_5.set_name("feeder")
	object_list.append(obj_5)
	#Good
	#final
	obj_6 = Object(2,3)
	obj_6.set_obstacles([5])
	obj_6.set_name("final")
	object_list.append(obj_6)

	cram_dict['object_list'] = object_list
	return

def reset_object_positions(cram_dict):
	cram_dict['object_positions'] = {}
	return

def color_placed_objects(cram_dict):
	colored_objects = {}
	color_cycle = ["red", "blue", "green", "purple", "pink", "yellow"]
	#object_positions': {'barrel': [15, 22, 23, 24, 25, 26, 33, 34, 35, 36, 37]}
	for name, coordinates in cram_dict['object_positions'].items():
		if name == "barrel":
			color = color_cycle[0]
		elif name == "lever":
			color = color_cycle[1]
		elif name == "grinder":
			color = color_cycle[2]
		elif name == "stock":
			color = color_cycle[3]
		elif name == "feeder":
			color = color_cycle[4]
		else:
			color = color_cycle[5]

		colored_objects[color] = coordinates
	cram_dict['colored_objects'] = colored_objects
	return

def place_object(cram_dict, obj, starting_coordinate):
	legal_tiles = cram_dict['legal_tiles']
	
	width = obj.get_width()
	height = obj.get_height()
	obstacles = obj.get_obstacles()
	name = obj.get_name()
	board_width = cram_dict['width']

	placed_positions = []
	for height_index in range(height):
		for width_index in range(width):
			current_object_position = height_index * width  + width_index

			if current_object_position not in obstacles:
				new_position = (height_index * board_width) + width_index + starting_coordinate
				placed_positions.append(new_position)

	taken_positions = []
	for obj_name, coordinates in cram_dict['object_positions'].items():
		if obj_name == name:
			continue
		for position in coordinates:
			taken_positions.append(position)

	for position in placed_positions:
		if position in cram_dict['obstacles']:
			return
		elif position in taken_positions:
			return

	cram_dict['object_positions'][name] = placed_positions
	return

def place_objects(cram_dict, associated_objs):
	
	for obj_name, positions in associated_objs.items():
		obj = get_object_from_name(cram_dict, obj_name)
		place_object_simplified(cram_dict, obj, positions)

	return

def get_object_from_name(cram_dict, obj_name):
	found_obj = None
	for obj in cram_dict['object_list']:
		if obj.get_name() == obj_name:
			found_obj = obj
			break

	return found_obj

def place_object_simplified(cram_dict, obj, target_positions):
	name = obj.get_name()
	cram_dict['object_positions'][name] = target_positions
	return

class Object():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.obstacles = []
		self.name = ""

	def set_name(self, name):
		self.name = name

	def set_obstacles(self, obstacles):
		self.obstacles = obstacles

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def get_obstacles(self):
		return self.obstacles

	def get_name(self):
		return self.name

	def rotate(self):
		new_width = self.height
		new_height = self.width

		#Set the new obstacles
		new_obstacles = []
		for obstacle in self.obstacles:
			row_location = obstacle // self.width
			column_location = obstacle % self.width

			new_column_location = new_width - row_location - 1
			new_row_location = column_location

			coordinate_position = new_row_location * new_width + new_column_location
			new_obstacles.append(coordinate_position)

		self.width = new_width
		self.height = new_height
		self.obstacles = new_obstacles
		return

	def display(self):
		print ("Width: ", self.width)
		print ("Height: ", self.height)
		print ("Obstacles: ", self.obstacles)



'''
Counting

Combinatorics Section
'''
def generate_all_possible_placements(cram_dict, obj):
	possibilities = []

	legal_tiles = cram_dict['legal_tiles']
	all_tiles = cram_dict['all_tiles']
	board_width = cram_dict['width']
	
	for rotation_index in range(0,4):
		width = obj.get_width()
		height = obj.get_height()
		obstacles = obj.get_obstacles()

		for starting_position in all_tiles:
			new_possibility = []
			add_possibility = True
			for height_index in range(height):
				for width_index in range(width):
					new_position = height_index * width + width_index
					if new_position not in obstacles:
						board_position = height_index * board_width + starting_position + width_index

						if board_position not in legal_tiles: 
							add_possibility = False
							break
						else:
							new_possibility.append(board_position)

				if not add_possibility:
					break

			if add_possibility:
				possibilities.append(new_possibility)

		obj.rotate()

	return possibilities


def clean_possibilities(cram_dict, possibilities):
	new_possibilities = []
	board_width = cram_dict['width']
	for grouping in possibilities:

		add_grouping = True
		for position in grouping:
			if (position + 1) % board_width == 0 and (position + 1) in grouping:
				add_grouping = False
				break 

		if add_grouping:
			new_possibilities.append(grouping)

	return new_possibilities

def remove_holes(cram_dict, possibilities):
	new_possibilities = []

	legal_tiles = cram_dict['legal_tiles']
	corners = get_board_corners()
	board_width = cram_dict['width']

	corner_dict = {}
	for corner in corners:
		up_position = corner - board_width
		down_position = corner + board_width
		left_position = corner - 1
		right_position = corner + 1

		if corner % board_width == 0 or left_position not in legal_tiles:
			left_position = None
		elif (corner + 1) % board_width == 0 or right_position not in legal_tiles:
			right_position = None

		if corner - board_width not in legal_tiles:
			up_position = None

		if corner + board_width not in legal_tiles:
			down_position = None

		list_variable = [up_position, down_position, left_position, right_position]
		corner_dict[corner] = list_variable

	for grouping in possibilities:
		add_grouping = True

		for corner_position, corner_list in corner_dict.items():
			if corner_position in grouping:
				continue

			found_counter = 0
			if corner_list[0] == None or corner_list[0] in grouping:
				found_counter += 1

			if corner_list[1] == None or corner_list[1] in grouping:
				found_counter += 1

			if corner_list[2] == None or corner_list[2] in grouping:
				found_counter += 1

			if corner_list[3] == None or corner_list[3] in grouping:
				found_counter += 1

			if found_counter == 4:
				add_grouping = False
				break

		if add_grouping:
			new_possibilities.append(grouping)
		
	return new_possibilities


#Grabbing corners
def get_board_corners():
	corners = [7, 9, 15, 21, 22, 33, 54, 60, 73, 75]
	return corners


'''
The next of the combinatoric generator is going to be the hardest in that I will
have several issues of expressionality that may be difficult to implement

I want to check remaining coordinates in all availables combinations to see if there exists sections that may 
make a portion of the board impossible to fill.

This requires: (on a macro level)
1. Grab all available combinatorics
2. Analyze each grouping with the others
3. Look for impossibilities
'''

def generate_possibilities(cram_dict):
	possibility_dict = {}

	for obj in cram_dict['object_list']:
		obj_name = obj.get_name()
		possibilities = generate_all_possible_placements(cram_dict, obj)

		#print ("Length: ", len(possibilities))
		#print (possibilities)
		possibilities = clean_possibilities(cram_dict, possibilities)
		possibilities = remove_holes(cram_dict, possibilities)
	
		obj_name = obj.get_name()
		possibility_dict[obj_name] = possibilities
	
	possibility_dict = remove_impossible_combinations(cram_dict, possibility_dict)

	total_options = analyze_combinatoric_feasability(possibility_dict)

	coordinate_placement_dict, potential_starting_locations = find_unique_positional_placements(cram_dict, possibility_dict)

	#Doesn't do anything
	#analyze_starting_positions(cram_dict, possibility_dict, coordinate_placement_dict, potential_starting_locations)
	
	winning = try_starting_position_combinatoric(cram_dict, possibility_dict, potential_starting_locations)
	return possibility_dict, winning

def remove_impossible_combinations(cram_dict, possibility_dict):
	new_possibility_dict = {}
	for obj_name, possibilities in possibility_dict.items():
		new_possibility_dict[obj_name] = []

	legal_tiles = cram_dict['legal_tiles']

	for obj_name, possibilities in possibility_dict.items():
		for possibility in possibilities:
			
			remaining_coordinates = get_remaining_coordinates(legal_tiles, possibility)
			coordinate_dict = create_coordinate_dict(legal_tiles, possibility)
			add_grouping = True

			#Delve into the other things
			for sub_name, sub_possibilities in possibility_dict.items():
				if obj_name == sub_name:
					continue

				for sub_possibility in sub_possibilities:
					continue_on = False

					for position in possibility:
						if position in sub_possibility:
							continue_on = True
							break

					if continue_on:
						continue

					for position in sub_possibility:
						coordinate_dict[position] += 1

			for position, occurrence in coordinate_dict.items():
				if occurrence == 0:
					add_grouping = False
					break

			if add_grouping:
				new_possibility_dict[obj_name].append(possibility)

	return new_possibility_dict

def get_remaining_coordinates(all_coordinates, *args):
	remaining_coordinates = []

	remove_coordinates = []
	for item in args:
		for coordinate in item:
			remaining_coordinates.append(coordinate)

	for coordinate in all_coordinates:
		if coordinate not in remove_coordinates:
			remaining_coordinates.append(coordinate)

	return remaining_coordinates

def create_coordinate_dict(legal_tiles, taken_positions):
	coordinate_dict = {}

	for position in legal_tiles:
		coordinate_dict[position] = 0

	for position in taken_positions:
		coordinate_dict[position] = 1

	return coordinate_dict

def analyze_combinatoric_feasability(possibility_dict):
	total_options = 0

	counter = 0
	for obj_name, possibilities in possibility_dict.items():
		if counter == 0:
			total_options += len(possibilities)
		else:
			total_options = total_options * len(possibilities)

		counter += 1

	return total_options

'''
Currently I can solve the problem by simply refining my selection set appropriately

Therefore I will be trying/testing some things which may not work at all.
'''

def find_unique_positional_placements(cram_dict, possibility_dict):
	coordinate_placement_dict = {}

	legal_tiles = cram_dict['legal_tiles']

	for position in legal_tiles:
		coordinate_placement_dict[position] = {}

	for obj_name, possibilities in possibility_dict.items():
		for possibility in possibilities:
			for coordinate in possibility:
				if obj_name in coordinate_placement_dict[coordinate].keys():
					coordinate_placement_dict[coordinate][obj_name].append(possibility)
				else:
					coordinate_placement_dict[coordinate][obj_name] = [possibility]

	#Collect Potential Starting Positions
	potential_starting_locations = {}

	for position, obj_dict in coordinate_placement_dict.items():
		total_options = 0
		for obj_name, possibilities in obj_dict.items():
			total_options += len(possibilities)

		if total_options < 4:
			#Add to the potential starting locations
			for obj_name, possibilities in obj_dict.items():
				if obj_name not in potential_starting_locations.keys():
					potential_starting_locations[obj_name] = possibilities
				else:
					for item in possibilities:
						if item not in potential_starting_locations[obj_name]:
							potential_starting_locations[obj_name].append(item)

	return coordinate_placement_dict, potential_starting_locations



'''
Doesn't Change Anything
'''
def analyze_starting_positions(cram_dict, possibility_dict, coordinate_dict, starting_positions):
	legal_tiles = cram_dict['legal_tiles']
	winning_starting_positions = {}

	remaining_coordinates = []
	for obj_name, possibilities in starting_positions.items():
		for possibility in possibilities:
			remaining_coordinates = get_remaining_coordinates(legal_tiles, possibility)
			add_to = True

			for remaining in remaining_coordinates:
				coordinate_intersection_dict = coordinate_dict[remaining]

				if len(coordinate_intersection_dict) == 1 and obj_name in coordinate_intersection_dict.keys():
					add_to = False

			if add_to:
				if obj_name in winning_starting_positions.keys():
					winning_starting_positions[obj_name].append(possibility)
				else:
					winning_starting_positions[obj_name] = [possibility]

	return



def refine_possibility_dict(possibility_dict, taken_positions):
	new_possibility_dict = {}

	for obj_name, possibilities in possibility_dict.items():
		for possibility in possibilities:
			add_possibility = True

			for position in possibility:
				if position in taken_positions:
					add_possibility = False
					break

			if add_possibility:
				if obj_name in new_possibility_dict.keys():
					new_possibility_dict[obj_name].append(possibility)
				else:
					new_possibility_dict[obj_name] = [possibility]

	return new_possibility_dict

def remove_obj_from_dict(possibility_dict, remove_name):
	new_possibility_dict = {}

	for obj_name, possibilities in possibility_dict.items():
		if obj_name == remove_name:
			continue

		new_possibility_dict[obj_name] = possibilities

	return new_possibility_dict

def try_starting_position_combinatoric(cram_dict, possibility_dict, starting_positions):
	possible_placements = []
	for starting_obj_name, object_starting_positions in starting_positions.items():
		for starting_position in object_starting_positions:
			placements = [starting_position]
			new_possibility_dict = refine_possibility_dict(possibility_dict, starting_position)
			new_possibility_dict = remove_obj_from_dict(new_possibility_dict, starting_obj_name)

			for obj_name, possibilities in new_possibility_dict.items():
				if len(possibilities) == 1:
					placements.append(possibilities[0])
					new_possibility_dict = refine_possibility_dict(new_possibility_dict, possibilities[0])
					new_possibility_dict = remove_obj_from_dict(new_possibility_dict, obj_name)

			all_placements = select_from_pool(placements, new_possibility_dict)

			for item in all_placements:
				possible_placements.append(item)

	print ("Length: ", len(possible_placements))
	winning = find_winning_combination(cram_dict['legal_tiles'], possible_placements)
	print ("Winning")
	print (winning)
	return winning


def select_from_pool(starting_placements, remaining_pool):
	all_placements = []
	all_placements.append(starting_placements)
	new_placements = []

	for key, values in remaining_pool.items():
		for placement in values:
			for item in all_placements:
				list_variable = []
				for sub_item in item:
					list_variable.append(sub_item)

				list_variable.append(placement)
				new_placements.append(list_variable)

		all_placements = new_placements
		new_placements = []

	return all_placements

def find_winning_combination(legal_tiles, possible_placements):
	winning_combinations = []

	length_of_legal = len(legal_tiles)
	highest_length = 0
	most_likely = None

	for grouping in possible_placements:
		found_coordinates = set()
		for sub_possibility in grouping:
			for position in sub_possibility:
				found_coordinates.add(position)


		if len(found_coordinates) == length_of_legal:
			winning_combinations.append(grouping)

		if len(found_coordinates) > highest_length:
			highest_length = len(found_coordinates)
			most_likely = grouping

	
	return winning_combinations


def find_obj_from_coordinates(possibilities, winning_coordinates):
	associated_objs = {}

	print (possibilities)
	for winning_grouping in winning_coordinates:
		for grouping in winning_grouping:
			grouping_length = len(grouping)
			for obj_name, obj_positions in possibilities.items():

				if grouping_length != len(obj_positions[0]):
					continue

				for positions in obj_positions:
					found_counter = 0
					for coordinate in grouping:
						if coordinate in positions:
							found_counter += 1
						else:
							break

					if found_counter == grouping_length:
						associated_objs[obj_name] = grouping


	return associated_objs