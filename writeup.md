# Citrine Informatics Technical Challenge
#### *Data and AI Research Engineer*
#### *Version: e6b4a7f0da67f298a09e9550d848bfb86bbc028b*
---

## Problem Outline
Deliver a script that can be run as `./sampler input_file output_file n_results` along with installation instructions. The input file contains the dimensionality of the problem, a single feasible point, and a list of constraints. The output file should contain a list of vectors (space delimited within the vector; one vector per line). 

---

## Solution:
### Instructions
The script can be run as below:

```./sampler.py input_file output_file 1000```

It will take in an input_file with the dimensionality, the single feasible point, and the constraints, and write 1000 points that satisfy those constraints to an output_file.
Note: The print() statements in the script have been commented out.

### Explanation
The idea of a bread-first search (BFS) is used to solve this problem. The script starts with with the given feasible sample point and expands outward (incrementing and decrementing by a particular step size) in each dimension. Any valid points that are found are added to a queue. This exploration is done for each point in the queue, after which it is added to the set of feasible points. Once the available space is explored, the step size is reduced by half, and the exploration is started from the given sample point again. This procedure is repeated until the required number of points are found.


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

Since the exploration is done consistenly with a regular step-size, (1.0, 0.5, 0.25, 0.125…), the points found fill the valid space in a uniform manner.

The points collected from mixture.txt (and the order in which they are filled) are shown below.
![mixture.gif](images/mixture.gif)

---

## Timing and Memory
The timing (calculated using the `time` library)
This code finds 1000 points in under 5 seconds for each given sample dataset. 

| Input Sample  | Time Taken    | Dimensions    | Points Generated  |
| ---           | ---           | ---           | ---               |
| mixture.txt   | 0.0088        | 2             | 1000              |
| example.txt   | 0.0375        | 4             | 1000              |
| formulation   | 0.0272        | 4             | 1000              |
| alloy.txt     | 0.3253        | 11            | 1000              |

The memory usage for alloy.txt (calculated using [`memory-profiler`](https://pypi.org/project/memory-profiler/)) is shown below:
![memoryUsage](images/mprof_plot_alloys.png)

---

## Drawbacks:
* An initial point is required to begin the search
* The memory footprint will be large for high dimensional problems where many points are required
* The points that are found will be fill the valid space but may not do it uniformly in all dimensions
* If the valid region is discontinuous, all subregions may not be found