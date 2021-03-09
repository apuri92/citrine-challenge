#!/usr/bin/env python3
import sys
from sampler_class import Sampler


if __name__ == '__main__':
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    n_points = int(sys.argv[3])
    
    
    # Create Sampler object for input_file_name
    sampler = Sampler(input_file_name)
    
    # Generate required number of points fulfilling constraints and write them to file
    sampler.generate_valid_points(n_points)
    sampler.write_to_file(output_file_name)

    # Run checker to test output files

    # # Checking the answers in the output file and writing to test/logfile.
    # if check_output_file(input_file_name, output_file_name):
    #     print('all tests passed')
    # else:
    #     print('check results')    
    


