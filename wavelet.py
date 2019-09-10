import random


def call_wavelet_functions():
	wavelet_dict = {}
	working_text = grab_text()
	wavelet_dict['working_text'] = working_text

	create_wavelet_objects(wavelet_dict)
	all_good = check_leaves_and_nodes(wavelet_dict['leaves'], wavelet_dict['tree'].get_root_node())

	if not all_good:
		print ("**********************")
		print ("***RETURNING EARLY****")
		print ("**********************")
		return wavelet_dict

	check_tree(wavelet_dict, wavelet_dict['tree'], wavelet_dict['leaves'])

	find_paths(wavelet_dict)
	check_leaf_parents(wavelet_dict)
	add_binary_string_data(wavelet_dict)

	starting_node = wavelet_dict['tree'].get_root_node()
	item_found = search_tree_recursion(wavelet_dict, starting_node, "The", False)


	decompressed_text = decompress_tree(wavelet_dict)
	print ("Decompressed: ", decompressed_text)
	occurrence = find_occurrence(wavelet_dict, "the")

	path = add_leaf(wavelet_dict, "x")

	occurrence = find_occurrence(wavelet_dict, "x")

	item_found = search_tree_recursion(wavelet_dict, wavelet_dict['tree'].get_root_node(), "x", False)

	decompressed_text = decompress_tree(wavelet_dict)
	print ("Decompressed: ", decompressed_text)
	return wavelet_dict



def grab_text():
	working_text = "The amazing happy amazing man happily ran across the road."
	return working_text

def create_wavelet_objects(wavelet_dict):
	working_text = wavelet_dict['working_text']
	unique_words = set()
	words = working_text.split()

	for word in words:
		unique_words.add(word)

	wavelet_leafs = []
	for word in unique_words:
		new_leaf = WaveletLeaf()
		new_leaf.set_information(word)
		wavelet_leafs.append(new_leaf)

	#Creating Wavelet Heap
	number_of_leafs = len(wavelet_leafs)

	tree_obj = WaveletTree()
	tree_obj.create_tree_from_bottom(wavelet_leafs)

	
	wavelet_dict['leaves'] = wavelet_leafs
	wavelet_dict['tree'] = tree_obj


	return

#Simply for user testing 
#Technically Unecessary
def check_tree(wavelet_dict, wavelet_tree, leaves):
	root_node = wavelet_tree.get_root_node()
	found_leaves = []
	nodes = []

	wavelet_tree.traverse_tree(root_node, found_leaves, nodes)

	for leaf in found_leaves:
		print (leaf.get_information())

	return

def check_leaves_and_nodes(leaves, root):
	all_good = True
	error_count = 0

	for leaf in leaves:
		parent_node = leaf.get_parent()

		if parent_node == None:
			all_good = False
			error_count += 1

	left = root.get_left_node()
	right = root.get_right_node()

	if left == None and right == None:
		all_good = False
		error_count += 1

	if not all_good:
		print ("Errors: ", error_count)

	return all_good

def find_paths(wavelet_dict):
	paths = {}
	tree = wavelet_dict['tree']
	leaves = wavelet_dict['leaves']
	found_paths = tree.generate_paths(leaves)

	for grouping in found_paths:
		leaf_obj = grouping[-1]

		if isinstance(leaf_obj, WaveletLeaf):
			information = leaf_obj.get_information()
			paths[information] = grouping
		else:
			print ("*************************")
			print ("** ERROR IN FIND PATHS **")
			print ("*************************")


	'''
	Paths Seem to work can check with this shit.
	for key, value in paths.items():
		print (key)
		print (value)

		for index, item in enumerate(value):

			if isinstance(item, WaveletNode):
				left_node = item.get_left_node()
				right_node = item.get_right_node()

				if left_node == value[index + 1] or right_node == value[index + 1]:
					pass
				else:
					print ("Blah")
			else:
				continue
	'''

	wavelet_dict['paths'] = paths
	return

