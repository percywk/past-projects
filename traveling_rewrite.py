import random
import math
import copy

def call_traveling_rewrite():
	traveling_dict = {}

	construct_random_network(traveling_dict, 50)
	#construct_test_network(traveling_dict)

	construct_hamiltonian_circuit(traveling_dict)

	#find_subgraphs_iter_bfs(traveling_dict) --> Not good bad idea in general

	find_subgraphs_linear_search(traveling_dict)

	found, seperation = find_minimum_degree_seperation(traveling_dict['node_list'], traveling_dict['node_list'][0], \
		traveling_dict['node_list'][-1])

	print (found)
	print (seperation)

	traveling_dict['js_test'] = 25

	#Junk bad heuristic that doesn't really make a lot of sense.
	#a_star_search(traveling_dict['node_list'], {}, traveling_dict['node_list'][0], traveling_dict['node_list'][-1])
	#a_star_rewrite(traveling_dict['node_list'], {}, traveling_dict['node_list'][0], traveling_dict['node_list'][-1])
	
	general_search(traveling_dict['node_list'], {}, traveling_dict['node_list'][0], traveling_dict['node_list'][-1])

	return traveling_dict


def construct_random_network(traveling_dict, total_nodes):
	node_list = []

	for index in range(total_nodes):
		new_node = Node()
		new_node.set_id(index)
		node_list.append(new_node)

	min_connections = math.ceil(total_nodes / 6)
	max_connections = math.floor(total_nodes / 2)

	for current_id, node in enumerate(node_list):
		total_connections = random.randint(min_connections, max_connections)

		for counter in range(total_connections):
			random_node = random.randint(0, total_nodes - 1)
			if random_node == current_id:
				continue
			else:
				node.add_connecting_node(node_list[random_node])

	for node in node_list:
		node.clean_node()

	traveling_dict['node_list'] = node_list
	return

def construct_test_network(traveling_dict):

	node_list = []
	#5 nodes total
	for index in range(5):
		new_node = Node()
		new_node.set_id(index)
		node_list.append(new_node)

	node_list[0].add_connecting_nodes(node_list[1], node_list[2])
	node_list[1].add_connecting_nodes(node_list[2], node_list[3])
	node_list[2].add_connecting_nodes(node_list[3], node_list[4])
	node_list[3].add_connecting_nodes(node_list[4], node_list[0], node_list[1])

	traveling_dict['node_list'] = node_list
	return

def make_random_node_a_sink(node_list):
	list_length = len(node_list)
	random_node = node_list[random.randint(0, list_length - 1)]
	random_node.remove_all_connections()
	return

def make_random_node_an_isolation(node_list):
	list_length = len(node_list)
	random_node = node_list[random.randint(0, list_length - 1)]
	random_node_id = random_node.get_id()

	random_node.remove_all_connections()

	for target_node in node_list:
		if random_node_id in target_node.get_connection_ids():
			target_node.remove_connection(random_node_id)

	return

def construct_hamiltonian_circuit(traveling_dict):
	#Number of connections will be n - 1
	#Choose some number of edges such that is true and check the solution.
	sorted_nodes = sort_nodes_by_num_connections(traveling_dict['node_list'])
	nodes_sorted = confirm_sorted_nodes_by_connections(sorted_nodes)

	#make_random_node_a_sink(sorted_nodes)
	#make_random_node_an_isolation(sorted_nodes)

	sink_nodes, isolated_nodes = check_for_sinks_and_isolations(sorted_nodes)
	if len(isolated_nodes) > 0:
		sorted_nodes = remove_isolated_nodes(isolated_nodes, sorted_nodes)
	if len(sink_nodes) > 0:
		sorted_nodes = rearrange_sink_nodes(sink_nodes, sorted_nodes)

	if not nodes_sorted:	
		raise Exception("YOU SUCK AT SORTING")
	elif len(sink_nodes) > 1:
		raise Exception("Impossible to create circuit. Sinks > 1")

	good_circuits = []
	bad_circuits = []
	for counter in range(100):
		randomized_nodes = randomize_node_list(sorted_nodes, sink_nodes)
		'''
		2 Things of history
		1: Successful creations
		2: Failed Creations
		Before adding to id check if the potential is in either
		If so choose another
		If no option can be chosen add to failed
		If successful add to successful creations
		'''
		circuit_created, visited_order = attempt_circuit_creation(traveling_dict, randomized_nodes, good_circuits, \
			bad_circuits)

		if not circuit_created:
			bad_circuits.append(visited_order)
		else:
			good_circuits.append(visited_order)

	
	print ("GOOD LENGTH: ", len(good_circuits))
	print ("BAD LENGTH: ", len(bad_circuits))

	return

