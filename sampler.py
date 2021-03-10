#!/usr/bin/env python3
import sys
from generator import Generator
from validator import Validator

def main():
    # Read arguments from command line
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    n_points = int(sys.argv[3])
    
    # Create Generator object for input_file_name, generate required number of points and write them to a file
    generator = Generator(input_file_name)
    generator.generate_valid_points(n_points)
    generator.write_to_file(output_file_name)

    # Run validator to check there are n_points in the output file that satisfy the constraints in the input file.
    validator = Validator()
    validator.validate_output_file(input_file_name, output_file_name, n_points)

if __name__ == '__main__':
    main()