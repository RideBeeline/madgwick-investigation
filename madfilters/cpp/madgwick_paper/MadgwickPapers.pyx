"""Interfaces to the original c based filter in the paper"""
cimport cython
import numpy as np
cimport numpy as np
cimport madg_paper as madg
cimport madg_paper_nocomp as madg_nocomp

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

cdef class MadgwickPaper(Base):
    """This is the original filter from the paper."""

    def __init__(self, q0 = [1.0, 0.0, 0.0, 0.0], beta = 0.1, freq = 256):
        self.set_q(q0)
        self.set_beta(beta)
        self.set_freq(freq)
        madg.zeta = 0
    
    def set_q(self, q):
        madg.SEq_1 = q[0]
        madg.SEq_2 = q[1]
        madg.SEq_3 = q[2]
        madg.SEq_4 = q[3]

    def set_beta(self, beta):
        madg.beta = beta
    
    def set_freq(self, freq):
        madg.deltat = 1/freq

    @cython.boundscheck(False)
    @cython.wraparound(False)  
    def _run_updates(self, np.ndarray[DTYPE_t, ndim=2] acc, 
                          np.ndarray[DTYPE_t, ndim=2] gyr, 
                          np.ndarray[DTYPE_t, ndim=2] mag ):
        """Efficiently run imu data arrays through the filter."""

        cdef int samples = acc.shape[0] # Number of steps

        cdef np.ndarray[DTYPE_t, ndim=2] Q = np.zeros((samples, 4), dtype=DTYPE)

        for s in range(samples):

            madg.filterUpdate(gyr[s,0], gyr[s,1], gyr[s,2], 
                acc[s,0], acc[s,1], acc[s,2], 
                mag[s,0], mag[s,1], mag[s,2])

            Q[s,0] = madg.SEq_1
            Q[s,1] = madg.SEq_2
            Q[s,2] = madg.SEq_3
            Q[s,3] = madg.SEq_4
        
        return Q


cdef class MadgwickPaperNocomp(Base):
    """This is the original filter from the paper but with gyro and magnetic compensation removed"""

    def __init__(self, q0 = [1.0, 0.0, 0.0, 0.0], beta = 0.1, freq = 256):
        self.set_q(q0)
        self.set_beta(beta)
        self.set_freq(freq)
        madg_nocomp.zeta = 0
    
    def set_q(self, q):
        madg_nocomp.SEq_1 = q[0]
        madg_nocomp.SEq_2 = q[1]
        madg_nocomp.SEq_3 = q[2]
        madg_nocomp.SEq_4 = q[3]

    def set_beta(self, beta):
        madg_nocomp.beta = beta
    
    def set_freq(self, freq):
        madg_nocomp.deltat = 1/freq

    @cython.boundscheck(False)
    @cython.wraparound(False)  
    def _run_updates(self, np.ndarray[DTYPE_t, ndim=2] acc, 
                          np.ndarray[DTYPE_t, ndim=2] gyr, 
                          np.ndarray[DTYPE_t, ndim=2] mag ):
        """Efficiently run imu data arrays through the filter."""

        cdef int samples = acc.shape[0] # Number of steps

        cdef np.ndarray[DTYPE_t, ndim=2] Q = np.zeros((samples, 4), dtype=DTYPE)

        for s in range(samples):

            madg_nocomp.filterUpdate(gyr[s,0], gyr[s,1], gyr[s,2], 
                acc[s,0], acc[s,1], acc[s,2], 
                mag[s,0], mag[s,1], mag[s,2])

            Q[s,0] = madg_nocomp.SEq_1
            Q[s,1] = madg_nocomp.SEq_2
            Q[s,2] = madg_nocomp.SEq_3
            Q[s,3] = madg_nocomp.SEq_4
        
        return Q