def sort_nodes_by_num_connections(node_list):
	id_connections_dict = {}
	for node in node_list:
		id_connections_dict[node.get_id()] = len(node.get_connections())

	new_node_list = []
	original_length = len(node_list)
	while len(new_node_list) < original_length:

		if len(new_node_list) == 0:
			last_minimum = -1
		else:
			last_minimum = len(new_node_list[-1].get_connections())

		minimum_chosen = False
		current_minimum = -1
		for node_id, total_connections in id_connections_dict.items():
			if not minimum_chosen:
				if total_connections > last_minimum:
					minimum_chosen = True
					current_minimum = total_connections
			else:
				if total_connections < current_minimum and total_connections > last_minimum:
					current_minimum = total_connections

		target_nodes = get_nodes_with_num_connections(node_list, current_minimum)
		for node in target_nodes:
			new_node_list.append(node)

	return new_node_list
			
def get_nodes_with_num_connections(node_list, num_connections):
	found_nodes = []
	for node in node_list:
		if len(node.get_connections()) == num_connections:
			found_nodes.append(node)

	return found_nodes

def confirm_sorted_nodes_by_connections(node_list):
	confirmed = True
	for node_index in range(len(node_list) - 1):
		current_connections =  len(node_list[node_index].get_connections())
		next_connections = len(node_list[node_index + 1].get_connections())

		if next_connections < current_connections:
			confirmed = False

	return confirmed

def check_for_sinks_and_isolations(sorted_nodes):
	sinks = []
	isolations = []

	sinks_found = False
	for node_index, target_node in enumerate(sorted_nodes):
		if len(target_node.get_connections()) == 0:
			sinks.append(target_node.get_id())
			isolations.append(target_node.get_id())

	if len(sinks) == 0:
		return sinks, isolations


	#Check that some sinks have incoming connections & for isolations
	for node_id in sinks:
		for node_index, target_node in enumerate(sorted_nodes):
			connections = target_node.get_connections()
			for connection in connections:
				if connection.get_id() in sinks and connection.get_id() in isolations:
					isolations.remove(connection.get_id())

		if len(isolations) == 0:
			break

	#Remove the sink from the id
	for node_id in isolations:
		sinks.remove(node_id)

	return sinks, isolations

def rearrange_sink_nodes(sink_ids, sorted_nodes):
	new_sorted = []
	for non_sink in sorted_nodes:
		if non_sink.get_id() not in sink_ids:
			new_sorted.append(non_sink)

	for sink in sorted_nodes:
		if sink.get_id() in sink_ids:
			new_sorted.append(sink)
	
	return new_sorted

def remove_isolated_nodes(isolated_ids, sorted_nodes):
	new_sorted = []
	for target_node in sorted_nodes:
		if target_node.get_id() not in isolated_ids:
			new_sorted.append(target_node)

	return new_sorted

def randomize_node_list(sorted_nodes, sink_ids):
	new_list = []
	for node in sorted_nodes:
		if node.get_id() not in sink_ids:
			new_list.append(node)

	random.shuffle(new_list)
	for node in sorted_nodes:
		if node.get_id() in sink_ids:
			new_list.append(node)

	return new_list

