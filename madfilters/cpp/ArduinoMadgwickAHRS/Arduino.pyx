"""Interface to Adafruit AHRS library"""
cimport cython
import numpy as np
cimport numpy as np
from arduino_madgwick cimport Madgwick

DTYPE = np.double # Default datatype for numpy arrays
ctypedef np.double_t DTYPE_t

cdef class Base:

    def update(self, acc, gyr, mag, q = None, beta = None, freq = None):
        
        if q is not None:
            self.set_q(q)
        
        if beta is not None:
            self.set_beta(beta)

        if freq is not None:
            self.set_freq(freq)

        if isinstance(acc, np.ndarray) and acc.ndim == 2:
            assert acc.dtype == DTYPE and gyr.dtype == DTYPE and mag.dtype == DTYPE

            if acc.shape[1] != 3 or gyr.shape[1] != 3 or mag.shape[1] != 3:
                raise ValueError("Acc, gyr, mag need to be x by 3 arrays.")

            if gyr.shape[0] != acc.shape[0] or mag.shape[0] != acc.shape[0]:
                raise ValueError("Acc, gyr and mag need to be the same length.")

            return self._run_updates(acc, gyr, mag)

        else:
            return self._run_updates(np.array([acc], dtype=DTYPE),
                                     np.array([gyr], dtype=DTYPE),
                                     np.array([mag], dtype=DTYPE))[0]

cdef class Arduino(Base):
    """Wrapper around the Arduino's Madgwick class."""

    cdef Madgwick c_madg

    def __cinit__(self):
        self.c_madg = Madgwick()

    def __init__(self, q0 = [1.0, 0.0, 0.0, 0.0], beta = 0.1, freq = 256):
        self.set_q(q0)
        self.set_beta(beta)
        self.set_freq(freq)
    
    def set_q(self, q):
        self.c_madg.q0 = q[0]
        self.c_madg.q1 = q[1]
        self.c_madg.q2 = q[2]
        self.c_madg.q3 = q[3]

    def set_beta(self, beta):
        self.c_madg.beta = beta
    
    def set_freq(self, freq):
        self.c_madg.invSampleFreq = 1/freq

    @cython.boundscheck(False)
    @cython.wraparound(False)  
    def _run_updates(self, np.ndarray[DTYPE_t, ndim=2] acc, 
                          np.ndarray[DTYPE_t, ndim=2] gyr, 
                          np.ndarray[DTYPE_t, ndim=2] mag ):
        """Efficiently run imu data arrays through the filter."""
        cdef int samples = acc.shape[0] # Number of steps

        cdef np.ndarray[DTYPE_t, ndim=2] Q = np.zeros((samples, 4), dtype=DTYPE)

        cdef double rad2deg = 57.2958

        for s in range(samples):

            self.c_madg.update(gyr[s,0] * rad2deg, gyr[s,1] * rad2deg, gyr[s,2] * rad2deg, 
                acc[s,0], acc[s,1], acc[s,2], 
                mag[s,0], mag[s,1], mag[s,2])

            Q[s,0] = self.c_madg.q0
            Q[s,1] = self.c_madg.q1
            Q[s,2] = self.c_madg.q2
            Q[s,3] = self.c_madg.q3
        
        return Q
