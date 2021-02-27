#!/usr/bin/env python3
from constraints import Constraint
from collections import deque
import matplotlib.pyplot as plt
import sys

def unitCubeCheck(x):
    for _ in x:
        if _ > 1 or _ < 0:
            return False
    return True

inputFile = sys.argv[1]
outputFile = sys.argv[2]
nPts = int(sys.argv[3])
print(f'inputFile:  {inputFile}\noutputFile:    {outputFile}\npointsRequested:  {nPts}')

cnstrnts = Constraint(inputFile)
dim = cnstrnts.get_ndim()
start = cnstrnts.get_example()
step = 1

exploredPoints = set()
qPoints = deque()
itr = 0
while len(exploredPoints) < nPts:
    qPoints.append(start)
    print(f'using stepsize {step}, starting with qlen {len(qPoints)}: {qPoints}, points collected = {len(exploredPoints)}')
    
    # safety condition if points are not found for whatever reason
    if step <= 0.000000001:
        break

    while qPoints and len(exploredPoints) < nPts:
        # print(qPoints)
        # print(len(exploredPoints))
        currPoint = qPoints.pop()
        # print(f'curr point = {currPoint}')
        # current point is added to the queue, always start from there
        if tuple(currPoint) in exploredPoints and tuple(currPoint) != tuple(start):
            continue
        
        for iDim in range(dim):
            p_neg = list(currPoint)
            p_pos = list(currPoint)
            
            p_pos[iDim]=p_pos[iDim]+step
            p_neg[iDim]=p_neg[iDim]-step

            # todo: catch 1/0 check in apply method
            # print(f'pos{p_pos}  neg:{p_neg}')
            if tuple(p_pos) not in exploredPoints and cnstrnts.apply(p_pos) and unitCubeCheck(p_pos):
                # print(f'adding pos')
                qPoints.append(p_pos)
            if tuple(p_neg) not in exploredPoints and cnstrnts.apply(p_neg) and unitCubeCheck(p_neg):
                # print(f'adding neg')
                qPoints.append(p_neg)
                
        exploredPoints.add(tuple(currPoint))

            # if len(exploredPoints) == nPts:
            #     break

    step /= 2
    itr+=1

# Setup output file
out = open(outputFile, "w")

print(f'len explorred={len(exploredPoints)}')
for _ in exploredPoints:
    # out.write(str(list(_))+'\n')
    out.write(" ".join(map(str, _))+'\n')


print(f'Done! Closing {outputFile}\n')
out.close()


xs=[]
ys=[]
for _ in exploredPoints:
    xs.append(_[0])
    ys.append(_[1])

plt.scatter(xs, ys)
plt.xlim([0,1])
plt.ylim([0,1])
plt.show()