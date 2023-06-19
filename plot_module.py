import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

def plot_function():
    plt.rcParams["font.family"] = "Times New Roman"
    font = {'family': 'Times New Roman', 'size': 20, 'weight': 'normal'}
    plt.rc('font', **font)
    fig, ax = plt.subplots(facecolor='w', edgecolor='k', tight_layout=True)
    plt.gca()
    ax.tick_params(direction='in', length=7.0, width=1.5)
    right_side = ax.spines["right"]
    right_side.set_visible(True)
    top_side = ax.spines["top"]
    top_side.set_visible(True)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2.0)

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which='minor', direction='in', length=4)

    def adjust_lightness(color, amount=0.5):
        import matplotlib.colors as mc
        import colorsys
        try:
            c = mc.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

    # Add your plotting code here
    plt.subplots_adjust(top=0.9)
    # plt.tight_layout()  # Automatically adjust plot layout

