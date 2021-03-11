from constraints import Constraint
from collections import deque
import sys
from os import path
import logging
from setup_logging import setup_logger
from math import sqrt, floor, log10
from helpers import *


class Generator:
    """
    Generator class to generate output_file with required number of points that satisfy constraints in input_file
    """
    
    def __init__(self, input_file_name):
        """
        Construct a Generator object and set up the log files.

        :param input_file_name: Name of the file to read the constraints from (string)
        """
        # Input file that contains the constraints and a set to hold the required points
        self.input_file_name = input_file_name
        self.point_set = set()

        # Setup class logger
        setup_logger('log_generator.log')
        self.log = logging.getLogger('log_generator.log')
        self.log.info(f'Setting up generator: {self.input_file_name}')

    # Generate_valid_points uses a form of breadth first search to generate n points satisfying the constraints defined in input_file_name.
    def generate_valid_points(self, n_points, min_step_size=1E-30):
        """
        Generate required number of points that satisfy constraints.

        :param1 n_points: Required number of points (int)
        :param2 min_step_size: Optional minimum step size (default = 1E-30) for exploration (float)
        """
        
        self.log.info(f'Constraints: {self.input_file_name}')
        self.log.info(f'Points required: {n_points}, min_step_size: {min_step_size}')
        
        # Set up the constraints object and get the dimensionality and starting point.
        # Exit if the constraints file does not exist.
        try:
            constraints = Constraint(self.input_file_name)
            dim =  constraints.get_ndim()
            starting_point =  constraints.get_example()
        except FileNotFoundError:
            self.log.critical(f'Constraints file {self.input_file_name} not found. Skipping generation...')
            return
        
        # The starting_point is cast as a tuple since immutability is required to put it into the set of valid points.
        self.point_set.add(tuple(starting_point))
        
        # Set up a queue to hold the points that need to be explored.
        points_queue = deque()
        
        # The step size with which the exploration starts.
        step_size = 1.0
        
        # Run while more points are required.
        while len(self.point_set) < n_points:
            
            # Add the current set of valid points to the queue for exploration
            for _ in self.point_set:
                points_queue.append(_)
            
            # Counter to count points found at a given step size.
            n_new_points = 0
                        
            # Run while the queue exists and more points are required.
            while points_queue and len(self.point_set) < n_points:
                
                # The current point is popped from the front of the queue.
                current_point = points_queue.popleft()

                # PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4]+"_eachExploration",f'Points:{len(self.point_set)} Step size: {step_size}')

                # Explore in positive and negative directions for each dimension in the current point.
                for i_dim in range(dim):
                    for direction in [-1, +1]:
                        # Cast as list because mutability is required to update the coordinates.
                        next_point = list(current_point)
                        next_point[i_dim]+=(direction*step_size)
                        # next_point[i_dim]=round(next_point[i_dim]+(direction*step_size), len(str(step_size)[2:]))

                        # fix floaring poitn err
                        # Cast as tuple for hashability.
                        next_point = tuple(next_point)
                        try:
                            # If next_point is within the unit hypercube, meets constraints, and is not already explored, add it to the queue for exploration and to the set of valid points.
                            if self.unit_cube_check(next_point) and constraints.apply(next_point) and next_point not in self.point_set:
                                points_queue.append(next_point)

                                # itr = len(self.point_set)
                                # if itr !=0 and (itr % pow(10, floor(log10(itr+1))) == 0):
                                #     PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4]+"_logarithmicNPoints",f'Points:{len(self.point_set)} Step size: {step_size}')

                                self.point_set.add(next_point)
                                # PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4]+"_eachStepSize",f'Points:{len(self.point_set)} Step size: {step_size}')
                                n_new_points+=1


                        # ZeroDivisionError exception is logged as a warning and the script continues.
                        except ZeroDivisionError:
                            self.log.warning(f'{sys.exc_info()[1]}, point: {next_point}')

                        # Unexpected exceptions are logged as errors and the script continues
                        except:
                            self.log.error(f'{sys.exc_info()}, point: {next_point}')
                        
                        # Break if the number of required points are found in the inner loop
                        
                        print(len(self.point_set))
                        if len(self.point_set) == n_points:
                            print(f'ending in for - {len(self.point_set)}')
                            break
            
                    if len(self.point_set) == n_points:
                        print(f'ending in for - {len(self.point_set)}')
                        break
                    
                    # End outer for loop: Done with exploration for current point
                # End inner while loop: Done with exploration at given step size
                # PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4]+"_eachExploration",f'Points:{len(self.point_set)} Step size: {step_size}')
                # print(f'set: {self.point_set}, len: {len(self.point_set)}, step: {step_size}')

            # Log how many new points found with current step size
            self.log.debug(f'Found: {n_new_points} with step size: {step_size}, total in set: {len(self.point_set)}')

            # PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4]+"_eachStepSize",f'Points:{len(self.point_set)} Step size: {step_size}')

            # Halve step_size after finding all valid points with current step_size.
            # Break if the step size becomes smaller than the min_step_size.           
            step_size /= 2
            if step_size < min_step_size:
                self.log.warning(f'Step size is too small: {step_size}, breaking search')            
                break

            # End outer while loop: Done with finding required number of points

        # Log the total number of points found
        self.log.info(f'Total number of points found: {len(self.point_set)}')
        self.log.info(f'-- Generation complete -- ')
        # End generate_valid_points
        return


    def write_to_file(self, output_file_name):
        """
        Setup output file and write coordinates to it.

        :param output_file_name: Name of the file to write the generated points to (string)
        """

        # If generate_valid_points failed because the constraint file was not found, point_set is empty so there is nothing to write.
        if len(self.point_set) == 0:
            self.log.error(f'No points generated for {self.input_file_name}. Skip writing to {output_file_name}...')
            return
        
        # If the file already exist, warn that it will be overwritten
        if path.exists(output_file_name):
            self.log.warning(f'{output_file_name} already exists, overwriting file')
        
        self.log.info(f'Writing: {self.input_file_name} -> {output_file_name}')
        
        # Open file for writing and write set of points to it
        with open(output_file_name, "w") as out:
            # Use itr to remove the new line character for the last line
            itr = 0
            new_line = '\n'
            for _ in self.point_set:
                itr+=1
                if itr == len(self.point_set): new_line=''
                out.write(" ".join(map(str, _))+new_line)

        self.log.info(f'Written {itr} lines.')
        self.log.info(f'-- Writing complete -- ')
        return


    def unit_cube_check(self, x):
        """
        Check if the given vector is within the unit hypercube.

        :param x: Object that is used to represent the vector (tuple)
        """
        for _ in x:
            if _ > 1 or _ < 0:
                return False
        return True
        