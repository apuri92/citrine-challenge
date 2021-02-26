from constraints import Constraint
from collections import deque
import matplotlib.pyplot as plt

def unitCubeCheck(x):
    for _ in x:
        if _ > 1 or _ < 0:
            return False
    return True

cnstrnts = Constraint('mixture.txt')
dim = cnstrnts.get_ndim()
start = cnstrnts.get_example()
step = 0.1

exploredPoints = set()
qPoints = deque()

qPoints.append(start)
while qPoints:
    # print(qPoints)
    currPoint = qPoints.pop()
    # print(f'curr point = {currPoint}')
    if tuple(currPoint) in exploredPoints:
        continue
    else:
        for iDim in range(dim):
            p_neg = list(currPoint)
            p_pos = list(currPoint)
            
            p_pos[iDim]=round(p_pos[iDim]+step,1)
            p_neg[iDim]=round(p_neg[iDim]-step,1)
            # print(f'pos{p_pos}  neg:{p_neg}')
            if tuple(p_pos) not in exploredPoints and cnstrnts.apply(p_pos) and unitCubeCheck(p_pos):
                # print(f'adding pos')
                qPoints.append(p_pos)
            if tuple(p_neg) not in exploredPoints and cnstrnts.apply(p_neg) and unitCubeCheck(p_neg):
                # print(f'adding neg')
                qPoints.append(p_neg)
            
        exploredPoints.add(tuple(currPoint))


    itr+=1

# print(f'explorred={exploredPoints}')

xs=[]
ys=[]
for _ in exploredPoints:
    xs.append(_[0])
    ys.append(_[1])
# print(f'xs: {xs}')
# print(f'ys: {ys}')

plt.scatter(xs, ys)
plt.show()
