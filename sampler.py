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
while itr < nPts:
    x = np.random.rand(nDim)
    if cnstrnt.apply(x):
        out.write(str(x)+'\n')
        itr+=1

print(f'Done! Closing {outputFile}')
out.close()