def attempt_circuit_creation(traveling_dict, node_list, good_circuits, bad_circuits):
	circuit_created = True
	#--> sorting by num connections is not nec. correct

	if len(node_list) == 0:
		raise Exception ("No nodes to form circuit with")

	counter = 0
	current_node = node_list[0]		#can choose a better starting node
	visited_ids = [current_node.get_id()]
	while counter < len(node_list) - 1:

		#look at current connections
		current_connections = current_node.get_connections()

		node_found = False
		for node in current_connections:
			if node.get_id() not in visited_ids:

				potential_visited = copy.copy(visited_ids)
				potential_visited.append(node.get_id())

				#Check if in good circuits
				already_found_good = check_if_in_good_circuits(potential_visited, good_circuits)
				already_found_bad = check_if_in_bad_circuits(potential_visited, good_circuits)

				if already_found_bad or already_found_bad:
					continue

				node_found = True
				next_node = node
				break

		if not node_found:
			circuit_created = False
			break

		visited_ids.append(next_node.get_id())
		current_node = next_node
		counter += 1

	return circuit_created, visited_ids



def check_if_in_good_circuits(potential_visited, good_circuits):
	found = False
	if len(good_circuits) == 0:
		return found
	elif len(potential_visited) != len(good_circuits[0]):
		return found

	for grouping in good_circuits:
		counter = 0
		for index, node_id in enumerate(grouping):
			if potential_visited[index] == node_id:
				counter += 1
			else:
				break

		if counter == len(grouping):
			found = True
			break

	return found

def check_if_in_bad_circuits(potential_visited, bad_circuits):
	found = False

	for grouping in bad_circuits:

		if abs(len(grouping) - len(potential_visited)) > 2:
			continue

		counter = 0
		for index, node_id in enumerate(grouping):
			if index == len(potential_visited):
				break

			if potential_visited[index] == node_id:
				counter += 1
			else:
				break

		if counter == len(grouping):
			found = True
			break

	return found

class Node():
	def __init__(self):
		self.node_id = 0
		self.connected_nodes = []

	def set_id(self, new_id):
		self.node_id = new_id

	def add_connecting_nodes(self, *args):
		for item in args:
			if isinstance(item, Node):
				self.connected_nodes.append(item)

	def add_connecting_node(self, node_p):
		if isinstance(node_p, Node):
			self.connected_nodes.append(node_p)

	def clear_connecting_nodes(self):
		self.connected_nodes = []

	def get_id(self):
		return self.node_id

	def remove_connection(self, *args):
		remove_indexes = []
		for index, connecting_node in enumerate(self.connected_nodes):
			if connecting_node.get_id() in args:
				remove_indexes.append(index)

		new_connecting = []
		for index, connecting_node in enumerate(self.connected_nodes):
			if index not in remove_indexes:
				new_connecting.append(connecting_node)

		self.connected_nodes = new_connecting

	def clean_node(self):
		if len(self.connected_nodes) == 0:
			print ("NODE HAS NO OUT-GOING CONNECTIONS")

		remove_indexes = []
		unique_ids = []
		for index, node in enumerate(self.connected_nodes):
			if node.get_id() == self.node_id:
				remove_indexes.append(index)

			if node.get_id() in unique_ids:		#Make the id's unique
				remove_indexes.append(index)
			else:
				unique_ids.append(node.get_id())

		if len(remove_indexes) > 0:
			new_nodes = []
			for index, node in enumerate(self.connected_nodes):
				if index not in remove_indexes:
					new_nodes.append(node)

			self.connected_nodes = new_nodes



	def get_connections(self):
		return self.connected_nodes

	def remove_all_connections(self):
		self.connected_nodes = []

	def get_connection_ids(self):
		connection_ids = []
		for item in self.connected_nodes:
			connection_ids.append(item.get_id())

		return connection_ids

'''
Check for subgraphs

Try a different algorithm? --> Choosing of connections is the most important
'''

