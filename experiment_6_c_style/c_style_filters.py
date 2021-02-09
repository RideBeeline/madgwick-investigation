"""Checking if fast_inv_sqrt or float precission cause problems"""
# %%
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec

import numpy as np


import madfilters.mat as mat
import madfilters.cpp as cpp
import madfilters.utils.io as io
import madfilters.utils.orientation as ot

beta = 0.3

# Load imu data

acc, gyr, mag, times, q0, freq = io.load_sample_data()

# Set up figure

fig = plt.figure(figsize=(12, 7), facecolor="w")
fig.suptitle("C style filters", fontsize=16)
spec = gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[2, 1])

ax0 = plt.subplot(spec[0])
ax0.set(ylabel='yaw (deg)', title="Filter output, yaw value")
ax0.grid()
ax0.set_yticks([-30, 0, 45, 90, 135])
ax0.text(15, 30, rf'$\beta={beta:0.2f},\ f={freq:.1f} \mathrm{{Hz}}$',
         fontsize=12, bbox=dict(boxstyle='round', fc='white', ec='lightgray'))


ax1 = plt.subplot(spec[1])
ax1.set(xlabel='time (s)', ylabel='difference (deg)',
        title="Difference in angle between quaternions")
ax1.grid()

num_plots = 5
curr_plot = 0

cmap = plt.get_cmap('gist_rainbow')
norm = matplotlib.colors.Normalize(vmin=0, vmax=num_plots-1)  

# Through the code without fast_inv_sqrt()
mad_sqrt = cpp.MadgwickOriginalSqrt(beta=beta, freq=freq, q0=q0)
Q_base = mad_sqrt.update(acc, gyr, mag)

def run_and_plot_filter(ax0, ax1, Q_base, madg, label):
    global curr_plot
    Q = madg.update(acc, gyr, mag)
    yaw = ot.q_to_aero_yaw(Q)
    diff = ot.q_angle_diff_safe(Q_base, Q)

    rgba = cmap(norm(curr_plot))
    curr_plot += 1

    ax0.plot(times, yaw, ls='--', c=rgba, label=label, alpha=0.7)
    ax1.plot(times, diff, ls='--', c=rgba, label=label, alpha=0.7)

mad_sqrt.set_q(q0)
run_and_plot_filter(ax0, ax1, Q_base, mad_sqrt, 'Madg C (sqrt fix)')

# Through the unmodified code
run_and_plot_filter(ax0, ax1, Q_base, 
    cpp.MadgwickOriginal(beta=beta, freq=freq, q0=q0), 
    'Madg C')

# Through the code without fast_inv_sqrt() and doubles
run_and_plot_filter(ax0, ax1, Q_base, 
    cpp.MadgwickOriginalSqrtDouble(beta=beta, freq=freq, q0=q0), 
    'Madg C (sqrt & double)')

# Adafruit
run_and_plot_filter(ax0, ax1, Q_base, 
    cpp.Adafruit(beta=beta, freq=freq, q0=q0), 
    'Adafruit')

# Arduino
run_and_plot_filter(ax0, ax1, Q_base, 
    cpp.Arduino(beta=beta, freq=freq, q0=q0), 
    'Arduino')


ax0.legend()


plt.savefig("./exp6_c_style_filters.png", transparent=False)

plt.show()