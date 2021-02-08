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


# Run imu data through Madgwick's c code
mad_orig = cpp.MadgwickOriginal(beta=beta, freq=freq, q0=q0)
orig_Q = mad_orig.update(acc, gyr, mag)
orig_yaw = ot.q_to_aero_yaw(orig_Q)


mad_sqrt = cpp.MadgwickOriginalSqrt(beta=beta, freq=freq, q0=q0)
sqrt_Q = mad_sqrt.update(acc, gyr, mag)
sqrt_yaw = ot.q_to_aero_yaw(sqrt_Q)

# Calculate differences in quaternions
sqrt_diff = ot.q_angle_diff(orig_Q, sqrt_Q)

# %%
# Plot figure

fig = plt.figure(figsize=(12, 7), facecolor="w")

fig.suptitle("Madgwick's C filters", fontsize=16)

spec = gridspec.GridSpec(ncols=1, nrows=2,
                         height_ratios=[2, 1])

ax0 = plt.subplot(spec[0])
ax0.plot(times, orig_yaw, '--g', label='Unmodified', alpha=0.7)
ax0.plot(times, sqrt_yaw, '--r', label='1/sqrt()', alpha=0.7)


ax0.set(ylabel='yaw (deg)',
        title="Filter output yaw value.")
ax0.grid()

ax0.text(15, 0, rf'$\beta={beta:0.2f},\ f={freq:.1f} \mathrm{{Hz}}$',
         fontsize=12, bbox=dict(boxstyle='round', fc='white', ec='lightgray'))

ax0.legend()

ax0.set_yticks([-30, 0, 45, 90, 135])


ax1 = plt.subplot(spec[1])
ax1.set(xlabel='time (s)', ylabel='difference (deg)',
        title="Difference in angle between quaternions")
ax1.grid()
ax1.plot(times, sqrt_diff, c='#3355ff', label='Matlab', alpha=0.7)

plt.savefig("./exp3_c_vs_c.png", transparent=False)

plt.show()
# %%
