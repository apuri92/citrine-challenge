from constraints import Constraint
from math import log10, floor
from os import path
import logging
from setup_logging import setup_logger

class Validator:
    """
    Validator class to check output file against constraints in input file
    """
    def __init__(self):
        """
        Construct a Validator object and set up the log files
        """

        setup_logger('log_validator.log', level=logging.INFO)
        self.log = logging.getLogger('log_validator.log')

    def validate_output_file(self, constraints_file_name, points_file_name, expected):
        """
        Validates output file against constraint file to see if required number of points available.

        :param constraints_file_name: path to a file that contains the constraints (string)
        :param points_file_name: path to a file that contains the vectors to be validated (string)
        :param expected: Number of points that are expected in this file (string)
        """
        self.log.info(f'Running validation: {constraints_file_name} <-> {points_file_name}')
        try:
            constraints = Constraint(constraints_file_name)
        except FileNotFoundError:
            self.log.critical(f'Constraints file {constraints_file_name} not found. Skipping validation...')
            return

        try:
            points_file = open(points_file_name, 'r')
        except FileNotFoundError:
            self.log.critical(f'Points file {points_file_name} not found. Skipping validation...')
            return
        else:
            failed = 0
            passed = 0
            generated = 0
            for itr, line in enumerate(points_file):
                x=[float(_) for _ in line.strip().split(" ")]
                
                # Log how many points have been checked.
                if itr !=0 and (itr % pow(10, floor(log10(itr+1))) == 0):
                    self.log.debug(f'Checked {itr}')
                
                # Count number of points in file
                generated+=1
                
                # Count the number of passed/failed.
                # Log a warning for a point outside the constraints, log any exceptions as errors
                try:
                    if constraints.apply(x):
                        passed+=1
                    else:
                        self.log.warning(f'Point outside constraints: {x}')
                        failed+=1
                except:
                    self.log.error(f'{sys.exc_info()[1]}, point: {x}')
            points_file.close()
                    
            # Points file summary
            self.log.info(f'{generated} generated, {expected} expected')
            self.log.info(f'{passed} passed, {failed} failed')
            
            # Log final result for points file
            if generated != expected:
                self.log.warning(f'Unexpected number of points')
            if failed > 0:
                self.log.warning(f'{failed} points failed')
            if passed == expected or passed == generated:
                self.log.info(f'All points are valid')
            self.log.info(f'-- Validation complete -- ')
            
        return
