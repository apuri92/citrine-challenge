#!/usr/bin/env python3
from constraints import Constraint
from collections import deque
from math import log10
import sys

# generate_valid_points uses a form of breadth first search to generate n points satisfying the constraints defined in input_file_name and saves them to output_file_name.
def generate_valid_points(input_file_name, output_file_name, n):
    # Get the constraints and dimensionality of the probelm from the input file.
    # The starting_point is cast as a tuple because hashing will be required to put the found points into a set.
    cnstrnts = Constraint(input_file_name)
    dim = cnstrnts.get_ndim()
    starting_point = tuple(cnstrnts.get_example())
    
    # This will the step size with which the exploration starts.
    step_size = 1.0

    # Setup the set to mark points that are explored and a queue to hold the points that need to be explored
    points_explored = set()
    points_queue = deque()
    
    # Run while number of points found is less than the number of points requested
    while len(points_explored) < n_points:
    
        # Print the step size being used and number of points already found
        # print(f'using step_size {step_size}, valid points found: {len(points_explored)}')
        
        # Search will begin from the given sample point so add it to the queue.
        points_queue.append(starting_point)
        # Break if the step size becomes too small.
        # This will typically happen when points are not being found or the number of points requested is too large
        if step_size <= 0.0000000000001:
            # print(f'Step size is too small, exiting with {len(points_explored)} points found.')
            break

        # Run while the queue exists and more points are required.
        while points_queue and len(points_explored) < n_points:
            
            # Get the current point from the queue.
            # A tuple is used so it can be hashed and put into a set.
            current_point = points_queue.popleft()

            # The search always starts from the given starting_point.
            # After the first iteration of the while loop, the starting_point is in the points_explored set.
            # The current_point != starting_point condition is required to ensure that the search begins for every iteration.
            if current_point != starting_point and current_point in points_explored:
                continue
            
            # Explore in positive and negative direction for each dimension in the current point.
            for i_dim in range(dim):
                for direction in [-1, +1]:
                    # Cast as list because mutability is required to upudate the coordinates.
                    next_point = list(current_point)
                    next_point[i_dim]+=(direction*step_size)
                    
                    # Cast as tuple for hashability.
                    next_point = tuple(next_point)
                    
                    # Add point to queue if the constraints defined in the input file are met and point is within the unit hypercube.
                    # This is done in a try/except since there may be a divide by zero error when checking constraints on a point.
                    # If there is a divide by zero, the point is not added to the queue and the script can continue.
                    try:
                        if next_point not in points_explored and cnstrnts.apply(next_point) and unit_cube_check(next_point):
                            points_queue.append(next_point)
                    except:
                        pass
            
            # Once all valid points associated to the current point are added to the queue, the current point is marked as explored.
            points_explored.add(current_point)

            # End of inner while loop.

        # Halve step_size after all points with current step_size within constraints are found and being search again.
        step_size /= 2

        # End of outer while loop.


    # Setup output file and write coordinates to it. File is closed automatically.
    with open(output_file_name, "w") as out:
        for _ in points_explored:
            out.write(" ".join(map(str, _))+'\n')

    # print(f'Found {len(points_explored)} valid points for constraints in {input_file_name}. These are saved to {output_file_name}')
    return 0

# Utility to check if point is within the unit hypercube.
def unit_cube_check(x):
    for _ in x:
        if _ > 1 or _ < 0:
            return False
    return True

# Utility to check if vectors in answer_file satisfy constraints in constraints file.
def check_output_file(constraints_file, answer_file):
    # print(f'\nchecking answer in {answer_file}')
    cnstrnts = Constraint(constraints_file)
    dim = cnstrnts.get_ndim()
    with open(output_file_name) as f:
        for itr, line in enumerate(f):
            x=[float(_) for _ in line.strip().split(" ")]
            # Print how many points have been checked.
            if log10(itr+1) % 1 == 0:
                # print("".join(['.']*2*int(log10(itr+1)))+str(itr+1))
                pass
            
            # If any vector fails, return False immediately.
            if not cnstrnts.apply(x):
                # print(f'failed on {x}')
                return False
    
    # Return true if all points are valid.
    return True



if __name__ == '__main__':
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    n_points = int(sys.argv[3])
    # Print out the input arguments.
    # print(f'input_file_name:  {input_file_name}\noutput_file_name:    {output_file_name}\npointsRequested:  {n_points}')
    
    # Generate n_points that satisfy the constraints in input_file_name and write them to output_file_name.
    generate_valid_points(input_file_name, output_file_name, n_points)
    
    # Checking the answers in the output file.
    # if check_output_file(input_file_name, output_file_name):
    #     print('all tests passed')
    # else:
    #     print('check results')    
    


