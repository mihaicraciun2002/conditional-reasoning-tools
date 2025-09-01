from constants import *
import numpy as np
import pylab as pl
from matplotlib import collections  as mc

def display(closure_algorithm, input_mt):
    global INF
    try:
        n, m, valuations_raw, valuations, ranks, ranks_right = closure_algorithm(input_mt, return_input = True)
    except:
        n, m, valuations_raw, valuations, ranks = closure_algorithm(input_mt, return_input = True)
        ranks_right = ranks.copy()
    lines = []

    rank_max = 0

    for idx in range(len(ranks)):
        rank_max = max(rank_max, ranks[idx])

    endpoints_1 = []
    endpoints_2 = []

    for idx in range(len(ranks)):
        lines.append([])
        if ranks[idx] != INF:
            lines[idx] = [(ranks[idx], idx), (ranks_right[idx], idx)]
            endpoints_1.append((ranks[idx], idx))
            endpoints_2.append((ranks_right[idx], idx))
        else:
            lines[idx] = [(0, idx), (0, idx)]

    lc = mc.LineCollection(lines, linewidths=2)
    fig, ax = pl.subplots()
    pl.yticks(range(len(ranks)), valuations_raw)
    pl.xticks(range(rank_max + 1))
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    ax.plot([x[0] for x in endpoints_1], [x[1] for x in endpoints_1], 'bo')
    ax.plot([x[0] for x in endpoints_2], [x[1] for x in endpoints_2], 'bo')
    # ax.plot(endpoints_2, 'ro')

def display_raw(labels, ranks, reverse = False):
    if not reverse:
        labels = labels[::-1]
        ranks = ranks[::-1]
    endpoints_1 = []
    endpoints_2 = []
    lines = []
    rank_max = 0
    for idx in range(len(ranks)):
        lines.append([])
        lines[idx] = [(ranks[idx][0], idx), (ranks[idx][1], idx)]
        endpoints_1.append((ranks[idx][0], idx))
        endpoints_2.append((ranks[idx][1], idx))

        rank_max = max(rank_max, ranks[idx][1])
    
    lc = mc.LineCollection(lines, linewidths=2)
    
    for idx in range(len(labels)):
        labels[idx] = str(labels[idx])
    fig, ax = pl.subplots()
    pl.yticks(range(len(ranks)), labels)
    pl.xticks(range(rank_max + 1))
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    ax.plot([x[0] for x in endpoints_1], [x[1] for x in endpoints_1], 'bo')
    ax.plot([x[0] for x in endpoints_2], [x[1] for x in endpoints_2], 'bo')