def look_for_subgraphs(node_list):
	incoming_connections = {}
	outgoing_connections = {}

	for node in node_list:
		node_id = node.get_id()
		connections = node.get_connections()
		outgoing_connections[node_id] = len(connections)

		for connection in connections():
			if isinstance(connection, node):
				connection_id = connection.get_id()
			elif isinstance(connection, int):
				connection_id = connection

			if connection_id in incoming_connections.keys():
				incoming_connections[connection_id] += 1
			else:
				incoming_connections[connection_id] = 1

	#Look for unbalanced items?
	average_incoming = 0
	for node_id, connetions in incoming_connections.items():
		average_incoming += connections

	average_incoming = average_incoming / len(incoming_connections.keys())
	std_dev_inc = find_std_deviation(incoming_connections, average_incoming)
	average_outgoing = 0
	for node_id, connections in outgoing_connections.items():
		average_outgoing += connections

	average_outgoing = average_outgoing / len(outgoing_connections.kes())
	std_dev_out = find_std_deviation(outgoing_connections, average_outgoing)

	outliers_inc = check_for_std_deviaion_outliers(incoming_connections, average_incoming, std_dev_inc)
	outliers_out = check_for_std_deviaion_outliers(outgoing_connections, average_outgoing, std_dev_out)

	if len(outliers_inc) > 0:
		print ("DO SOMETHING")
	else:
		print ("DO SOMETHING")

	return

def find_std_deviation(dict_parameter, average):
	average_diff_squares = []

	for key, count in dict_parameter.items():
		squared = (count - average) ** 2
		average_diff_squares.append(squared)

	total_items = len(dict_parameter.keys())

	sum_squares = 0
	for item in average_diff_squares:
		sum_squares += item

	std_dev = math.sqrt(sum_squares / total_items)
	return std_dev

def check_for_std_deviaion_outliers(dict_parameter, average, std_deviation):
	outliers = []
	for key, value in dict_parameter.items():
		if math.abs(value - average) > 2 * std_deviation:
			outliers.append(key)

	return outliers


'''
I think a better way to find a subgraph is to do a modification of a BFS that holds individual nodes in a 
cycle of heirarchy so something like:


{0: -- [starting_node] }
{1: -- [node_id, node_id]} etc.

Then we can just attempt to collapse the list looking for any solitary levels outside of the initial
'''


def find_subgraphs_iter_bfs(traveling_dict):
	node_list = traveling_dict['node_list']
	all_heirarchies = []
	max_searches = 10
	for counter in range(max_searches):
		starting_node = node_list[random.randint(0, len(node_list) - 1)]
		heirarchy = graph_BFS(starting_node, node_list)
		all_heirarchies.append(heirarchy)

	print (all_heirarchies)
	subgraph_points = analyze_hierarchy_dicts(node_list, all_heirarchies)
	print ("SUBGRAPH POINTS: ", subgraph_points)
	return


def graph_BFS(starting_node, node_list):
	heirarchy_dict = {}

	heirarchy_dict[starting_node.get_id()] = 0
	queue = [starting_node]
	history = [starting_node.get_id()]
	counter = 1

	while len(heirarchy_dict.keys()) < len(node_list) and len(queue) > 0:

		next_nodes = []
		for node in queue:
			connections = node.get_connections()
			for connection in connections:
				if connection.get_id() in history:
					continue

				next_nodes.append(connection)


		for node in next_nodes:
			heirarchy_dict[node.get_id()] = counter
			history.append(node.get_id())

		queue = next_nodes
		counter += 1

	return heirarchy_dict

def analyze_hierarchy_dicts(node_list, heirarchy_list):
	isolated_nodes = []

	for dictionary in heirarchy_list:
		heirarchy_count, min_level, max_level = count_heirarchy_levels(dictionary)

		isolated_levels = []
		for level, count in heirarchy_count.items():
			if count == 1 and level != max_level and level != min_level:
				isolated_levels.append(level)

		if len(isolated_levels) > 0:
			for node_id, level in dictionary.items():
				if level in isolated_levels:
					isolated_nodes.append(node_id)

	return isolated_nodes

