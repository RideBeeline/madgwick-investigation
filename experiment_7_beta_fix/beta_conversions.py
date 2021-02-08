"""Find what initial beta values require the largest fix"""
# %%
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec

import numpy as np
import scipy.optimize

import madfilters.py as py
import madfilters.cpp as cpp
import madfilters.utils.io as io
import madfilters.utils.orientation as ot


# Load imu data
acc, gyr, mag, times, q0, freq = io.load_sample_data()

# Through the ahrs module's madgwick, this gives us a "source of truth" to compare to
ahrs_filter = py.AhrsMadgwick(beta=0.1, freq=freq, q0=q0)
ahrs_Q = ahrs_filter.update(acc, gyr, mag)

#Cut down data for less calculations
mask = (times > 6) & (times<15)
acc=acc[mask]
gyr=gyr[mask]
mag=mag[mask]
times=times[mask]
Q_comp=ahrs_Q[mask]
q0 = Q_comp[0]


def find_optimum_beta(beta_base, base_filter, free_filter):
    """Evaluates the best beta to use on the free filter, given the base filter's beta"""

    Q_base = base_filter.update(acc=acc, gyr=gyr, mag=mag, q=q0, beta=beta_base)
 
    
    def quat_diff(beta, Q_base, free_filter):
        """Calculate quaternions and average difference"""
        Q_free = free_filter.update(acc, gyr, mag, beta=beta, q=q0)
        diff = ot.q_angle_diff_safe(Q_base, Q_free)
        return np.average(diff)


    result = scipy.optimize.minimize(fun=quat_diff, args=(Q_base, free_filter), 
        x0 = beta_base, method='Nelder-Mead', options=dict(maxiter=100))

    beta_optimum = result.x[0]

    return beta_optimum

def find_optimum_betas(base_filter, free_filter):
    betas = np.linspace(0.001,1,100)
    vbeta_diff = np.vectorize(find_optimum_beta)
    y_values = vbeta_diff(betas, base_filter, free_filter)

    return betas, y_values

mad_filter = cpp.MadgwickOriginalSqrt(freq=freq)

betas, y_values = find_optimum_betas(base_filter=ahrs_filter, free_filter=mad_filter)

fig = plt.figure(figsize=(14, 4), facecolor="w")

fig.suptitle('Beta Conversions', fontsize=16)

ax1 = fig.add_subplot()
ax1.plot(betas, y_values/betas, label='Py AHRS vs original C')
ax1.set(xlabel='beta Py Ahrs', ylabel='beta ratio: C / Py Ahrs', title="Ratio of beta values")
ax1.grid()
ax1.legend()


# TODO: Run through fixed cpp filters for speed to produce bug->fix beta change update graph
# %%
print(find_optimum_beta(beta_base=0.303, base_filter=mad_filter, free_filter=ahrs_filter))

# %%
print(find_optimum_beta(beta_base=0.057, base_filter=ahrs_filter, free_filter=mad_filter))
# %%

plt.savefig(f"./exp7_beta_conversions.png", transparent=False)
plt.show()
