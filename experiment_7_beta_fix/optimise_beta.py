"""Find what beta values reduce the effect of the bug"""
# %%
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec

import numpy as np
import scipy.optimize

import madfilters.py as py
import madfilters.cpp as cpp
import madfilters.mat as mat
import madfilters.utils.io as io
import madfilters.utils.orientation as ot

# Beta of the python filter. The aim of the optimisation is to find a beta for the
#  C filter that leads to similar filter outputs.
beta_py = 0.1

# Load imu data
acc, gyr, mag, times, q0, freq = io.load_sample_data()

# Through the ahrs module's madgwick filter, this gives us a reference to compare to
ahrs_filter = py.AhrsMadgwick(beta=beta_py, freq=freq, q0=q0)
ahrs_Q = ahrs_filter.update(acc, gyr, mag)


def show_beta_optimisation(acc, gyr, mag, times, Q_comp):
    """ Chooses a value of beta so that the c based filter most closely 
    tracks the python filter. """

    # Optimisation part
    mad_filter = cpp.MadgwickOriginalSqrt(freq=freq)

    def quat_diff(beta):
        """Calculate quaternions and average difference"""
        sqrt_Q = mad_filter.update(acc, gyr, mag, beta=beta, q=q0)
        diff = ot.q_angle_diff_safe(Q_comp, sqrt_Q)
        return np.average(diff)

    result = scipy.optimize.minimize(fun=quat_diff, x0=beta_py,
                                     method='Nelder-Mead', options=dict(maxiter=100))

    beta_optimum = result.x[0]
    diff_optimum = result.fun

    # Generate plot to show the result of optmisation.

    fig = plt.figure(figsize=(14, 7), facecolor="w")
    fig.suptitle(fr"Finding optimum Beta to match $\beta={beta_py:.2f}$", fontsize=16)

    gs = gridspec.GridSpec(2, 2, height_ratios=[2.5, 1], figure=fig, hspace=0.3)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, :])

    # Plot 0 shows the yaw output of the C and Py filter. This is the most similar that was found.
    yaw_comp = ot.q_to_aero_yaw(Q_comp)
    sqrt_Q = mad_filter.update(acc, gyr, mag, beta=beta_optimum, q=q0)
    yaw_sqrt = ot.q_to_aero_yaw(sqrt_Q)
    ax0.set(ylabel='yaw (deg)', xlabel='time (s)',
            title="Plot 1: Filter yaw value over time")
    ax0.grid()
    ax0.plot(times, yaw_comp, '--r', label=fr"Py: $\beta={beta_py:.2f}$", alpha=0.7)
    ax0.plot(times, yaw_sqrt, '--g', label=fr"C: $\beta={beta_optimum:.2f}$", alpha=0.7)
    ax0.legend()

    # Plot 1 shows the optimisation
    betas = np.linspace(0.01, 6, 50)
    vquat_diff = np.vectorize(quat_diff)
    y_values = vquat_diff(betas)
    ax1.plot(betas, y_values, label='Quat Difference')
    ax1.axvline(beta_optimum, label=fr"$\beta={beta_optimum:.2f}$", color='g', ls=':')
    ax1.axhline(diff_optimum, label=fr"Diff = ${diff_optimum:.2f}°$", color='r', ls=':')
    ax1.set(xlabel='beta', ylabel='average difference (deg)', title='Plot 2: Average difference')
    ax1.legend()

    # Plot 2 shows the difference in quaternions
    diff = ot.q_angle_diff_safe(sqrt_Q, Q_comp)
    diff_avg = np.average(diff)

    ax2.plot(times, diff, c='#3355ff', label='Diff', alpha=0.7)
    ax2.axhline(diff_avg, label=fr"Avg Diff = ${diff_avg:.2f}°$", color='r', ls=':')
    ax2.set(xlabel='time (s)', ylabel='difference (deg)',
            title="Plot 3: Difference in angle between quaternions")
    ax2.legend()

    return beta_optimum

def show_betas(betas, beta_optimum, Q_base):
    """ Plots Filter yaw and quaternion error at different Beta values """
    betas = np.round(betas, decimals=2)
    betas = np.sort(betas)

    # Set up figure
    yaw_base = ot.q_to_aero_yaw(Q_base)

    fig = plt.figure(figsize=(14, 7), facecolor="w")
    fig.suptitle("Different Beta values for C filter", fontsize=16)

    gs = gridspec.GridSpec(ncols=1, nrows=2,
                        height_ratios=[2, 1])

    # Set up colourmap
    cmap = plt.get_cmap('winter')
    norm = matplotlib.colors.Normalize(vmin=0, vmax=len(betas))  # normalize item number values to colormap

    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])


    # Plot all the different beta curves
    mad_sqrt = cpp.MadgwickOriginalSqrt(freq=freq)

    for idx, beta in enumerate(betas):
        sqrt_Q = mad_sqrt.update(acc, gyr, mag, beta=beta, q=q0)
        sqrt_yaw = ot.q_to_aero_yaw(sqrt_Q)

        diff = ot.q_angle_diff_safe(sqrt_Q, Q_base)

        # Highlight the optimimum beta value in the legend
        label = rf'$\beta={beta:.2f}$'
        if abs(beta - beta_optimum) < 0.01:
            label += " (o)"
        rgba_colour = cmap(norm(idx))
        ax0.plot(times, sqrt_yaw, c=rgba_colour, label=label, alpha=0.7)
        ax1.plot(times, diff, c=rgba_colour, label=label, alpha=0.7)

    ax0.plot(times, yaw_base, ls='--', lw=2, c='orangered', label='Py: ahrs', alpha=0.7)

    ax0.set(ylabel='yaw (deg)', title="C filter yaw over time")
    ax0.grid()
    ax0.text(16, 15, rf'$f={freq:.1f} \mathrm{{Hz}},$ Py:ahrs $\beta={beta_py:0.2f}$',
            fontsize=12, bbox=dict(boxstyle='round', fc='white', ec='lightgray'))
    ax0.legend()
    ax0.set_yticks([-30, 0, 45, 90, 135])

    ax1.set(xlabel='time (s)', ylabel='difference (deg)',
            title="Difference in angle between quaternions")
    ax1.grid()

# Now plot a bunch of betas to show how changing it affects the resulting yaw graphs
beta_optimum = show_beta_optimisation(acc, gyr, mag, times, ahrs_Q)
plt.savefig(f"./exp7_d1_optimise_beta_{beta_py*100:.0f}.png", transparent=False)
# %%
betas = [0.01, 0.1, 0.3, 0.6, 1.2, 2, beta_optimum]
show_betas(betas, beta_optimum, ahrs_Q)
plt.savefig(f"./exp7_d1_show_betas_{beta_py*100:.0f}.png", transparent=False)

# Same thing with the original madgwick sample data
Q_mat, beta, freq, times, acc, gyr, mag = io.load_hdf5(
    mat.example_data_filename, load_imu_data=True)
q0 = Q_mat[0]
beta_optimum = show_beta_optimisation(acc, gyr, mag, times, Q_mat)
plt.savefig(f"./exp7_d2_optimise_beta_{beta_py*100:.0f}.png", transparent=False)

betas = [0.01, 0.1, 0.2, 0.6, beta_optimum]
show_betas(betas, beta_optimum, Q_mat)
plt.savefig(f"./exp7_d2_show_betas_{beta_py*100:.0f}.png", transparent=False)

plt.show()


# %%
