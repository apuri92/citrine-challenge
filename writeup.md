# Citrine Informatics Technical Challenge
#### *Data and AI Research Engineer*
#### *Version: e6b4a7f0da67f298a09e9550d848bfb86bbc028b*
---

## Problem Outline
Deliver a script that can be run as `./sampler input_file output_file n_results` along with installation instructions. The input file contains the dimensionality of the problem, a single feasible point, and a list of constraints. The output file should contain a list of vectors (space delimited within the vector; one vector per line). 

---

## Solution:
I used the idea of a bread-first search (BFS) to solve this problem. 

### Pseudocode

```
while (number of found points < number of required points)
	add the given feasible point to a queue
	
	while (queue exists) and (number of found points < number of required points)
		currentPoint = popleft from queue
		if currentPoint in exploredPoints and currentPoint != feasiblePoint:
            continue
        for each dimension in current point:
			explore outward with a particular step size
			
            if point is feasible:
                add to queue
		
        add currentPoint to exploredPoints set
	
    halve the step size and repeat search
```

At the end of this loop, the exploredPoints set will contain the required number of valid points.

Since the exploration is done in a consistent manner with a regular step-size, (1.0, 0.5, 0.25, 0.125…), the points found fill the valid space uniformly.

The points collected from mixture.txt are shown below. The order of filling can be seen and it covers the valid space
![mixture.gif](images/mixture.gif)

---

## Benchmark tests:
Timing: Big O analysis
Space: memory footprint

---

## Drawbacks:
requires a feasible point to begin the search
?? Can the size go up exponentially for very high dimensional spaces?