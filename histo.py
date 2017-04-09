#!/usr/bin/env python
import numpy as np
from scipy.interpolate import spline
from matplotlib import gridspec
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

# Get current size
fig_size = plt.rcParams["figure.figsize"]
# Set figure width to 12 and height to 9
print(fig_size)
fig_size[0] = 12
fig_size[1] = 5
plt.rcParams["figure.figsize"] = fig_size

fig = plt.figure(dpi=None, facecolor="white")

# histogram our data with numpy
binedges = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55,
            0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]

bincenters = [0.025, 0.075, 0.125, 0.175, 0.225, 0.275, 0.325, 0.375, 0.425,
              0.475, 0.525, 0.575, 0.625, 0.675, 0.725, 0.775, 0.825, 0.875,
              0.925 , 0.975]

data_N = [227, 8075, 100851, 545880, 771393, 512225, 246382, 169306, 163280,
          141312, 97975, 56857, 38200, 32972, 35268, 41484, 59981, 52033, 11324,
          1571]
# data_N = [170, 438, 572, 343, 182, 87, 50, 21, 10, 2, 7, 0, 1, 0, 1, 1, 0, 0, 0, 0]
# data_N = [105, 2585, 4389, 1261, 216, 53, 15, 8, 26, 27, 53, 52, 50, 39, 28, 17, 10, 9, 3, 1]
# data_N = [40, 5666, 11177, 4108, 654, 124, 39, 18, 31, 20, 42, 43, 44, 50, 40, 15, 14, 3, 3, 4]

data_P = [0, 8, 376, 778, 4426, 7204, 8275, 7372, 5574, 3823, 2496, 1580, 1064,
        911, 946 , 1107, 1252, 1352, 833 , 190]
# data_P = [0, 0, 0, 0, 0, 0, 1, 1, 0, 3, 2, 5, 8, 7, 6, 4, 1, 0, 0, 0]
# data_P = [0, 0, 0, 0, 1, 1, 10, 7, 26, 27, 53, 52, 50, 39, 28, 17, 10, 9, 3, 1]
# data_P = [0, 0, 0, 0, 0, 4, 6, 15, 31, 20, 42, 43, 44, 50, 40, 15, 14, 3, 3, 4]

wsum_P = sum(data_P)
data_P[:] = [float(weight)/wsum_P for weight in data_P]
wsum_N = sum(data_N)
data_N[:] = [float(weight)/wsum_N for weight in data_N]


###############################################################################
# Line Plot
###############################################################################

# bincenters = 0.5 * (bins[1:] + bins[:-1])
newcenters = np.linspace(min(bincenters), max(bincenters), 300)
smooth_P = spline(bincenters, data_P, newcenters)
smooth_N = spline(bincenters, data_N, newcenters)
plt.plot(newcenters, smooth_P, '-', color='#1f77b4', label="True Matches")
plt.plot(newcenters, smooth_N, '-', color='#ff7f0e', label="True Non-Matches")
plt.xlabel("Similarity")
plt.ylabel("Amount")
plt.ylim(0, max(max(smooth_P), max(smooth_N)) + 0.02)
plt.title("True Ground Truth Distribution (ncvoter)")
plt.legend(loc="best")

###############################################################################
# Histogram
###############################################################################

# fig = plt.figure(dpi=None, facecolor="white")
# ax = fig.add_subplot(111)

# # get the corners of the rectangles for the histogram
# left = np.array(binedges[:-1])
# right = np.array(binedges[1:])
# bottom = np.zeros(len(left))
# top = bottom + data_P

# # we need a (numrects x numsides x 2) numpy array for the path helper
# # function to build a compound path
# XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T

# # get the Path object
# barpath = path.Path.make_compound_path_from_polys(XY)
# # make a patch out of it
# patch = patches.PathPatch(barpath, facecolor='#1f77b4', alpha=0.8)
# ax.add_patch(patch)
# # update the view limits
# ax.set_xlim(left[0], right[-1])
# ax.set_ylim(bottom.min(), top.max() + (top.max() * 0.05))
# plt.xlabel("Ähnlichkeit")
# plt.ylabel("Anzahl")

# plt.title("Verteilung der Matches (NCVoter)")

# plt.show()
picture_names = ["ncvoter_histo_P"]
for index, figno in enumerate(plt.get_fignums()):
    plt.figure(figno)
    plt.savefig("%s.pdf" % picture_names[index], bbox_inches='tight')

plt.close('all')
