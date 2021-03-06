# coding: utf-8

import sys
import numpy
from matplotlib import pyplot, rcParams
from matplotlib.backends.backend_pdf import FigureCanvasPdf

rcParams['font.family'] = 'serif'
rcParams['font.size'] = '10'

# load result file
result = open(sys.argv[1])
lines = result.readlines()


for i,line in enumerate(lines):
    if "StokesBEM on a sphere: Speedup" in line:
        break

temp = []

for line in lines[i+1:]:
    # remove string "s" (seconds) for parsing
    for elem in line.replace("s","").split():
        try:
            temp.append(float(elem))
        except ValueError:
            pass

# remove recursion number from the list
del temp[::4]

# make an average for each case
time = numpy.mean(numpy.array(temp).reshape(-1,3), axis=1)

# calculate speedup
speedup = time[::2] / time[1::2]
print("Speedup: ", speedup)
print("fixed-p: ", time[::2])
print("relaxed-p: ", time[1::2])

ind = numpy.arange(len(speedup))
width = 0.3

# set up plot
fig = pyplot.figure(figsize=(3,2), dpi=80)
ax = fig.add_subplot(111)

# plot
bar = ax.bar(ind+0.1, speedup, width, fill=False, edgecolor='k', hatch='..'*2, linewidth=1)

# axis labels
ax.set_xticks(ind+0.1+width/2)
ax.set_xlim(-0.4, 3)
ax.set_ylim(0, numpy.ceil(numpy.max(speedup)))
ax.set_xticklabels( ('8192','32768','131072') )
ax.set_ylabel('Speedup', fontsize=10)
ax.set_xlabel('N', fontsize=10)
fig.subplots_adjust(left=0.195, bottom=0.21, right=0.955, top=0.95)
canvas = FigureCanvasPdf(fig)

# plot to pdf
canvas.print_figure('StokesSpeedupRelaxation.pdf',dpi=80)