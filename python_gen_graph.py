import random
import networkx as nx
import matplotlib.pyplot as plt

# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.


class Node:
    def __init__(self, value):
        """
        Initialize a new node with a given value.

        :param value: The value to store in the node.
        """
        self.value = value  # The value of the node
        self.children = []  # List to store child nodes (for tree structures)

    def add_child(self, child_node):
        """
        Add a child node to this node.

        :param child_node: The child node to add.
        """
        self.children.append(child_node)

    def __repr__(self):
        """
        String representation of the node.
        """
        return f"Node(value={self.value})"


def generate_n_nodes(level, number_nodes):
    print("level " + str(level) + " - number of nodes: " + str(number_nodes))
    l = []
    for i in range(number_nodes):
        l.append(Node(str(level) + "_" + str(i)))
    return l

def pos_range(total_len_range, len_sub_range):
    return [x for x in range(total_len_range - len_sub_range + 1)]

def add_connection(edges, left, right):
    print("connect " + str(left) + " to " + str(right))
    for l in left:
        for r in right:
            edges.append([l,r])

def assign_range(edges, left_nodes, right_nodes):
    print("left nodes: " + str(left_nodes) + "; right nodes: " + str(right_nodes))
    # only one right node left?
    if len(right_nodes) == 1 or len(left_nodes) == 1:
        add_connection(edges, left_nodes, right_nodes)
        return

    left_node = random.randint(0, len(left_nodes) - 1) # node position in array
    range_size = random.randint(1, len(right_nodes))  # number of connections

    print("left node: " + str(left_node) + "; range size: " + str(range_size))
    # if first left node then range has to start at first right node
    if left_node == 0:
        print("first")
        if range_size >= len(right_nodes):
            add_connection(edges, [left_nodes[left_node]], right_nodes)
            assign_range(edges, left_nodes[1:len(left_nodes)], [right_nodes[len(right_nodes)-1]])
        else:
            first_right_nodes = right_nodes[0:range_size]
            last_right_nodes = right_nodes[range_size:len(right_nodes)]
            add_connection(edges, [left_nodes[left_node]], first_right_nodes)
            assign_range(edges, left_nodes[1:len(left_nodes)], last_right_nodes)
        return

    # if last left node then range has to end at last right node
    if left_node == len(left_nodes) - 1:
        print("last")
        if range_size >= len(right_nodes):
            add_connection(edges, [left_nodes[left_node]], right_nodes)
            assign_range(edges, left_nodes[0:left_node], [right_nodes[0]])
        else:
            first_right_nodes = right_nodes[0:len(right_nodes) - range_size]
            last_right_nodes = right_nodes[len(right_nodes) - range_size:len(right_nodes)]
            add_connection(edges, [left_nodes[left_node]], last_right_nodes)
            assign_range(edges, left_nodes[0:left_node], first_right_nodes)
        return

    # left node in middle
    print("middle")
    pssbl_rng_positions = pos_range(len(right_nodes), range_size)
    range_pos = random.choice(pssbl_rng_positions)
    first_right_nodes = right_nodes[0:range_pos+1]
    middle_right_nodes = right_nodes[range_pos:range_pos + range_size]
    last_right_nodes = right_nodes[range_pos + range_size-1:len(right_nodes)]
    print("f: " + str(first_right_nodes) + "; m: " + str(middle_right_nodes) + "; l: " + str(last_right_nodes))
    add_connection(edges, [left_nodes[left_node]], middle_right_nodes)
    assign_range(edges, left_nodes[0:left_node], first_right_nodes)
    assign_range(edges, left_nodes[left_node+1:len(left_nodes)], last_right_nodes)


# Example usage
if __name__ == "__main__":
    # Init Graph
    root = Node("start")
    end = Node("end")
    edges = []

    # generate nodes for every level
    level_1_nodes = generate_n_nodes(1, random.randint(1, 4))
    level_2_nodes = generate_n_nodes(2, random.randint(1, 4))
    level_3_nodes = generate_n_nodes(3, random.randint(1, 4))

    # connect root and 1
    assign_range(edges,[root], level_1_nodes)
    assign_range(edges, level_1_nodes, level_2_nodes)
    assign_range(edges, level_2_nodes, level_3_nodes)
    assign_range(edges, level_3_nodes, [end])

    G = nx.Graph()


    G.add_node(root.value)
    G.add_nodes_from([x.value for x in level_1_nodes])
    G.add_nodes_from([x.value for x in level_2_nodes])
    G.add_nodes_from([x.value for x in level_3_nodes])
    G.add_edges_from([(x.value, y.value) for (x,y) in edges])

    print(list(G.nodes))
    print(list(G.edges))

    nx.draw(G, with_labels=True, font_weight='bold')
    plt.savefig("graph.png")
