from constraints import Constraint
from collections import deque
import sys
from os import path
import logging
from setup_logging import setup_logger
from math import sqrt
from helpers import *

setup_logger('log_generator.log')
log_generator = logging.getLogger('log_generator.log')

class Generator:
    """
    Generator class to generate output_file with required number of points that satisfy constraints in input_file
    """
    
    # Initialize with input_file_name that is used to set up the constraints.
    def __init__(self, input_file_name):
        
        # Input file that contains the constraints
        self.input_file_name = input_file_name
        
        # Define set to hold the set of required points
        self.point_set = set()

        log_generator.info(f'Setting up generator: {self.input_file_name}')

    # Generate_valid_points uses a form of breadth first search to generate n points satisfying the constraints defined in input_file_name.
    def generate_valid_points(self, n_points, min_step_size=1E-30):
        log_generator.info(f'Constraints: {self.input_file_name}')
        log_generator.info(f'Points required: {n_points}, min_step_size: {min_step_size}')
        
        # Set up the constraints object and get the dimensionality and starting point.
        constraints = Constraint(self.input_file_name)
        dim =  constraints.get_ndim()
        starting_point =  constraints.get_example()
        
        # The starting_point is cast as a tuple since immutability is required to put it into the set of valid points .
        self.point_set.add(tuple(starting_point))
        
        # This is the step size with which the exploration starts.
        step_size = 1.0

        # Setup a queue to hold the points that need to be explored
        points_queue = deque()
        
        # Run while number of points found is less than the number of points requested
        while len(self.point_set) < n_points:

            # Break if the step size becomes smaller than the min_step_size.
            # This will typically happen when the valid points are too close to the sample point or the number of points requested is too large.
            if step_size < min_step_size:
                log_generator.warning(f'Step size is too small: {step_size}, breaking search')            
                break
            
            # Add the current set of found points to the queue of points that will be explored
            for _ in self.point_set:
                points_queue.append(_)
            
            
            # Counter to count points found for a given step size.
            n_new_points = 0
            
            # Run while the queue exists and more points are required.
            while points_queue and len(self.point_set) < n_points:
                # The current point is the front of the queue.
                current_point = points_queue.popleft()
                
                # Explore in positive and negative directions for each dimension in the current point.
                for i_dim in range(dim):
                    for direction in [-1, +1]:
                        # Cast as list because mutability is required to update the coordinates.
                        next_point = list(current_point)
                        next_point[i_dim]+=(direction*step_size)
                        
                        # Cast as tuple for hashability.
                        next_point = tuple(next_point)
                        
                        # If next_point is within the unit hypercube, meets constraints, and is not already explored, add it to the queue.
                        # If there is a ZeroDivisionError exception, a warning is logged.
                        # Unexpected exceptions are logged as errors byt the script continues
                        try:
                            if self.unit_cube_check(next_point) and constraints.apply(next_point) and next_point not in self.point_set:
                                points_queue.append(next_point)
                        except ZeroDivisionError:
                            log_generator.warning(f'{sys.exc_info()[1]}, point: {next_point}')
                        except:
                            log_generator.error(f'{sys.exc_info()[1]}, point: {next_point}')

                # Once all valid points associated to the current point are added to the queue, the current point added to set of found points.
                if current_point not in self.point_set:
                    self.point_set.add(current_point)
                    n_new_points+=1
                    if len(self.point_set) % 50 == 0 or len(self.point_set) <= 50:
                        PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4],f'Points:{len(self.point_set)} Step size: {step_size}')

                # End of inner while loop.

            # Halve step_size after finding all valid points with current step_size.
            step_size /= 2
            PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4],f'Points:{len(self.point_set)} Step size: {step_size}')
            
            # Log how many new points found with current step size
            log_generator.debug(f'found: {n_new_points} with step size: {step_size}')

            # End of outer while loop.

        # Log the total number of points found
        log_generator.info(f'Total number of points found: {len(self.point_set)}')


    # Setup output file and write coordinates to it. File is closed automatically.
    def write_to_file(self, output_file_name):
        # If file already exist, log that it will be overwritten
        if path.exists(output_file_name):
            log_generator.warning(f'{output_file_name} already exists, overwriting file')
        
        # Open file for writing and write set of points to it
        with open(output_file_name, "w") as out:
            
            # Use itr to remove the new line character for the last line
            itr = 0
            new_line = '\n'
            for _ in self.point_set:
                itr+=1
                if itr == len(self.point_set): new_line=''
                out.write(" ".join(map(str, _))+new_line)

        log_generator.info(f'Writing output: {self.input_file_name} -> {output_file_name}')


    # Utility to check if point is within the unit hypercube.
    def unit_cube_check(self, x):
        for _ in x:
            if _ > 1 or _ < 0:
                return False
        return True
        