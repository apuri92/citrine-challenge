#!/usr/bin/env python3
from constraints import Constraint
import numpy as np
import sys

inputFile = sys.argv[1]
outputFile = sys.argv[2]
nPts = int(sys.argv[3])
print(f'inputFile:  {inputFile}\noutputFile:    {outputFile}\npointsRequested:  {nPts}')

# Setup output file
out = open(outputFile, "w")

# Setup constraint object
cnstrnt = Constraint(inputFile)
nDim = cnstrnt.get_ndim()
itr = 0
np.random.seed(1234)

# sample from hypercube continuously till required points are obtained
while itr < nPts:
    x = np.random.rand(nDim)*0.2
    if cnstrnt.apply(x):
        out.write(str(x)+'\n')
        print(f'found {itr}')
        itr+=1

print(f'Done! Closing {outputFile}\n')
out.close()


