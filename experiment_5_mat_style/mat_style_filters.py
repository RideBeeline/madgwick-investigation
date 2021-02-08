"""Comparing to original Paper's code"""
# %%
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec

import numpy as np


import madfilters.mat as mat
import madfilters.py as py
import madfilters.cpp as cpp
import madfilters.utils.io as io
import madfilters.utils.orientation as ot

beta = 0.3

# Load imu data

acc, gyr, mag, times, q0, freq = io.load_sample_data()

# Set up figure

fig = plt.figure(figsize=(12, 7), facecolor="w")
fig.suptitle("Matlab-like filters", fontsize=16)
spec = gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[2, 1])

ax0 = plt.subplot(spec[0])
ax0.set(ylabel='yaw (deg)', title="Filter output yaw value.")
ax0.grid()
ax0.set_yticks([-30, 0, 45, 90, 135])
ax0.text(15, 30, rf'$\beta={beta:0.2f},\ f={freq:.1f} \mathrm{{Hz}}$',
         fontsize=12, bbox=dict(boxstyle='round', fc='white', ec='lightgray'))


ax1 = plt.subplot(spec[1])
ax1.set(xlabel='time (s)', ylabel='difference (deg)',
        title="Difference in angle between quaternions")
ax1.grid()

num_plots = 4
curr_plot = 0

cmap = plt.get_cmap('gist_rainbow')
norm = matplotlib.colors.Normalize(vmin=0, vmax=num_plots)  

# Load data from matlab
Q_base = io.sync_with_matlab('mat_out.pickle', acc, gyr, mag, q0, beta, freq)

def plot_filter_output(ax0, ax1, Q_base, Q, label):
    global curr_plot
    yaw = ot.q_to_aero_yaw(Q)
    diff = ot.q_angle_diff_safe(Q_base, Q)

    rgba = cmap(norm(curr_plot))
    curr_plot += 1

    ax0.plot(times, yaw, ls='--', c=rgba, label=label, alpha=0.7)
    ax1.plot(times, diff, ls='--', c=rgba, label=label, alpha=0.7)

plot_filter_output(ax0, ax1, Q_base, Q_base, "Matlab")


# Through the ahrs module's madgwick
Q = py.AhrsMadgwick(beta=beta, freq=freq, q0=q0).update(acc, gyr, mag)
plot_filter_output(ax0, ax1, Q_base, Q, "ahrs")

# Matlab clone
Q = py.MatlabClone(beta=beta, freq=freq, q0=q0).update(acc, gyr, mag)
plot_filter_output(ax0, ax1, Q_base, Q, "Matlab Clone")

# C code with 2x fix
Q = cpp.MadgwickFixed(beta=beta, freq=freq, q0=q0).update(acc, gyr, mag)
plot_filter_output(ax0, ax1, Q_base, Q, "C + fixed")

ax0.legend()


plt.savefig("./exp5_mat_style.png", transparent=False)

plt.show()

