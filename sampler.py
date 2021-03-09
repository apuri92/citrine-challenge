#!/usr/bin/env python3
import logging
from sampler_class import *
from checker_class import *

def main():
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    n_points = int(sys.argv[3])
    
    # Create Sampler object for input_file_name, generate required number of points and write them to a file
    sampler = Sampler(input_file_name)
    sampler.generate_valid_points(n_points)
    sampler.write_to_file(output_file_name)

    # Run checker to test input<->output file has expected number of points.
    checker = Checker()
    checker.check_output_file(input_file_name, output_file_name, n_points)

if __name__ == '__main__':
    main()