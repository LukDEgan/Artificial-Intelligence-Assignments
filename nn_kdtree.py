import sys

def read_data(filename):
    points = []
    with open(filename, 'r') as file:
        next(file)
        for line in file:
            data = line.strip().split()
            point = tuple(map(float, data))
            points.append(point)
    return points


Depth = int(sys.argv[3])
points = read_data(sys.argv[1])
training_data = [i[:-1] for i in points]
labels = [i[-1] for i in points]
test_samples = read_data(sys.argv[2])

def closer_distance(pivot, p1, p2):
        if p1 is None:
            return p2

        if p2 is None:
            return p1

        d1 = squared_distance(pivot, p1)
        d2 = squared_distance(pivot, p2)

        if d1 < d2:
            return p1
        else:
            return p2
        
def squared_distance(point1, point2):
    squared_distance = sum((x1-x2)**2 for x1, x2 in zip(point1, point2))
    return squared_distance


class Node:
    def __init__(self, point=None):
        self.point = point
        self.left = None
        self.right = None

def BuildKdTree(Points, Depth):
    if not Points:
        return None
    elif len(Points) == 1:
        node = Node(Points[0])
        return node
    else:
        dim = len(Points[0])
        axis = Depth % dim

        sorted_points = sorted(Points, key=lambda point: point[axis])
        m = len(Points)//2
        node = Node(sorted_points[m])
        node.left = BuildKdTree(sorted_points[:m], Depth + 1)
        node.right = BuildKdTree(sorted_points[m+1:], Depth + 1)
        return node

def OneNN(root, point, Depth):
        if root is None:
            return None
        axis = (Depth) % 11
        next_branch = None
        skipped_branch = None
        if point[axis] < root.point[axis]:
            next_branch = root.left
            skipped_branch = root.right
        else:
            next_branch = root.right
            skipped_branch = root.left
        best = closer_distance(point, OneNN(next_branch, point, Depth + 1), root.point)

        if squared_distance(point, best) > (point[axis] - root.point[axis])**2: 
            best = closer_distance(point, OneNN(skipped_branch, point, Depth + 1), best)

        return best


tree = BuildKdTree(training_data, Depth)
for sample in test_samples:
    nearest_neighbor = OneNN(tree, sample, 0)
    nearest_neighbor_index = training_data.index(nearest_neighbor)
    print(nearest_neighbor)
    print(nearest_neighbor_index)
    print(points[nearest_neighbor_index])
    print("\n")
