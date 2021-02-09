"""The most basic experiment, comparing the matlab and the c code."""
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


# Run imu data through Madgwick's c code
mad_c = cpp.MadgwickOriginal(beta=beta, freq=freq, q0=q0)
c_Q = mad_c.update(acc, gyr, mag)
c_yaw = ot.q_to_aero_yaw(c_Q)
# c_yaw = q_to_yaw_yrp(c_Q)

# Load data from matlab
m_Q = io.sync_with_matlab('mat_out.pickle', acc, gyr, mag, q0, beta, freq)
m_yaw = ot.q_to_aero_yaw(m_Q)

# Calculate differences in quaternions
diff = ot.q_angle_diff(m_Q, c_Q)

# %%
# Plot figure

fig = plt.figure(figsize=(12, 7), facecolor="w")

fig.suptitle("Madgwick's implementations, slower data", fontsize=16)

spec = gridspec.GridSpec(ncols=1, nrows=2,
                         height_ratios=[2, 1])

ax0 = plt.subplot(spec[0])
ax0.plot(times, m_yaw, '--g', label='Matlab', alpha=0.7)
ax0.plot(times, c_yaw, '--r', label='C', alpha=0.7)


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
ax1.plot(times, diff, c='#3355ff', label='Matlab', alpha=0.7)

plt.savefig("./exp2_mat_vs_c_2.png", transparent=False)

plt.show()
# %%
