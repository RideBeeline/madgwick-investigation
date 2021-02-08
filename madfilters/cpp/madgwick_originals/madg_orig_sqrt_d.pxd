
cdef extern from "MadgwickAHRS_sqrt_d/MadgwickAHRS_sq_d.cpp":
    pass

cdef extern from "MadgwickAHRS_sqrt_d/MadgwickAHRS_sq_d.h" namespace "original_sqrt_double":
    double sampleFreq
    double beta
    double q0, q1, q2, q3

    void MadgwickAHRSupdate(double gx, double gy, double gz, double ax, double ay, double az, double mx, double my, double mz)
    void MadgwickAHRSupdateIMU(double gx, double gy, double gz, double ax, double ay, double az)

