"""Just wraps the matlab clone"""

import numpy as np
from .matlab_clone import Update as filter_update

class MatlabClone:

    def __init__(self, q0 = [1.0, 0.0, 0.0, 0.0], beta = 0.1, freq = 256):

        q0 = np.array(q0)
        self.set_q(q0)
        self.set_freq(freq)
        self.set_beta(beta)

    
    def set_q(self, q):
        self.q = q.copy()
    
    def set_beta(self, beta):
        self.beta = beta

    def set_freq(self, freq):
        self.Dt = 1 / freq

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
                self.q = filter_update(q=self.q, Gyroscope=gyr[t], Accelerometer=acc[t], Magnetometer=mag[t], Beta=self.beta, SamplePeriod=self.Dt)
                Q[t, :] = self.q
            return Q

        self.q = filter_update(q=self.q, Gyroscope=gyr, Accelerometer=acc, Magnetometer=mag, Beta=self.beta, SamplePeriod=self.Dt)
        return self.q