def count_heirarchy_levels(heirarchy_dict):
	heirarchy_count = {}
	max_level = 0
	min_level = 0
	for key, level in heirarchy_dict.items():

		if level > max_level:
			max_level = level

		if level in heirarchy_count.keys():
			heirarchy_count[level] += 1
		else:
			heirarchy_count[level] = 1

	return heirarchy_count, min_level, max_level


'''
Doing a BFS to establish heirarchies is close but I don't think its the best way.

A node_point can be established outside by happenstance in very connected graphs.
Wasn't a bad idea. It would work for certain starting nodes in specific graphs.
Which is what I was probably imagining.
'''

def find_subgraphs_linear_search(traveling_dict):
	subgraph_points = []

	checked_nodes = []
	
	total_nodes = len(traveling_dict['node_list'])
	for node in traveling_dict['node_list']:
		if node.get_id() in checked_nodes:		#From previous iterations node is definately not a subgraph
			continue

		history = [node.get_id()]
		queue = find_previous_connected(traveling_dict['node_list'], node.get_id())

		#Use a modified search to grab all connections
		while len(history) < total_nodes and len(queue) > 0:
			current_node = queue[0]
			queue = queue[1:]

			if current_node.get_id() in history:
				continue

			#Append the queue
			history.append(current_node.get_id())		
			connected_nodes = current_node.get_connections()
			for connected in connected_nodes:
				if connected.get_id() != history[0]:		#Make sure we don't add the target node
					queue.append(connected)

		#Check the list generated by our search
		if len(history) == 1:
			subgraph_points.append(node)
		elif len(history) < total_nodes:
			subgraph_points.append(node)
		else:
			pass

	print ("SUBGRAPHS: ", subgraph_points)
	return subgraph_points

def find_previous_connected(node_list, target_id):
	previous = []
	for node in node_list:
		connections = node.get_connections()
		for sub_node in connections:
			if sub_node.get_id() == target_id:
				previous.append(sub_node)

	return previous

def get_previous_connected_dict(node_list):
	previous_dict = {}

	for node in node_list:
		connections = node.get_connections()
		for connection in connections:
			if connection.get_id() in previous_dict.keys():
				previous_dict[connection.get_id()].append(node)
			else:
				previous_dict[connection.get_id()] = [node]

	#Check for leftovers
	for node in node_list:
		if node.get_id() not in previous_dict.keys():
			previous_dict[node.get_id()] = []

	return previous_dict


'''
Minimum degree of seperation can identify nodes that have a large distance between
'''

def find_minimum_degree_seperation(node_list, starting_node, ending_node):
	degree_of_seperation = 0

	if starting_node.get_id() == ending_node.get_id():
		return True, degree_of_seperation

	ending_node_found = False
	history = [starting_node.get_id()]
	current_nodes = [starting_node]
	next_nodes = []
	

	while not ending_node_found:

		for node in current_nodes:
			connections = node.get_connections()
			for connection in connections:
				if connection.get_id() not in history:
					history.append(connection.get_id())
					next_nodes.append(connection)
				elif connection.get_id() == ending_node.get_id():
					ending_node_found = True


		#If we can't find the node just break.
		if len(next_nodes) == 0:
			break


		current_nodes = next_nodes
		next_nodes = []
		degree_of_seperation += 1

	return ending_node_found, degree_of_seperation


def create_random_connection_distance_dict(node_list):
	connection_distance_dict = {}
	cycle_options = []
	for index in range(25):
		cycle_options.append(random.randint(1, 25))

	counter = 0
	cycle_length = len(cycle_options)
	total_connections = 0
	for node in node_list:
		connections = node.get_connections()
		total_connections += len(connections)

		for connection in connections:
			key = str(node.get_id()) + "-" + str(connection.get_id())
			connection_distance_dict[key] = cycle_options[counter]

			counter += 1
			if counter == cycle_length:
				counter = 0
				random.shuffle(cycle_options)


	#Check that all connections have a distance
	if len(connection_distance_dict.keys()) != total_connections:
		raise Exception ("Total keys do not match!")


	return connection_distance_dict

