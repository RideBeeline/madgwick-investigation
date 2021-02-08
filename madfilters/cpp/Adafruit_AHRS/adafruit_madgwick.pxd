
cdef extern from "src/Adafruit_AHRS_Madgwick.cpp":
    pass

cdef extern from "src/Adafruit_AHRS_Madgwick.h":
    cdef cppclass Adafruit_Madgwick:
        Adafruit_Madgwick() except +

        float beta
        float q0
        float q1
        float q2
        float q3 
        float invSampleFreq
        void update(float gx, float gy, float gz, float ax, float ay, float az, float mx, float my, float mz)
        void updateIMU(float gx, float gy, float gz, float ax, float ay, float az)