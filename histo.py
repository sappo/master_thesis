#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path

# setup plot details
lw = 2

plt.rcParams.update({'font.size': '12'})
plt.rcParams.update({'figure.titlesize': 'x-large'})
plt.rcParams.update({'axes.titlesize': 'x-large'})
plt.rcParams.update({'axes.labelsize': 'large'})
plt.rcParams.update({'legend.fontsize': 'medium'})

fig = plt.figure(dpi=None, facecolor="white")
fig.canvas.set_window_title("Frequency Distribution")
ax = fig.add_subplot(111)

# histogram our data with numpy
bins = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6,
        0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
n = [0, 8, 376, 778, 4426, 7204, 8275, 7372, 5574, 3823, 2496, 1580, 1064, 911,
     946 , 1107, 1252, 1352, 833 , 190]

# get the corners of the rectangles for the histogram
left = np.array(bins[:-1])
right = np.array(bins[1:])
bottom = np.zeros(len(left))
top = bottom + n

# we need a (numrects x numsides x 2) numpy array for the path helper
# function to build a compound path
XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T

# get the Path object
barpath = path.Path.make_compound_path_from_polys(XY)
# make a patch out of it
patch = patches.PathPatch(barpath, facecolor='#1f77b4', alpha=0.8)
ax.add_patch(patch)
# update the view limits
ax.set_xlim(left[0], right[-1])
ax.set_ylim(bottom.min(), top.max() + (top.max() * 0.05))
plt.xlabel("Ähnlichkeit")
plt.ylabel("Anzahl")

plt.title("NCVoter")
plt.suptitle("Verteilung der Matches")
plt.show()