def add_binary_string_data(wavelet_dict):
	working_text = wavelet_dict['working_text']
	split_text = working_text.split()
	paths = wavelet_dict['paths']

	for word in split_text:
		current_path = paths[word]

		for index in range(0, len(current_path) - 1):
			node = current_path[index]
			next_node = current_path[index + 1]

			#left or right
			if isinstance(node, WaveletNode):
				if node.get_left_node() == next_node:
					node.add_direction("0")

				if node.get_right_node() == next_node:
					node.add_direction("1")
	return

#Attempting to make sure leaves have parents 
def check_leaf_parents(wavelet_dict):
	paths = wavelet_dict['paths']

	for key, path in paths.items():
		leaf = path[-1]
		if isinstance(leaf, WaveletNode):
			print ("In check_leaf_parents: Node at end of path")
			continue

		if not isinstance(leaf, WaveletLeaf):
			print ("Strange Error: ", leaf)
			continue

		if leaf.get_parent() == None:
			try:
				parent = path[-2]
				leaf.set_parent(parent)
			except:
				continue
	return

def search_tree_recursion(wavelet_dict, current_node, search_term, item_found):
	if isinstance(current_node, WaveletNode):
		go_left = True
		go_right = True

		if isinstance(current_node.get_left_node(), WaveletLeaf):
			go_left = False
			if current_node.get_left_node().get_information() == search_term:
				item_found = True

		if isinstance(current_node.get_right_node(), WaveletLeaf):
			go_right = False
			if current_node.get_right_node().get_information() == search_term:
				item_found = True

		if go_left:
			new_node = current_node.get_left_node()
			item_found = search_tree_recursion(wavelet_dict, new_node, search_term, item_found)

		if go_right:
			new_node = current_node.get_right_node()
			item_found = search_tree_recursion(wavelet_dict, new_node, search_term, item_found)

	return item_found

def decompress_tree(wavelet_dict):
	decompressed_text = ""
	root_node = wavelet_dict['tree'].get_root_node()

	root_node_bin_string = root_node.get_binary_string()
	
	final_path_taken = []
	final_path_taken.append(root_node)

	for index, direction in enumerate(root_node_bin_string):
		current_node = root_node
		current_string = root_node_bin_string
		if direction == "0":
			current_node = current_node.get_left_node()
		
		elif direction == "1":
			current_node = current_node.get_right_node()
		
		new_index = get_next_index_decompression(current_string, index)

		'''	
		Need to perculate down getting the new index each time.
		'''
		while isinstance(current_node, WaveletNode):
			new_string = current_node.get_binary_string()
			direction = new_string[new_index]
			
			if direction == "0":
				current_node = current_node.get_left_node()
			elif direction == "1":
				current_node = current_node.get_right_node()



			new_index = get_next_index_decompression(new_string, new_index)
			if index == len(root_node_bin_string) - 1:
				final_path_taken.append(current_node)
				

		decompressed_text += current_node.get_information() + " "

	return decompressed_text

def get_next_index_decompression(binary_string, current_index):
	current_value = binary_string[current_index]
	new_string = binary_string[:current_index + 1]

	occurrence = new_string.count(current_value)
	occurrence = occurrence - 1
	return occurrence

def find_leaf(wavelet_dict, current_node, search_term, leaf):
	
	if isinstance(current_node, WaveletNode):

		if isinstance(current_node.get_left_node(), WaveletLeaf):
			info = current_node.get_left_node().get_information()
			info = remove_whitespace(info)
			if info == search_term:
				leaf = current_node.get_left_node()
				return leaf

		if isinstance(current_node.get_right_node(), WaveletLeaf):
			info = current_node.get_right_node().get_information()
			info = remove_whitespace(info)
			if info == search_term:
				leaf = current_node.get_right_node()
				return leaf


		if isinstance(current_node.get_left_node(), WaveletNode):
			new_node = current_node.get_left_node()
			leaf = find_leaf(wavelet_dict, new_node, search_term, leaf)

		if isinstance(current_node.get_right_node(), WaveletNode):
			new_node = current_node.get_right_node()
			leaf = find_leaf(wavelet_dict, new_node, search_term, leaf)

	return leaf