def find_all_degrees_of_seperation(node_list, target_node):
	seperation_dict = {}

	queue = [target_node]
	history = [target_node.get_id()]
	next_nodes = []
	counter = 0
	while len(seperation_dict.keys()) < len(node_list):

		for current_node in queue:
			#Create entry in seperation dict
			seperation_dict[current_node.get_id()] = counter

			#Add descendents
			for connection in current_node.get_connections():
				if connection.get_id() not in history:
					next_nodes.append(connection)
					history.append(connection.get_id())

		if len(next_nodes) == 0:
			break

		queue = next_nodes
		next_nodes = []
		counter += 1

	#Refine for unreachables
	if len(seperation_dict.keys()) < len(node_list):
		for node in node_list:
			if node.get_id() not in seperation_dict.keys():
				seperation_dict[node.get_id()] = "Undefined"

	return seperation_dict

def a_star_search(node_list, connection_distance_dict, starting_node, ending_node):

	#Make sure distances are correct
	if not isinstance(connection_distance_dict, dict):
		connection_distance_dict = create_random_connection_distance_dict(node_list)
	elif len(connection_distance_dict.keys()) == 0:
		connection_distance_dict = create_random_connection_distance_dict(node_list)

	#Grab the heuristic
	seperation_dict = find_all_degrees_of_seperation(node_list, ending_node)
	print ("Ending Node: ", ending_node.get_id())
	print ("seperation_dict " , seperation_dict)
	reachable_count = len(seperation_dict.keys())
	print ("REACHABLE COUNT: ", reachable_count)

	#Formulate the A* search LUL JUST DO IT
	explored_nodes = {starting_node.get_id(): 0}
	
	end_reached = False
	counter = 0
	while not end_reached:
		
		#Grab the closest seperated.
		potential_node_dict =  grab_closest_seperated_keys(explored_nodes, seperation_dict)

		#From the potential, grab the next one that minimizes the distance.
		target_node, next_node, smallest_distance = minimize_distance(node_list, potential_node_dict, \
			seperation_dict, connection_distance_dict)
		
		print ("explored: ", explored_nodes)
		print ("potential_node_dict: ", potential_node_dict)
		print (target_node.get_id())
		print (next_node.get_id())
		print ("Smallest Distance: ", smallest_distance)

		total_distance = smallest_distance
		'''
		for node_id, distance in explored_nodes.items():
			if node_id == target_node.get_id():
				total_distance = distance + smallest_distance
		'''
		explored_nodes[next_node.get_id()] = total_distance
		if next_node.get_id() == ending_node.get_id():		#We are done.
			break

		counter += 1
		if counter == 3:
			break

	return



def grab_closest_seperated_keys(explored_nodes, seperation_dict):
	winning_key = None
	min_seperation = -1
	current_distance = -1

	#Find the least currently seperated.
	for node_id, distance in explored_nodes.items():
		if winning_key is None:
			winning_key = node_id
			min_seperation = seperation_dict[node_id]
			continue

		try:
			current_seperation = seperation_dict[node_id]
		except:
			raise Exception ("Exploration in A* couldn't grab node with heuristic")

		if current_seperation < min_seperation:
			winning_key = node_id
			min_seperation = current_seperation

	#Grab all of the same seperation
	potential_node_dict = {}
	for node_id, distance in explored_nodes.items():
		try:
			current_seperation = seperation_dict[node_id]
		except:
			raise Exception ("Exploration in A* couldn't grab node with heuristic")

		if current_seperation == min_seperation:
			potential_node_dict[node_id] = distance

	return potential_node_dict

