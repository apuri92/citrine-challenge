import os, sys
import numpy as np
import matplotlib.pyplot as plt
import imageio
from pathlib import Path
import glob

input_file_name = sys.argv[1]

files = glob.glob(f"./images/{input_file_name}_*.png")
files.sort(key=os.path.getmtime)
for file in files:
    print(file)

# paths = sorted(Path('images').iterdir(), key=os.path.getmtime)
with imageio.get_writer(f'./images/{input_file_name}.gif', mode='I',duration=0.2,loop=-1) as writer:
    for filename in files:
        image = imageio.imread(filename)
        writer.append_data(image)