def find_occurrence(wavelet_dict, search_term):
	occurrence = 0

	tree = wavelet_dict['tree']
	starting_node = tree.get_root_node()
	found_leaf = find_leaf(wavelet_dict, starting_node, search_term, None)
	print ("LEAF FOUND FOR OCCURENCE: ", found_leaf)

	if found_leaf != None:
		parent_node = found_leaf.get_parent()

		if parent_node is None:
			print ("************************************")
			print ("ILLEGAL EXCEPTION IN find_occurrence")
			print ("************************************")

		if parent_node.get_left_node() == found_leaf:
			occurrence = find_total_perculations(parent_node.get_binary_string(), "left")
		elif parent_node.get_right_node() == found_leaf:
			occurrence = find_total_perculations(parent_node.get_binary_string(), "right")

	return occurrence

def find_total_perculations(binary_string_info, left_or_right):
	occurrence = 0
	if left_or_right == "left":
		for item in binary_string_info:
			if item == "0":
				occurrence += 1

	elif left_or_right == "right":
		for item in binary_string_info:
			if item == "1":
				occurrence += 1

	return occurrence

def add_leaf(wavelet_dict, new_information):

	#Let's assume new_information will not update against current leafs.
	#So no leaf has information equal to new_information

	tree = wavelet_dict['tree']
	current_node = tree.get_root_node()

	#A loop function to go down.
	node_added = False
	path = []
	additional_node = None
	new_leaf = None

	while not node_added:
		add_direction = determine_add(current_node)

		if add_direction == "perculate":
			direction = choose_direction(new_information)
		elif add_direction == "left":
			direction = 0
		elif add_direction == "right":
			direction = 1

		if direction == 0:
			if isinstance(current_node, WaveletNode):
				current_node.add_direction("0")

			if isinstance(current_node.get_left_node(), WaveletNode):
				current_node = current_node.get_left_node()
			elif isinstance(current_node.get_left_node(), WaveletLeaf):
				additional_node, new_leaf = add_node_to_tree_rework(current_node, new_information, direction)
				node_added = True

		elif direction == 1:
			if isinstance(current_node, WaveletNode):
				current_node.add_direction("1")

			if isinstance(current_node.get_right_node(), WaveletNode):
				current_node = current_node.get_right_node()
			elif isinstance(current_node.get_right_node(), WaveletLeaf):
				additional_node, new_leaf = add_node_to_tree_rework(current_node, new_information, direction)
				node_added = True
		else:
			print ("ERROR")
		path.append(current_node)


		if additional_node != None:
			path.append(additional_node)
			path.append(new_leaf)
		elif new_leaf != None:
			path.append(new_leaf)

	valid_path = traverse_path(path)

	return path

def add_node_to_tree_rework(current_node, new_information, direction):
	additional_node = None
	left_node = current_node.get_left_node()
	right_node = current_node.get_right_node()

	new_leaf = WaveletLeaf()
	new_leaf.set_information(new_information)

	#Setting a default parent
	new_leaf.set_parent(current_node)

	if left_node is None and isinstance(right_node, WaveletLeaf):
		#Add to left
		current_node.add_direction("0")
		current_node.set_left_node(current_node)
		return additional_node

	elif isinstance(left_node, WaveletLeaf) and right_node is None:
		#Add to right
		current_node.add_direction("1")
		current_node.set_right_node(current_node)
		return additional_node


	new_node = WaveletNode()

	#If we are still here we need to create & rotate the new node
	if direction == 0 or direction == "left":
		information = get_partial_binary(current_node, "left")

		new_node.set_binary_string(information)

		new_node.set_left_node(left_node)
		new_node.set_right_node(new_leaf)
		new_node.add_direction("1")
		new_leaf.set_parent(new_node)
		current_node.set_left_node(new_node)

	
	elif direction == 1 or direction == "right":
		information = get_partial_binary(current_node, "right")

		new_node.set_binary_string(information)

		new_node.set_left_node(new_leaf)
		new_node.set_right_node(right_node)
		new_node.add_direction("0")
		new_leaf.set_parent(new_node)
		current_node.set_right_node(new_node)

	return new_node, new_leaf

