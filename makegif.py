import os
import numpy as np
import matplotlib.pyplot as plt
import imageio
from pathlib import Path
import glob

files = glob.glob("./images/mixture_*.png")
files.sort(key=os.path.getmtime)
for file in files:
    print(file)

# paths = sorted(Path('images').iterdir(), key=os.path.getmtime)
with imageio.get_writer('./images/mixture.gif', mode='I',duration=0.1,loop=-1) as writer:
    for filename in files:
        image = imageio.imread(filename)
        writer.append_data(image)