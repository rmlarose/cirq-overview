"""Script for plotting the cirq simulator timing data.

Data is assumed to have the following format:
    ____________________________________________________________________
    | number of qubits | depth | number of repetitions | time (seconds)|
    --------------------------------------------------------------------
"""

# =============================================================================
# imports
# =============================================================================

import matplotlib.pyplot as plt
from numpy import loadtxt, reshape, log, float64

from glob import glob

# =============================================================================
# constants
# =============================================================================

# font sizes
SMALL_SIZE = 14         # small font size for plotting
MEDIUM_SIZE = 18        # medium font size for plotting
BIGGER_SIZE = 36        # large font size for plotting

# format of data
QUBITS_COLUMN = 0       # column index where number of qubits is
DEPTH_COLUMN = 1        # column index where depth is
REPS_COLUMN = 2         # column index where number of repetitions is
TIME_COLUMN = 3         # column index where time is (in seconds)

# details of data
NQUBITS = 8             # number of different qubit numbers used
NDEPTHS = 5             # number of different depths used

# =============================================================================
# plot options
# =============================================================================

plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=MEDIUM_SIZE)  # fontsize of the figure title

# =============================================================================
# load data
# =============================================================================

# file path
fpath = "../timing/"

# simulator type
sim = "xmonsimulator/"

# get all filenames
fnames = glob(fpath + sim + "*.txt")

# make sure we found at least one file
assert len(fnames) > 0, "No data files in directory"

# grab the first data
data = loadtxt(fnames[0], dtype=float64)

# sum up all the data
for fname in fnames[1:]:
    data += loadtxt(fname, dtype=float64)

# divide by the number of data points
data /= len(fnames)

# =============================================================================
# parse the data
# =============================================================================

# grab the time and divide it by the number of repetitions
time = data[:, TIME_COLUMN] / data[:, REPS_COLUMN]

# make sure the number of times is as expected
assert len(time) == NQUBITS * NDEPTHS

# reshape the time values into the format for plotting
time = reshape(time, (NQUBITS, NDEPTHS))
time = time.T

# =============================================================================
# make the plots
# =============================================================================

# get a plot
fig, ax = plt.subplots()

im = ax.imshow(log(time), origin=[0,0], cmap='summer')
#cbar = ax.figure.colorbar(im, ax=ax)

# title and labels
plt.title('Cirq XmonSimulator Performance (in Seconds)', fontsize=16, fontweight='bold')
plt.xlabel('Number of Qubits')
plt.ylabel('Circuit Depth')

xlocs, xlabels = plt.xticks()
plt.xticks(range(NQUBITS), range(10, 24 + 1, 2))

plt.yticks(range(NDEPTHS), range(20, 100 + 1, 20))

# loop over data dimensions and create text annotations
for i in range(len(time)):
    for j in range(len(time[0])):
        tstr = str(time[i, j])
        text = ax.text(j, i, tstr[:5],
                       ha="center", va="center", color="k")

# show the plot
plt.show()