def add_node_to_tree(current_node, new_information):
	#Get Information about the current node
	#Does it have both filled?
	additional_node = None
	left_node = current_node.get_left_node()
	right_node = current_node.get_right_node()

	new_leaf = WaveletLeaf()
	new_leaf.set_information(new_information)
	new_leaf.set_parent(current_node)


	'''	
	These first two probably never execute
	'''
	if left_node is None and isinstance(right_node, WaveletLeaf):
		#Add to left
		current_node.add_direction("0")
		current_node.set_left_node(current_node)

	elif isinstance(left_node, WaveletLeaf) and right_node is None:
		#Add to right
		current_node.add_direction("1")
		current_node.set_right_node(current_node)


	elif isinstance(left_node, WaveletLeaf) and isinstance(right_node, WaveletLeaf):
		#left or right
		direction = choose_direction(new_information)

		if direction == 0:
			new_node = WaveletNode()

			new_information = get_partial_binary(current_node, "left")
			new_node.set_binary_string(new_information)
			new_node.add_direction("1")

			new_node.set_left_node(left_node)
			new_node.set_right_node(new_leaf)
			new_leaf.set_parent(new_node)
			current_node.set_left_node(new_node)
			current_node.add_direction("0")

			additional_node = new_node

		elif direction == 1:
			new_node = WaveletNode()

			new_information = get_partial_binary(current_node, "right")
			new_node.set_binary_string(new_information)
			new_node.add_direction("0")

			new_node.set_left_node(new_leaf)
			new_node.set_right_node(right_node)
			new_leaf.set_parent(new_node)
			current_node.set_right_node(new_node)
			current_node.add_direction("1")

			additional_node = new_node

	elif isinstance(left_node, WaveletLeaf) and isinstance(right_node, WaveletNode):
		new_node = WaveletNode()
		new_information = get_partial_binary(current_node, "left")
		new_node.set_binary_string(new_information)
		new_node.add_direction("1")

		new_node.set_left_node(left_node)
		new_node.set_right_node(new_leaf)
		new_leaf.set_parent(new_node)
		current_node.set_left_node(new_node)
		#current_node.add_direction("0")

		additional_node = new_node


	elif isinstance(right_node, WaveletLeaf) and isinstance(left_node, WaveletNode):
		new_node = WaveletNode()
		new_information = get_partial_binary(current_node, "right")
		new_node.set_binary_string(new_information)
		new_node.add_direction("0")

		new_node.set_right_node(right_node)
		new_node.set_left_node(new_leaf)
		new_leaf.set_parent(new_node)
		current_node.set_right_node(new_node)
		#current_node.add_direction("1")

		additional_node = new_node

	elif left_node == None and right_node == None:
		print ("Illegal Structure handle anyways")

	else:
		print ("No Executions")

	return additional_node

def choose_direction(new_information):
	return random.randint(0,2)

def get_partial_binary(current_node, direction):
	binary_string = ""
	if direction == "left" or direction == 0:
		for item in current_node.get_binary_string()[:-1]:
			if item == "0":
				binary_string += item

	elif direction == "right" or direction == 1:
		for item in current_node.get_binary_string()[:-1]:
			if item == "1":
				binary_string += item

	return binary_string

def determine_add(current_node):
	direction = "perculate"
	left_node = current_node.get_left_node()
	right_node = current_node.get_right_node()

	if left_node is None:
		direction = "left"

	elif right_node is None:
		direction = "right"

	elif isinstance(left_node, WaveletNode) and isinstance(right_node, WaveletLeaf):
		direction = "right"

	elif isinstance(right_node, WaveletNode) and isinstance(left_node, WaveletLeaf):
		direction = "left"

	elif isinstance(left_node, WaveletLeaf) and isinstance(right_node, WaveletLeaf):
		direction = "left"

	return direction

def traverse_path(path):

	if isinstance(path[-1], WaveletNode):
		print ("Final Node: ", path[-1].display())
		valid_path = False
	else:
		print ("Final Leaf: ", path[-1].get_information())
		valid_path = True

	print (path)
	#Build a function to traverse a path for testing.
	for index, node in enumerate(path):
		if isinstance(node, WaveletNode):
			left_node = node.get_left_node()
			right_node = node.get_right_node()

			if index == len(path) - 1:
				continue

			if left_node == path[index + 1] or right_node == path[index + 1]:
				continue
			else:
				print ("Path Disconnect @ ", node)
				valid_path = False

		elif isinstance (node, WaveletLeaf):

			if index != len(path) - 1:
				valid_path = False

	if valid_path == False:
		print ("******************")
		print ("***INVALID PATH***")
		print ("******************")

	return valid_path

