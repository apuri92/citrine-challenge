from constraints import Constraint
from collections import deque
import sys, logging
from setup_logging import setup_logger

setup_logger('log_sampler.log')
log_sampler = logging.getLogger('log_sampler.log')

class Sampler:
    """
    SamplerClass to generate output_file with required number of points that satisfy constraints in input_file
    """
    
    # Initialize with input_file_name that is used to set up the constraints.
    def __init__(self, input_file_name):
        
        # Input file that contains the constraints
        self.input_file_name = input_file_name
        
        # Define set to hold the set of required points
        self.point_set = set()

        log_sampler.info(f'Setting up sampler: {self.input_file_name}')

    # Generate_valid_points uses a form of breadth first search to generate n points satisfying the constraints defined in input_file_name.
    def generate_valid_points(self, n_points, min_step_size=0.0000000000001):
        log_sampler.info(f'Constraints: {self.input_file_name}')
        log_sampler.info(f'Points required: {n_points}, min_step_size: {min_step_size}')
        
        # Get dimensionality and starting point of the problem from the input file.
        # The starting_point is cast as a tuple because hashing will be required to put the found points into a set.
        constraints = Constraint(self.input_file_name)
        dim =  constraints.get_ndim()
        starting_point =  tuple(constraints.get_example())

        # This will the step size with which the exploration starts.
        step_size = 1.0

        # Setup the set to mark points that are explored and a queue to hold the points that need to be explored
        points_queue = deque()
        
        # Run while number of points found is less than the number of points requested
        while len(self.point_set) < n_points:

            log_sampler.debug(f'step_size: {step_size}, valid points found: {len(self.point_set)}')
           
            # Search will begin from the given sample point so add it to the queue.
            points_queue.append(starting_point)
            
            # Break if the step size becomes smaller than the min_step_size.
            # This will typically happen when the valid points are too close to the sample point or the number of points requested is too large.
            if step_size < min_step_size:
                log_sampler.warning(f'Step size: {step_size}, breaking search for more points')            
                break

            # Run while the queue exists and more points are required.
            while points_queue and len(self.point_set) < n_points:
                
                # Get the current point from the queue.
                # A tuple is used so it can be hashed and put into a set.
                current_point = points_queue.popleft()

                # The search always starts from the given starting_point.
                # After the first iteration of the while loop, the starting_point is in the self.point_set set.
                # The current_point != starting_point condition is required to ensure that the search begins for every iteration.
                if current_point != starting_point and current_point in self.point_set:
                    continue
                
                # Explore in positive and negative direction for each dimension in the current point.
                for i_dim in range(dim):
                    for direction in [-1, +1]:
                        # Cast as list because mutability is required to upudate the coordinates.
                        next_point = list(current_point)
                        next_point[i_dim]+=(direction*step_size)
                        
                        # Cast as tuple for hashability.
                        next_point = tuple(next_point)
                        
                        # Add point to queue if the point is within the unit hypercube and constraints met.
                        # If there is a ZeroDivisionError exception, a warning is logged.
                        # Other exceptions are unexpected and are logged as errors.
                        try:
                            if self.unit_cube_check(next_point) and constraints.apply(next_point) and next_point not in self.point_set:
                                points_queue.append(next_point)
                        except ZeroDivisionError:
                            log_sampler.warning(f'{sys.exc_info()[1]} for {next_point}')
                        except:
                            log_sampler.error(f'{sys.exc_info()[1]} for {next_point}')
                
                # Once all valid points associated to the current point are added to the queue, the current point is marked as explored.
                self.point_set.add(current_point)

                # End of inner while loop.

            # Halve step_size after all points with current step_size within constraints are found and begin search again.
            step_size /= 2

            # End of outer while loop.

        # log the total number of points found
        log_sampler.info(f'Points found: {len(self.point_set)}')



    # Setup output file and write coordinates to it. File is closed automatically.
    def write_to_file(self, output_file_name):
        with open(output_file_name, "w") as out:
            for _ in self.point_set:
                out.write(" ".join(map(str, _))+'\n')

        log_sampler.info(f'Writing output: {self.input_file_name} -> {output_file_name}')


    # Utility to check if point is within the unit hypercube.
    def unit_cube_check(self, x):
        for _ in x:
            if _ > 1 or _ < 0:
                return False
        return True
        