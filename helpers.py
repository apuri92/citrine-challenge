from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

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