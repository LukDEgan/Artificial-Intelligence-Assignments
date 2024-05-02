
# first I need to read in the arguments
import sys
import csv
from statistics import median
from math import ceil, floor

train_filename = sys.argv[1]
test_filename = sys.argv[2]
dimensions = int(sys.argv[3])

# I now need to construct a KD tree from the training data (meaning I need to read in the training and testing data)

# Im gonna store everything as a list of lists because im lazy

def read_in(filename: str)->list:...

# then Im going to need to build the tree

def build_tree(points: list):...

# then I want to be able to classify each point

def classify_point(root, point: list)->tuple:...

"""Okay so Now I am going to actually write the functions because I am lazy lol"""

def read_in(filename: str)->list:
    """Takes filename returns a list of lists
    Return:
        List of points ->points are tab separated from the file
    """
    file = list()
    with open(filename, 'r') as f:
        tsv_file = csv.reader(f, delimiter="\t")
        next(tsv_file)
        for row in tsv_file:
            row = row[0].split(' ')
            row = [float(i) for i in row if i != '']
            # row = [float(i) for i in row]
            file.append(row)

    return file

"""Need a node class"""

class Node:
    def __init__(self, point=None, label=None, left=None, right=None):
        self.point = point
        self.label = label
        self.left = left
        self.right = right
    
# def median(l: list)->tuple:
#     # I want to take a list and not only return the median but also the index
#     return None

def euclidean_distance(node_a, node_b)->float:
    dist = 0
    for i in range(0, dimensions):
        dist += ((node_a[i] - node_b.point[i]) ** 2)
    return dist
    

def make_tree(points:list, labels:list, depth=0):
    """Takes in a list of points and their respective labels and returns the root node"""
    if len(points) == 0: # if we don't have any points
        return None

    d = depth % len(points[0]) # modding current depth by M

    # Sort points by the cut (d)
    sorted_points = sorted(zip(points, labels), key=lambda x: x[0][d]) # I want to sort both together
    # because otherwise the order of their labels will not be maintained
    m = len(points) // 2

    # getting all points to the left of the median
    left_node = make_tree([x[0] for x in sorted_points[:m]], [x[1] for x in sorted_points[:m]], depth + 1)
    right_node = make_tree([x[0] for x in sorted_points[m+1:]], [x[1] for x in sorted_points[m+1:]], depth + 1)


    # Create node and construct subtrees
    node = Node(
        point=sorted_points[m][0],
        label=sorted_points[m][1],
        left=left_node,
        right=right_node
    )
    return node

def classify_point(root, point: list, depth=0)->tuple:
    """Here we take a root node (from a KD tree) and a given point (list) and classify it
    based on its 1nn
    i.e. we return its distance to the next value (which we need to check) and that node's's label
    """
    if root is None: return (float('inf'), None)

    d = depth % dimensions

    dist_sq = euclidean_distance(point, root)
    dx = sum(float((point[i] - root.point[i]) ** 2) 
            for i in range(len(point)) )
    dimension_distance = (point[d] - root.point[d]) ** 2 # distance between current node and point along dimension d


    if(root.point[d] < point[d]): # if the current node's val along dimension d is < point we go right
        n_b = root.right 
        o_b = root.left
    else: # if the current node val along dimension d > point we go left
        n_b = root.left 
        o_b = root.right
    
    dist, label = classify_point(n_b, point, depth+1)  # checking out the best branch first
    if dx < dist: # if the current distance is better than the next branch's distance
        dist = dx
        label = root.label
    
    if(dimension_distance < dist):
        d, l = classify_point(o_b, point, depth+1) # checking out the classification on the other branch
        if(d < dist): # if the new distance is better than the last best
            dist = d
            label = l
    
    return (dist, label)

train_file = read_in(train_filename)
train_points = [i[:-1] for i in train_file]
train_labels = [i[-1] for i in train_file]
train_root = make_tree(train_points, train_labels)



test_file = read_in(test_filename)
for i in test_file:

    print(int(classify_point(train_root, i, 0)[1]))