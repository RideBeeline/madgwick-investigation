
"Original, completely unmodified madgwick library interface"

cdef extern from "MadgwickAHRS/MadgwickAHRS.cpp":
    pass

cdef extern from "MadgwickAHRS/MadgwickAHRS.h":
    float beta
    float q0, q1, q2, q3

    void MadgwickAHRSupdate(float gx, float gy, float gz, float ax, float ay, float az, float mx, float my, float mz)
    void MadgwickAHRSupdateIMU(float gx, float gy, float gz, float ax, float ay, float az)

