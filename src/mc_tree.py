class Node(object):
	"""docstring for Node"""
	def __init__(self, name):
		self.name = name
		self.rightnodes = {}
		self.endvalue = False

	def has_node(self, name):
		return name in self.rightnodes.keys()

	def add_node(self, name):
		if not self.has_node(name):
			self.rightnodes[name] = Node(name)
		return self.rightnodes[name]

	def get_node(self, name):
		return self.rightnodes[name]


def _check_node(node, name):
	return node.get_node(name)

def _move_right(node, name):
	return node.add_node(name)

def walk(startnode, node_names):
	try:
		ret_val = reduce(_check_node, node_names, startnode)
	except KeyError:
		return False
	return ret_val

def build(startnode, node_names):
	ret_val = reduce(_move_right, node_names, startnode)
	return ret_val

if __name__ == '__main__':
	basenode = Node('basenode')
	build(basenode, 'Searchterm').endvalue=True
	print(walk(basenode, 'Searchterm').endvalue)

		