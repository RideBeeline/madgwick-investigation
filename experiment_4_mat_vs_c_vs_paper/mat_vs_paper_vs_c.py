"""Comparing to original Paper's code"""
# %%
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec

import numpy as np


import madfilters.mat as mat
import madfilters.cpp as cpp
import madfilters.utils.io as io
import madfilters.utils.orientation as ot

beta = 0.06

# Load imu data

acc, gyr, mag, times, q0, freq = io.load_sample_data()

# Set up figure

fig = plt.figure(figsize=(12, 7), facecolor="w")
fig.suptitle("All of Madgwick's Implementations", fontsize=16)
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

num_plots = 6
curr_plot = 0

cmap = plt.get_cmap('gist_rainbow')
norm = matplotlib.colors.Normalize(vmin=0, vmax=num_plots-1)  

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


# Through the code without fast_inv_sqrt()
Q = cpp.MadgwickOriginalSqrt(beta=beta, freq=freq, q0=q0).update(acc, gyr, mag)
plot_filter_output(ax0, ax1, Q_base, Q, "C + 1/sqrt()")

# Through the code with fix
Q = cpp.MadgwickFixed(beta=beta, freq=freq, q0=q0).update(acc, gyr, mag)
plot_filter_output(ax0, ax1, Q_base, Q, "C fix")

# Through the code from the paper
Q = cpp.MadgwickPaper(beta=beta, freq=freq, q0=q0).update(acc, gyr, mag)
plot_filter_output(ax0, ax1, Q_base, Q, "paper org")

# Through the code from the paper but without compensation
Q = cpp.MadgwickPaperFixed(beta=beta, freq=freq, q0=q0).update(acc, gyr, mag)
plot_filter_output(ax0, ax1, Q_base, Q, "paper fix")


# Through the code from the paper but without compensation
Q = cpp.MadgwickPaperNocomp(beta=beta, freq=freq, q0=q0).update(acc, gyr, mag)
plot_filter_output(ax0, ax1, Q_base, Q, "paper nocomp")


ax0.legend()


plt.savefig("./exp4_mat_vs_paper_vs_c.png", transparent=False)

plt.show()