def minimize_distance(node_list, potential_node_dict, seperation_dict, connection_distance_dict):

	#Assign node_id to class pointer
	id_list = []
	for key, value in potential_node_dict.items():
		id_list.append(key)

	node_id_mapping = assign_ids_to_pointer(node_list, id_list)


	#For each potential node check if a seperation + 1 exists
	target_node = None
	next_node = None
	smallest_distance = 0

	for node_id, distance in potential_node_dict.items():
		node = node_id_mapping[node_id]
		connections = node.get_connections()
		current_seperation = seperation_dict[node_id]

		for connection in connections:
			if seperation_dict[connection.get_id()] == current_seperation - 1:
				connection_key = get_connection_key(node, connection)
				if target_node is None:
					target_node = node
					next_node = connection
					smallest_distance = distance + connection_distance_dict[connection_key]
				elif distance + connection_distance_dict[connection_key] < smallest_distance:
					target_node = node
					next_node = connection
					smallest_distance = distance + connection_distance_dict[connection_key]

	return target_node, next_node, smallest_distance

def assign_ids_to_pointer(node_list, id_list):
	node_id_mapping = {}
	for node in node_list:
		if node.get_id() in id_list:
			node_id_mapping[node.get_id()] = node

	return node_id_mapping

def get_connection_key(first_node, second_node):

	return str(first_node.get_id()) + "-" + str(second_node.get_id())





'''
So the problem here is that degree of seperation isn't applicable for this project.
I don't think it is necessarilly a great idea.
I don't doubt it is doable, but I don't like the heuristic I have chosen. 
Any Degree of seperation heurisitc has already found the path anyways.
'''

def a_star_rewrite(node_list, connection_distance_dict, starting_node, ending_node):

	#Make sure distances are correct
	if not isinstance(connection_distance_dict, dict):
		connection_distance_dict = create_random_connection_distance_dict(node_list)
	elif len(connection_distance_dict.keys()) == 0:
		connection_distance_dict = create_random_connection_distance_dict(node_list)

	#Grab the heuristic
	seperation_dict = find_all_degrees_of_seperation(node_list, ending_node)

	explored_paths = [[starting_node]]
	end_reached = False
	counter = 0
	while not end_reached:
		print ("LOOP")
		print (explored_paths)
		minimum_seperation = None

		#Get all paths that have the least seperation.
		for path in explored_paths:
			final_degree_of_seperation = seperation_dict[path[-1].get_id()]
			if minimum_seperation is None:
				minimum_seperation = final_degree_of_seperation
			elif final_degree_of_seperation <  minimum_seperation:
				minimum_seperation = final_degree_of_seperation

		chosen_paths = []
		for path in explored_paths:
			final_degree_of_seperation = seperation_dict[path[-1].get_id()]
			if final_degree_of_seperation == minimum_seperation:
				chosen_paths.append(path)

		print ("CHOSEN", chosen_paths)
		if len(chosen_paths) == 0:
			break

		#From all chosen paths expand them
		for path in chosen_paths:
			final_node = path[-1]
			next_nodes = expand_node_path(final_node, seperation_dict, connection_distance_dict)

			print ("NEXT NODES: ", next_nodes)
			#choose the 2 that minimize the distance
			min_distances = {}
			max_items = 2

			for node in next_nodes:
				con_key = get_connection_key(final_node, node)
				distance = connection_distance_dict[con_key]
				add_to_min_distances(min_distances, max_items, node, distance)

			print ("MIN DISTANCES ", min_distances)
			for node_id, distance in min_distances.items():
				if node_id == ending_node.get_id():
					end_reached = True

				new_path = []
				for pointer in path:
					new_path.append(pointer)

				pointer = get_pointer_from_id(node_list, node_id)
				if pointer is not None:
					new_path.append(pointer)

				explored_paths.append(new_path)

		print ("FINAL EXPLORED: ", explored_paths)
		counter += 1
		if counter == 2:
			break

	'''
	Check if the thing has been reached.

	'''
	if end_reached:
		print ("GRAB THE NEXT ")

	return



def expand_node_path(final_node, seperation_dict, connection_distance_dict):
	next_nodes = []
	connections = final_node.get_connections()
	current_seperation = seperation_dict[final_node.get_id()]

	for connection in connections:
		if current_seperation - 1 == seperation_dict[connection.get_id()]:
			next_nodes.append(connection)


	return next_nodes

