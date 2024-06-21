import numpy as np
import sys
#Step one, read in the input
def read_input(file_path):
    with open(file_path, 'r') as file:
        #store file lines in list
        lines = file.readlines()
    #map size is first line
    map_size = tuple(map(int, lines[0].strip().split()))
    #next lines are the map, map has rows given from previous line
    map_data = [lines[i].strip().split() for i in range(1,map_size[0]+1)]
    #next line is number of observations
    num_observations = int(lines[map_size[0] + 1].strip())
    #next lines are observations
    observations = [lines[i + map_size[0] + 2].strip() for i in range(num_observations)]
    #sensor error
    sensor_error_rate = float(lines[map_size[0] + num_observations + 2].strip())
    
    return map_size, map_data, num_observations, observations, sensor_error_rate

def get_traversable_positions(map_data):
    traversable_points = []
    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j] == '0':
                traversable_points.append((i, j))
    return traversable_points

def get_adjacent_positions(position, map_data):
    rows, cols = len(map_data), len(map_data[0])
    x, y = position
    adjacent_positions = []
    
    if x > 0 and map_data[x - 1][y] == '0':  # Up
        adjacent_positions.append((x - 1, y))
    if x < rows - 1 and map_data[x + 1][y] == '0':  # Down
        adjacent_positions.append((x + 1, y))
    if y > 0 and map_data[x][y - 1] == '0':  # Left
        adjacent_positions.append((x, y - 1))
    if y < cols - 1 and map_data[x][y + 1] == '0':  # Right
        adjacent_positions.append((x, y + 1))
    
    return adjacent_positions

def build_transition_matrix(traversable_points, map_data):
    K = len(traversable_points)
    Tm = np.zeros((K, K))
    pos_to_index = {pos: idx for idx, pos in enumerate(traversable_points)}

    for idx, pos in enumerate(traversable_points):
        adj_positions = get_adjacent_positions(pos, map_data)
        N = len(adj_positions)
        if N > 0:
            prob = 1.0 / N
            for adj in adj_positions:
                adj_idx = pos_to_index.get(adj)
                if adj_idx is not None: 
                    Tm[idx, adj_idx] = prob

    return Tm

def get_obstacle_reading(position, map_data):
    rows, cols = len(map_data), len(map_data[0])
    x, y = position
    reading = []
    
    # Up
    if x == 0 or map_data[x - 1][y] == 'X':
        reading.append('1')
    else:
        reading.append('0')

    # Down
    if x == rows - 1 or map_data[x + 1][y] == 'X':
        reading.append('1')
    else:
        reading.append('0')    
    # Left
    if y == 0 or map_data[x][y - 1] == 'X':
        reading.append('1')
    else:
        reading.append('0')
    # Right
    if y == cols - 1 or map_data[x][y + 1] == 'X':
        reading.append('1')
    else:
        reading.append('0')
    

    
    return ''.join(reading)

def build_emission_matrix(traversable_points, map_data, observations, error_rate):
    K = len(traversable_points)
    N = len(observations)
    Em = np.zeros((K, N))

    for idx, pos in enumerate(traversable_points):
        true_reading = get_obstacle_reading(pos, map_data)
        for obs_idx, observed_reading in enumerate(observations):
            diff = sum(tr != or_ for tr, or_ in zip(true_reading, observed_reading))
            prob = (1 - error_rate) ** (4 - diff) * error_rate ** diff
            Em[idx, obs_idx] = prob

    return Em


def viterbi(traversable_points, Tm, Em, observations):
    K = len(traversable_points)
    T = len(observations)
    trellis = np.zeros([K, T])

    initial_prob = 1.0 / K
    for i in range(K):
        trellis[i, 0] = initial_prob * Em[i, 0]
        print( trellis[i, 0])

    for j in range(1, T):
        for i in range(K):
            max_prob = 0
            for k in range(K):
                prob = trellis[k, j - 1] * Tm[k, i] * Em[i, j]
                if prob > max_prob:
                    max_prob = prob
            trellis[i, j] = max_prob

    return trellis

def save_output(trellis, traversable_points, map_size):
    rows, cols = map_size
    output_maps = []

    for t in range(trellis.shape[1]):
        map_representation = np.zeros((rows, cols))
        for idx, pos in enumerate(traversable_points):
            map_representation[pos] = trellis[idx, t]
        output_maps.append(map_representation)

    np.savez("output.npz", *output_maps)



def main(file_path):
    map_size, map_data, num_observations, observations, sensor_error_rate = read_input(file_path)
    traversable_points = get_traversable_positions(map_data)
    Tm = build_transition_matrix(traversable_points, map_data)
    Em = build_emission_matrix(traversable_points, map_data, observations, sensor_error_rate)
    trellis = viterbi(traversable_points, Tm, Em, observations)
    save_output(trellis, traversable_points, map_size)

input_file_path = sys.argv[1]
main(input_file_path)