"""Interfaces to the original c based filters"""
cimport cython
import numpy as np
cimport numpy as np
cimport madg_orig_s as orig
cimport madg_orig_sqrt as orig_sqrt
cimport madg_orig_sqrt_d as orig_sqrt_d
cimport madg_orig_sqrt_fix as sqrt_fix

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

cdef class MadgwickOriginal(Base):
    """This is the original filter with the ability to change frequency added to it."""

    def __init__(self, q0 = [1.0, 0.0, 0.0, 0.0], beta = 0.1, freq = 256):
        self.set_q(q0)
        self.set_beta(beta)
        self.set_freq(freq)
    
    def set_q(self, q):
        orig.q0 = q[0]
        orig.q1 = q[1]
        orig.q2 = q[2]
        orig.q3 = q[3]

    def set_beta(self, beta):
        orig.beta = beta
    
    def set_freq(self, freq):
        orig.sampleFreq = freq

    @cython.boundscheck(False)
    @cython.wraparound(False)  
    def _run_updates(self, np.ndarray[DTYPE_t, ndim=2] acc, 
                          np.ndarray[DTYPE_t, ndim=2] gyr, 
                          np.ndarray[DTYPE_t, ndim=2] mag ):
        """Efficiently run imu data arrays through the filter."""

        cdef int samples = acc.shape[0] # Number of steps

        cdef np.ndarray[DTYPE_t, ndim=2] Q = np.zeros((samples, 4), dtype=DTYPE)

        for s in range(samples):

            orig.MadgwickAHRSupdate(gyr[s,0], gyr[s,1], gyr[s,2], 
                acc[s,0], acc[s,1], acc[s,2], 
                mag[s,0], mag[s,1], mag[s,2])

            Q[s,0] = orig.q0
            Q[s,1] = orig.q1
            Q[s,2] = orig.q2
            Q[s,3] = orig.q3
        
        return Q

cdef class MadgwickOriginalSqrt(Base):
    """This is the original filter but without fast_inv_sqrt()."""

    def __init__(self, q0 = [1.0, 0.0, 0.0, 0.0], beta = 0.1, freq = 256):
        self.set_q(q0)
        self.set_beta(beta)
        self.set_freq(freq)
    
    def set_q(self, q):
        orig_sqrt.q0 = q[0]
        orig_sqrt.q1 = q[1]
        orig_sqrt.q2 = q[2]
        orig_sqrt.q3 = q[3]

    def set_beta(self, beta):
        orig_sqrt.beta = beta
    
    def set_freq(self, freq):
        orig_sqrt.sampleFreq = freq

    @cython.boundscheck(False)
    @cython.wraparound(False)  
    def _run_updates(self, np.ndarray[DTYPE_t, ndim=2] acc, 
                          np.ndarray[DTYPE_t, ndim=2] gyr, 
                          np.ndarray[DTYPE_t, ndim=2] mag ):
        """Efficiently run imu data arrays through the filter."""

        cdef int samples = acc.shape[0] # Number of steps

        cdef np.ndarray[DTYPE_t, ndim=2] Q = np.zeros((samples, 4), dtype=DTYPE)

        for s in range(samples):

            orig_sqrt.MadgwickAHRSupdate(gyr[s,0], gyr[s,1], gyr[s,2], 
                acc[s,0], acc[s,1], acc[s,2], 
                mag[s,0], mag[s,1], mag[s,2])

            Q[s,0] = orig_sqrt.q0
            Q[s,1] = orig_sqrt.q1
            Q[s,2] = orig_sqrt.q2
            Q[s,3] = orig_sqrt.q3
        
        return Q

cdef class MadgwickOriginalSqrtDouble(Base):
    """This is the original filter but without fast_inv_sqrt() and floats changed to doubles."""

    def __init__(self, q0 = [1.0, 0.0, 0.0, 0.0], beta = 0.1, freq = 256):
        self.set_q(q0)
        self.set_beta(beta)
        self.set_freq(freq)
    
    def set_q(self, q):
        orig_sqrt_d.q0 = q[0]
        orig_sqrt_d.q1 = q[1]
        orig_sqrt_d.q2 = q[2]
        orig_sqrt_d.q3 = q[3]

    def set_beta(self, beta):
        orig_sqrt_d.beta = beta
    
    def set_freq(self, freq):
        orig_sqrt_d.sampleFreq = freq

    @cython.boundscheck(False)
    @cython.wraparound(False)  
    def _run_updates(self, np.ndarray[DTYPE_t, ndim=2] acc, 
                          np.ndarray[DTYPE_t, ndim=2] gyr, 
                          np.ndarray[DTYPE_t, ndim=2] mag ):
        """Efficiently run imu data arrays through the filter."""

        cdef int samples = acc.shape[0] # Number of steps

        cdef np.ndarray[DTYPE_t, ndim=2] Q = np.zeros((samples, 4), dtype=DTYPE)

        for s in range(samples):

            orig_sqrt_d.MadgwickAHRSupdate(gyr[s,0], gyr[s,1], gyr[s,2], 
                acc[s,0], acc[s,1], acc[s,2], 
                mag[s,0], mag[s,1], mag[s,2])

            Q[s,0] = orig_sqrt_d.q0
            Q[s,1] = orig_sqrt_d.q1
            Q[s,2] = orig_sqrt_d.q2
            Q[s,3] = orig_sqrt_d.q3

        return Q

cdef class MadgwickFixed(Base):
    """Same as sqrt filter but with 2x fix applied."""

    def __init__(self, q0 = [1.0, 0.0, 0.0, 0.0], beta = 0.1, freq = 256):
        self.set_q(q0)
        self.set_beta(beta)
        self.set_freq(freq)
    
    def set_q(self, q):
        sqrt_fix.q0 = q[0]
        sqrt_fix.q1 = q[1]
        sqrt_fix.q2 = q[2]
        sqrt_fix.q3 = q[3]

    def set_beta(self, beta):
        sqrt_fix.beta = beta

    def set_freq(self, freq):
        sqrt_fix.sampleFreq = freq

    @cython.boundscheck(False)
    @cython.wraparound(False)  
    def _run_updates(self, np.ndarray[DTYPE_t, ndim=2] acc, 
                          np.ndarray[DTYPE_t, ndim=2] gyr, 
                          np.ndarray[DTYPE_t, ndim=2] mag ):
        """Efficiently run imu data arrays through the filter."""

        cdef int samples = acc.shape[0] # Number of steps

        cdef np.ndarray[DTYPE_t, ndim=2] Q = np.zeros((samples, 4), dtype=DTYPE)

        for s in range(samples):

            sqrt_fix.MadgwickAHRSupdate(gyr[s,0], gyr[s,1], gyr[s,2], 
                acc[s,0], acc[s,1], acc[s,2], 
                mag[s,0], mag[s,1], mag[s,2])

            Q[s,0] = sqrt_fix.q0
            Q[s,1] = sqrt_fix.q1
            Q[s,2] = sqrt_fix.q2
            Q[s,3] = sqrt_fix.q3
        
        return Q