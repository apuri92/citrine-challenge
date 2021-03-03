#!/usr/bin/env python3
from constraints import Constraint
from collections import deque
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from math import log10
import sys

# Utility to check if point is within the unit hypercube
def UnitCubeCheck(x):
    for _ in x:
        if _ > 1 or _ < 0:
            return False
    return True

# Utility to plot points in 3D
def PlotPoints3D(pointsExplored, dim0=0, dim1=1, dim2=2):
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    xs=[]
    ys=[]
    zs=[]
    for _ in pointsExplored:
        xs.append(_[dim0])
        ys.append(_[dim1])
        zs.append(_[dim2])
    
    ax.scatter3D(xs, ys, zs, c=zs, cmap='hsv')
    plt.xlim([0,1])
    plt.ylim([0,1])
    # plt.show()

# Utility to plot points in 2D
def PlotPoints(pointsExplored, filename, dim0=0, dim1=1):
    xs=[]
    ys=[]
    for _ in pointsExplored:
        xs.append(_[dim0])
        ys.append(_[dim1])

    plt.scatter(xs, ys,marker='o', c='#1f2db4')
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.xlabel(f'x[{dim0}]')
    plt.ylabel(f'x[{dim1}]')
    plt.title(f'Total points used = {len(pointsExplored)}')
    plt.savefig(f'./images/{filename}_len{len(pointsExplored)}')
    plt.show()


# Utility to check if vectors in answerFile satisfy constraints in constraints file
def CheckOutputFile(constraints, answerFile):
    print(f'\nchecking answer in {answerFile}')
    cnstrnts = Constraint(constraints)
    dim = cnstrnts.get_ndim()
    with open(outputFileName) as f:
        for itr, line in enumerate(f):
            x=[float(_) for _ in line.strip().split(" ")]
            # print location in checker
            if log10(itr+1) % 1 == 0:
                print("".join(['.']*2*int(log10(itr+1)))+str(itr+1))
            
            # if any vector fails, return false immediately
            if not cnstrnts.apply(x):
                print(f'failed on {x}')
                return False
    
    # return true if all points succeed
    return True

# GenerateValidPoints uses a form of breadth first search to generate n points satisfying the constraints defined in inputFileName and saves them to outputFileName. 
def GenerateValidPoints(inputFileName='example.txt', outputFileName='exampleOut.txt', n=50):
    # Get the constraints and dimensionality of the probelm from the input file.
    # The startingPoint is cast as a tuple because hashing will be required to put the found points into a set.
    cnstrnts = Constraint(inputFileName)
    dim = cnstrnts.get_ndim()
    startingPoint = tuple(cnstrnts.get_example())
    
    # This will the step size with which the exploration will be done.
    stepSize = 1.0

    # Setup the set to mark points that are explored and a queue to hold the points that need to be explored
    pointsExplored = set()
    pointsQueue = deque()
    
    itr = 0
    # Drawback is that if region is not continuous, point may not be found
    
    # Run while number of points found is less than the number of points requested
    while len(pointsExplored) < nPts:
    
        # Print the step size being used and number of points already found
        print(f'using stepSize {stepSize}, valid points found: {len(pointsExplored)}')
        
        # Search will begin from the given sample point so add it to the queue.
        pointsQueue.append(startingPoint)
        # Break if the step size becomes too small.
        # This will typically happen when points are not being found or the number of points requested is too large
        if stepSize <= 0.00000000001:
            print(f'Step size is too small, exiting with {len(pointsExplored)} points found.')
            return

        # Run while the queue exists and more points are required.
        while pointsQueue and len(pointsExplored) < nPts:
            
            # Get the current point from the queue.
            # A tuple is used so it can be hashed and put into a set.
            currPoint = pointsQueue.popleft()

            # The search always starts from the given sample point.
            # The currPoint != startingPoint condition in the while loop ensures that the search begins.
            # Otherwise it would be skipped since the starting point may already be in the pointsExplored set.
            if currPoint != startingPoint and currPoint in pointsExplored:
                continue
            
            # Explore in positive and negative direction for each dimension in the current point.
            for iDim in range(dim):
                for direction in [-1, +1]:
                    # Cast as list because mutability is required to upudate the coordinates.
                    nextPoint = list(currPoint)
                    nextPoint[iDim]+=(direction*stepSize)
                    
                    # Cast as tuple for hashability.
                    nextPoint = tuple(nextPoint)
                    
                    # Add to queue if it meets requirements.
                    # This is done in a try/except since there may be a divide by zero error when checking constraints on a point.
                    # If there is a divide by zero, the point is not added to the queue and we can continue.
                    try:
                        if nextPoint not in pointsExplored and cnstrnts.apply(nextPoint) and UnitCubeCheck(nextPoint):
                            pointsQueue.append(nextPoint)
                    except:
                        pass
            
            # Once all valid points associated to the current point are added to the queue, the current point is marked as explored.
            pointsExplored.add(currPoint)
            
            # if len(pointsExplored) < 50:
            #     PlotPoints(pointsExplored, inputFileName.split('/')[-1][:-4])

            # if len(pointsExplored) % 100 == 0:
            #     PlotPoints(pointsExplored, inputFileName.split('/')[-1][:-4])
            
            # End of inner while loop.

        # Halve stepSize after all points with current stepSize within constraints are found and being search again.
        stepSize /= 2

        # End of outer while loop.


    # Setup output file and write coordinates to it. File is closed automatically
    with open(outputFileName, "w") as out:
        for _ in pointsExplored:
            out.write(" ".join(map(str, _))+'\n')

    print(f'Found {len(pointsExplored)} valid points for constraints in {inputFileName}. These are saved to {outputFileName}')
    
    
    return 0


if __name__ == '__main__':
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]
    nPts = int(sys.argv[3])
    print(f'inputFileName:  {inputFileName}\noutputFileName:    {outputFileName}\npointsRequested:  {nPts}')
    GenerateValidPoints(inputFileName, outputFileName, nPts)
    
    # Checking the answers in the output file (commented out).
    # if CheckOutputFile(inputFileName, outputFileName):
    #     print('all tests passed')
    # else:
    #     print('check results')    
    


