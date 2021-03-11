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

        :param string input_file_name: Name of the constraints file
        """

        # Setup class logger
        setup_logger('log_generator.log')
        self.log = logging.getLogger('log_generator.log')

        # Set up the constraints
        self.input_file_name = input_file_name
        try:
            self.constraints = Constraint(self.input_file_name)
        except FileNotFoundError:
            self.log.critical(f'Constraints file {self.input_file_name} not found.')

        # Set and queue to hold and explore the required points
        self.point_set = set()
        self.points_queue = deque()

        self.log.info(f'Setup Generator for {self.input_file_name}')

    # Generate_valid_points uses a form of breadth first search to generate n points satisfying the constraints defined in input_file_name.
    def generate_valid_points(self, n_points, min_step_size=1E-30):
        """
        Generate required number of points that satisfy constraints.

        :param int n_points: Required number of points
        :param float min_step_size: Optional minimum step size (default = 1E-30) for exploration
        """
        
        # Return if constraints do not exist
        try:
            constraints
        except NameError:
            self.log.critical(f'Constraints file {self.input_file_name} not found. Skipping generation...')
            return

        self.log.info(f'Points required: {n_points}, min_step_size: {min_step_size}')
        self.log.info(f'Constraints: {self.input_file_name}')
        
        # Cast as a tuple since immutability is required to put into a set.
        self.point_set.add(tuple(constraints.get_example()))
        
        # Initial step size for exploration.
        step_size = 1.0
        
        # Run while more points are required.
        while len(self.point_set) < n_points:
            
            # Add all valid points to the queue for exploration
            for _ in self.point_set:
                self.points_queue.append(_)
            
            # Counter to count points found at a given step size.
            n_new_points = 0
                        
            # Run while the queue exists and more points are required.
            while self.points_queue and len(self.point_set) < n_points:
                
                # Explore outward from each point in the queue and add the found valid points to the queue and set.
                current_point = self.points_queue.popleft()
                n_new_points += self.explore_point(current_point, step_size, n_points, constraints)

                # PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4]+"_eachExploration",f'Points:{len(self.point_set)} Step size: {step_size}')
                # End inner while loop
                
            # PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4]+"_eachStepSize",f'Points:{len(self.point_set)} Step size: {step_size}')

            self.log.debug(f'Found: {n_new_points} with step size: {step_size}, total in set: {len(self.point_set)}')

            # Decrease step_size and search again from points already found.
            # Break if the step size becomes smaller than the min_step_size.
            step_size /= 2
            if step_size < min_step_size:
                self.log.warning(f'Step size is too small: {step_size}, breaking search')            
                break

            # End outer while loop: Done with finding required number of points

        self.log.info(f'Total number of points found: {len(self.point_set)}')
        self.log.info(f'-- Generation complete -- ')
        return


    def explore_point(self, current_point, step_size, n_points, constraints):
        """
        Explore outward from the current point in all dimensions with a given step size.
        Points that satisfy constraints are added to the queue and the point_set.
        The function returns the number of valid points found from current point.

        :param tuple current_point: Starting point of exploration
        :param float step_size: extent of exploration
        :param int n_points: required number of points
        :param Constraint constraints: set of constraints to satisfy
        """
        found_points = 0
        for i_dim in range(len(current_point)):
            for direction in [-1, +1]:
                # Update the coordinates, use round() to remove floating point errors, and cast as tuple for hash-abilty.
                next_point = list(current_point)
                round_to_digit = max(self.n_digits_after_decimal(next_point[i_dim]), self.n_digits_after_decimal(step_size))
                next_point[i_dim]=round(next_point[i_dim] + (direction*step_size), round_to_digit)
                next_point = tuple(next_point)

                try:
                    # If next_point is within the unit hypercube, meets constraints, and is not already explored, add to queue and set.
                    if self.unit_cube_check(next_point) and constraints.apply(next_point) and next_point not in self.point_set:
                        self.points_queue.append(next_point)
                        self.point_set.add(next_point)
                        self.point_list.append(next_point)
                        found_points+=1

                        # itr = len(self.point_set)
                        # if itr !=0 and (itr % pow(10, floor(log10(itr+1))) == 0):
                        #     PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4]+"_logarithmicNPoints",f'Points:{len(self.point_set)} Step size: {step_size}')
                        # PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4]+"_eachStepSize",f'Points:{len(self.point_set)} Step size: {step_size}')

                # ZeroDivisionError exception is logged as a warning and the script continues.
                except ZeroDivisionError:
                    self.log.warning(f'{sys.exc_info()[1]}, point: {next_point}')

                # Unexpected exceptions are logged as errors and the script continues
                except:
                    self.log.error(f'{sys.exc_info()}, point: {next_point}')
                
                # Return if the number of required points are found
                if len(self.point_set) == n_points:
                    return found_points
        
        return found_points


    def write_to_file(self, output_file_name):
        """
        Setup output file and write coordinates to it.

        :param string output_file_name: Name of the file to write the generated points
        """

        # If constraint file was not found, point_set is empty so there is nothing to write.
        if len(self.point_set) == 0:
            self.log.error(f'No points generated for {self.input_file_name}. Skip writing to {output_file_name}...')
            return
        
        self.log.info(f'Writing: {self.input_file_name} -> {output_file_name}')
        
        # Warn if file already exists.
        if path.exists(output_file_name):
            self.log.warning(f'{output_file_name} already exists, overwriting file')
        
        
        # Open file for writing and write set of points to it.
        # Use an iterator to remove the new line character from the last line
        with open(output_file_name, "w") as output_file:
            itr = 0
            new_line = '\n'
            for _ in self.point_set:
                itr+=1
                if itr == len(self.point_set): new_line=''
                output_file.write(" ".join(map(str, point))+new_line)

        self.log.info(f'Written {itr} lines.')
        self.log.info(f'-- Writing complete -- ')
        return


    def unit_cube_check(self, x):
        """
        Check if the given vector is within the unit hypercube.

        :param tuple x: Object that is used to represent the vector
        """
        for _ in x:
            if _ > 1 or _ < 0:
                return False
        return True


    def n_digits_after_decimal(self, x):
        """
        Return the number of digits after the decimal in x.
        :param float x: input number x
        """
        return len( str(x).split(".")[-1] )