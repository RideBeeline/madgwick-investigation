
cdef extern from "MadgwickAHRS_sqrt_fix/MadgwickAHRS_sq_fix.cpp":
    pass

cdef extern from "MadgwickAHRS_sqrt_fix/MadgwickAHRS_sq_fix.h" namespace "fixed_sqrt":
    float sampleFreq
    float beta
    float q0, q1, q2, q3

    void MadgwickAHRSupdate(float gx, float gy, float gz, float ax, float ay, float az, float mx, float my, float mz)
    void MadgwickAHRSupdateIMU(float gx, float gy, float gz, float ax, float ay, float az)

