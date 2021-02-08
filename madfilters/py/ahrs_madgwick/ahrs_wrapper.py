"""Just a simple wrapper function"""

import numpy as np
import ahrs

class AhrsMadgwick:

    def __init__(self, q0 = [1.0, 0.0, 0.0, 0.0], beta = 0.1, freq = 256):

        q0 = np.array(q0)
        self.filter = ahrs.filters.Madgwick(q0=q0, gain = beta, frequency = freq)
        self.q = q0
    
    def set_q(self, q):
        self.q = q
    
    def set_beta(self, beta):
        self.filter.gain = beta

    def set_freq(self, freq):
        self.filter.Dt = 1 / freq

    def update(self, acc, gyr, mag, q = None, beta = None, freq = None):
        
        if q is not None:
            self.set_q(q)
        
        if beta is not None:
            self.set_beta(beta)

        if freq is not None:
            self.set_freq(freq)

        if isinstance(acc, np.ndarray) and acc.ndim == 2:
            Q=np.zeros((len(acc), 4), dtype = np.double)

            for t, _ in enumerate(acc):
                self.q = self.filter.updateMARG(q=self.q, gyr=gyr[t], acc=acc[t], mag=mag[t])
                Q[t, :]=self.q
            return Q

        self.q = self.filter.updateMARG(q=self.q, gyr=gyr, acc=acc, mag=mag)
        return self.q