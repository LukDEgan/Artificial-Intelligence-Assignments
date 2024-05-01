import sys
def closer_distance(pivot, p1, p2):
        if p1 is None:
            return p2

        if p2 is None:
            return p1

        d1 = distance(pivot, p1)
        d2 = distance(pivot, p2)

        if d1 < d2:
            return p1
        else:
            return p2
def distance(point1, point2):
    squared_distance = sum((y-x)**2 for y, x in zip(point2, point1))**0.5
    return squared_distance

class kdTree:
    def __init__(self, Points, Dim = 0):   
        n = len(Points)
        if n <= 0:
            return None   
       
        axis = (Dim+1) % 12
        Points.sort(key = lambda x: x[axis])
        m = n // 2
        self.point = Points[m]
        self.left = self.right = None
        if m > 0:
            self.left = kdTree(Points[:m], Dim)
        if n-(m+1) > 0:
            self.right = kdTree(Points[m+1:], Dim)

def OneNN(root, point, Depth = 0):
        if root is None:
            return None
        axis = Depth % 12
        next_branch = None
        skipped_branch = None
        if point[axis] < root.point[axis]:
            next_branch = root.left
            skipped_branch = root.right
        else:
            next_branch = root.right
            skipped_branch = root.left
        best = closer_distance(point,
                           OneNN(next_branch,
                                                point,
                                                Depth + 1),
                           root.point)

        if distance(point, best) > (point[axis] - root.point[axis])**2:
            best = closer_distance(point,
                               OneNN(skipped_branch,
                                                    point,
                                                    Depth + 1),
                               best)

        return best

def read_points(filename):
    points = []
    with open(filename, 'r') as file:
        next(file)
        for line in file:
            data = line.strip().split()
            point = tuple(map(float, data[:-1]))
            points.append(point)
    return points
def read_tests(filename):
    points = []
    with open(filename, 'r') as file:
        next(file)
        for line in file:
            data = line.strip().split()
            point = tuple(map(float, data))
            points.append(point)
    return points
def label_test_samples(test_samples, trained_tree, training_data, points):
    labeled_samples = []
    for sample in test_samples:
        nearest_neighbor = OneNN(trained_tree, sample)
        nearest_neighbor_index = points.index(nearest_neighbor)
        print(training_data[nearest_neighbor_index])
        quality = training_data[nearest_neighbor_index][-1]
        labeled_samples.append(sample + (quality,))
    return labeled_samples

points = read_points('train')
training_data = read_tests('train')
samples = read_tests('test-sample')
D = int(sys.argv[3])
tree = kdTree(points, D)
labeled_test_samples = label_test_samples(samples, tree, training_data, points)

for i, sample in enumerate(labeled_test_samples):
    print(f"Sample {i+1}: {sample}")