class WaveletTree():

	def __init__(self):
		self.root_node = None

	def get_root_node(self):
		return self.root_node

	def set_root_node(self, new_root_node):
		self.root_node = new_root_node

	def add_leaf(self, new_leaf):
		first_letter_index = self.get_first_letter_index(new_leaf)
		return

	def get_first_letter_index(self, new_leaf):
		if len(new_leaf) > 0:
			first_letter = new_leaf.get_information()[0]
		else:
			return

		first_letter = first_letter.lower()
		alphabet = "abcdefghijklmnopqrstuvwxyz"
		first_letter_index = 0
		try:
			first_letter_index = alphabet.index(first_letter)
		except:
			first_letter_index = 0

		return first_letter_index

	def go_left_or_right(self, new_leaf):
		left_or_right = 0
		total_ascii = 0
		for character in new_leaf.get_information():
			total_ascii += ord(character)

		left_or_right = total_ascii % 2

		if total_ascii == 0:
			direction = "left"
		else:
			direction = "right"

		return direction

	def create_and_rotate(self, collided_leaf, new_leaf):

		parent_node = collided_leaf.get_parent()
		#was collided left or right?
		left_child = parent_node.get_left_node()
		right_child = parent_node.get_right_node()

		direction = ""
		if left_child == collided_leaf:
			direction = "left"
		else:
			direction = "right"

		if direction == "left" and right_child == None:
			parent_node.set_right_node(new_leaf)
			return
		elif direction == "right" and left_child == None:
			parent_node.set_left_node(new_leaf)
			return

		new_node = WaveletNode()
		previous_information = parent_node.get_information()
		if direction == "right":
			new_information = ""
			for character in previous_information:
				if character == "1":
					new_information += "1"

		elif direction == "left":
			new_information = ""
			for character in previous_information:
				if character == "0":
					new_information += "0"

		new_node.set_information(new_information)

		if direction == "right":
			new_node.set_right_node(collided_leaf)
			new_node.set_left_node(new_leaf)
			parent_node.set_right_node(new_node)

		elif direction == "left":
			new_node.set_left_node(collided_leaf)
			new_node.set_right_node(new_leaf)
			parent_node.set_left_node(new_node)

		return

	def traverse_tree(self, current_node, leafs, visited_nodes):
		if isinstance(current_node, WaveletNode):
			if isinstance(current_node.get_left_node(), WaveletLeaf):
				leafs.append(current_node.get_left_node())
			
			if isinstance(current_node.get_right_node(), WaveletLeaf):
				leafs.append(current_node.get_right_node())
			
			if current_node.get_left_node() not in visited_nodes and isinstance(current_node.get_left_node(), WaveletNode):
				visited_nodes.append(current_node.get_left_node())
				self.traverse_tree(current_node.get_left_node(), leafs, visited_nodes)

			if current_node.get_right_node() not in visited_nodes and isinstance(current_node.get_right_node(), WaveletNode):
				visited_nodes.append(current_node.get_right_node())
				self.traverse_tree(current_node.get_right_node(), leafs, visited_nodes)


	def generate_paths(self, leaves):
		paths = []
		paths.append([self.get_root_node()])

		found_paths = []
		while len(found_paths) < len(leaves):
			
			new_paths = []
			for item in paths:
				last_item = item[-1]
				if isinstance(last_item, WaveletNode):

					if isinstance(last_item.get_left_node(), WaveletLeaf):

						list_variable = []
						for sub_item in item:
							list_variable.append(sub_item)
						list_variable.append(last_item.get_left_node())
						found_paths.append(list_variable)

					elif last_item.get_left_node() != None:
						list_variable = []
						for sub_item in item:
							list_variable.append(sub_item)

						list_variable.append(last_item.get_left_node())
						new_paths.append(list_variable)

					if isinstance(last_item.get_right_node(), WaveletLeaf):
						list_variable = []
						for sub_item in item:
							list_variable.append(sub_item)
						list_variable.append(last_item.get_right_node())
						found_paths.append(list_variable)

					elif last_item.get_right_node() != None:
						list_variable = []
						for sub_item in item:
							list_variable.append(sub_item)

						list_variable.append(last_item.get_right_node())
						new_paths.append(list_variable)

				else:
					continue

			paths = new_paths

		return found_paths

	def create_tree_from_bottom(self, all_leaves):
		tree = []

		for item in all_leaves:
			tree.append(item)

		counter = 0

		while len(tree) > 1:
			if counter == 12:
				break

			new_tree = []
			number_of_items = len(tree)
			for index in range(0, number_of_items, 2):
				item_one = tree[index]

				if index + 1 == number_of_items:
					new_tree.append(item_one)
					break

				item_two = tree[index + 1]
				
				#Connect Item One with Item 2 and Add

				new_node = WaveletNode()
				if item_one is not list and isinstance(item_one, WaveletLeaf):
					item_one.set_parent(new_node)
					new_node.set_left_node(item_one)
				elif isinstance(item_one, list):
					new_node.set_left_node(item_one[-1])


				if item_two is not list and isinstance(item_two, WaveletLeaf):
					item_two.set_parent(new_node)
					new_node.set_right_node(item_two)
				elif isinstance(item_two, list):
					new_node.set_right_node(item_two[-1])

				#Add all items not including any list

				list_variable = []
				if isinstance(item_one, list):
					for sub_item in item_one:
						list_variable.append(sub_item)
				else:
					list_variable.append(item_one)

				if isinstance(item_two, list):
					for sub_item in item_two:
						list_variable.append(sub_item)
				else:
					list_variable.append(item_two)

				list_variable.append(new_node)
				new_tree.append(list_variable)

			tree = new_tree

		self.root_node = tree[0][-1]
		first_nodes = self.find_first_nodes(tree[0])
		
		if len(first_nodes) > 0: 
			if (self.root_node != first_nodes[0]):
				print ("***********************")
				print ("* ERROR CREATING TREE *")
				print ("***********************")

		return

	def find_first_nodes(self, tree_list):
		first_nodes = []
		node_list = []

		for item in tree_list:

			if isinstance(item, WaveletLeaf):
				continue

			elif isinstance(item, WaveletNode):
				node_list.append(item)

		has_parent_nodes = []
		for node in node_list:

			if node.get_left_node() != None:
				has_parent_nodes.append(node.get_left_node())

			if node.get_right_node() != None:
				has_parent_nodes.append(node.get_right_node())

		for item in node_list:
			if item not in has_parent_nodes:
				first_nodes.append(item)

		return first_nodes