def add_to_min_distances(min_distances, max_items, node, distance):

	if len(min_distances.keys()) < max_items:
		min_distances[node.get_id()] = distance
	else:
		min_key = None
		less_than = []
		for key, current_distance in min_distances.items():
			if distance < current_distance:
				less_than.append(key)

		#Set the max distance
		if len(less_than) > 0:
			max_distance = min_distances[less_than[0]]
			max_key = less_than[0]
			for key in less_than:
				if min_distances[key] > max_distance:
					max_distance = min_distances[key]
					max_key = key

			del min_distances[max_key]
			min_distances[node.get_id()] = distance

	return

def get_pointer_from_id(node_list, node_id):
	for node in node_list:
		if node.get_id() == node_id:
			return node
	return None













'''
Given a node, I want to find the shortest path.

'''

def general_search(node_list, connection_distance_dict, starting_node, ending_node):
	if not isinstance(connection_distance_dict, dict):
		connection_distance_dict = create_random_connection_distance_dict(node_list)
	elif len(connection_distance_dict.keys()) == 0:
		connection_distance_dict = create_random_connection_distance_dict(node_list)


	#I want to do a heuristic search of some sort.
	seperation_dict = find_all_degrees_of_seperation(node_list, ending_node)

	current_seperation_level = seperation_dict[starting_node.get_id()]
	ending_seperation_level = seperation_dict[ending_node.get_id()]

	current_node = starting_node
	end_reached = False
	failed_nodes = []
	history = []
	counter = 0
	while not end_reached:

		#Get connections with seperation - 1
		connections = current_node.get_connections()
		next_seperation_level = current_seperation_level - 1
		possible_nodes = []
		for connection in connections:
			if seperation_dict[connection.get_id()] == next_seperation_level:
				possible_nodes.append(connection)

		#Check if that node has already been reached.
		possible_nodes = refine_possible_nodes(possible_nodes, failed_nodes)
		if len(possible_nodes) == 0:
			failed_nodes.append(current_node)
			current_node = get_previous_node(history, current_node)
			continue

		#Choose 1
		next_node = choose_next_node(possible_nodes, connection_distance_dict)
		if next_node.get_id() == ending_node.get_id():
			end_reached = True

		history.append(current_node)
		current_node = next_node
		current_seperation_level = next_seperation_level
		counter += 1			
		if counter == 50:		#If I ever get this shit running again. I swear.
			break

	return

def choose_next_node(possible_nodes, connection_distance_dict):
	if len(possible_nodes) == 0:
		return None

	chosen_node = possible_nodes[0]
	min_distance = connection_distance_dict[chosen_node.get_id()]

	for index in range(1, len(possible_nodes)): 
		if connection_distance_dict[possible_nodes[index].get_id()] < min_distance:
			chosen_node = possible_nodes[index]
			min_distance = connection_distance_dict[possible_nodes[index].get_id()]

	return chosen_node

def refine_possible_nodes(possible_nodes, failed_nodes):
	new_possible = []

	cleaned_failed = []
	for node in failed_nodes:
		if isinstance(node, Node):
			cleaned_failed.append(node.get_id())
		elif isinstance(node, int):
			cleaned_failed.append(node)

	for node in possible_nodes:
		if node.get_id() not in cleaned_failed:
			new_possible.append(node)


	return new_possible

def get_previous_node(history, current_node):
	if len(history) == 0:
		return None

	elif len(history) == 1:
		if isinstance(history[0], Node):
			if history[0].get_id() == current_node.get_id():
				return None
			else:
				return history[0]

		elif isinstance(history[0], int):
			if history[0] == current_node.get_id():
				return None
			else:
				return history[0]

	else:
		for index in range(len(history) - 1, -1, -1):
			current_item = history[index]
			if isinstance(current_item, Node):
				if current_item.get_id() != current_node.get_id():
					return current_item
			elif isinstance(current_item, int):
				if current_item == current_node.get_id():
					return current_item