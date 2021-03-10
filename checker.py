from constraints import Constraint
from math import log10, floor
import logging
from setup_logging import setup_logger

setup_logger('log_checker.log', level=logging.INFO)
log_checker = logging.getLogger('log_checker.log')

class Checker:
    """
    Checker class to check output file against constraints in input file
    """

    # checks output file against constraint file to see if required number of points available
    def check_output_file(self, constraints_file, points_file, expected):
        log_checker.info(f'running check: {constraints_file} <-> {points_file}')
        constraints = Constraint(constraints_file)

        with open(points_file) as f:
            failed = 0
            passed = 0
            generated = 0
            for itr, line in enumerate(f):
                x=[float(_) for _ in line.strip().split(" ")]
                
                # Log how many points have been checked.
                if itr !=0 and (itr % pow(10, floor(log10(itr+1))) == 0):
                    log_checker.debug(f'Checked {itr}')
                
                # Count number of points in file
                generated+=1
                
                # Count the number of passed/failed
                try:
                    if constraints.apply(x):
                        passed+=1
                    else:
                        log_checker.warning(f'outside constraints: {x}')
                        failed+=1
                except:
                    log_checker.error(f'error for point: {x}, {sys.exc_info()[1]}')
                    pass
                
            # Log warning if number of points is less than expected
            if generated < expected:
                log_checker.warning(f'{generated} points less than expected {expected}')
            
            # Log summary for file
            log_checker.info(f'{passed} passed, {failed} failed')
            log_checker.info(f'{generated} generated, {expected} expected\n')