class WaveletNode():
	def __init__(self):
		self.binary_string = ""
		self.left_node = None 
		self.right_node = None

	#Basic Getters and Setters
	def set_binary_string(self, new_string):
		self.binary_string = new_string

	def set_left_node(self, new_left_node):
		self.left_node = new_left_node

	def set_right_node(self, new_right_node):
		self.right_node = new_right_node

	def get_binary_string(self):
		return self.binary_string

	def get_left_node(self):
		return self.left_node

	def get_right_node(self):
		return self.right_node

	def add_direction(self, new_direction):
		self.binary_string += new_direction

	def display(self):
		print ("Binary String: ", self.binary_string)
		print ("Left Node: ", self.left_node)

		if isinstance(self.left_node, WaveletLeaf):
			print ("\t -> ", self.left_node.get_information())

		print ("Right Node: ", self.right_node)

		if isinstance(self.right_node, WaveletLeaf):
			print ("\t -> ", self.right_node.get_information())


class WaveletLeaf():
	def __init__(self):
		self.information = ""
		self.parent = None
		self.parent_indicator = ""

	def set_information(self, new_information):
		self.information = new_information

	def set_parent(self, new_parent):
		self.parent = new_parent

	def set_parent_indicator(self, new_parent_indicator):
		self.parent_indicator = new_parent_indicator

	def get_information(self):
		return self.information

	def get_parent(self):
		return self.parent

	def get_parent_indicator(self):
		return self.parent_indicator



'''
**********************
	HELPER FUNCS
*********************
'''

def remove_whitespace(string_parameter):
	new_string = ""
	for character in string_parameter:
		if character == " ":
			continue

		new_string += character

	return new_string
