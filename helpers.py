from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
#Usage: PlotPoints(self.point_set, self.input_file_name.split("/")[-1][:-4],f'Points:{len(self.point_set)} Step size: {step_size}')

# Utility to plot points in 3D
def PlotPoints3D(pointsExplored, filename, dim0=0, dim1=1, dim2=2):
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    xs=[]
    ys=[]
    zs=[]
    for _ in pointsExplored:
        xs.append(_[dim0])
        ys.append(_[dim1])
        zs.append(_[dim2])
    ax.scatter3D(xs, ys, zs, c='#1f2db4', cmap='hsv',marker='o')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 0.1)

    # plt.show()
    plt.title(f'Total points used = {len(pointsExplored)}')
    plt.savefig(f'./images/{filename}_len{len(pointsExplored)}')
    plt.cla()
    plt.clf()

# Utility to plot points in 2D
def PlotPoints(pointsExplored, filename, title, dim0=0, dim1=1):
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
    plt.title(title)
    plt.savefig(f'./images/{filename}_len{len(pointsExplored)}')
    plt.cla()
    plt.clf()
    # plt.show()

# Utility to plot points in 2D
def PlotPoints1D(pointsExplored, filename, dim0=0, dim1=1):
    xs=[]
    ys=[]
    for _ in pointsExplored:
        xs.append(_)
        ys.append(0)

    plt.scatter(xs, ys,marker='o', c='#1f2db4')
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.xlabel(f'x[{dim0}]')
    plt.ylabel(f'x[{dim1}]')
    plt.title(f'Total points used = {len(pointsExplored)}')
    plt.savefig(f'./images/{filename}_len{len(pointsExplored)}')
    # plt.show()
    plt.cla()
    plt.clf()
