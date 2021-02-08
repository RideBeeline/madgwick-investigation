# Straight translation from Magdwick's Matlab code

import numpy as np

# Changed function definition
# removed ;
# Changed % comments to #
# Changed (4)->[3], (3)->2, (2)->[1], (1)->[0]
# Changed (:,4)->[3], (:,3)->[2], (:,2)->[1], (:,1) -> [0]
# Changed (J'*F) -> J.T @ F
# add return statements
# add zero initializers (eg ab = np.zeros[4])
# added , and [] to array definitions
# added npa() around array definitions to turn them into np.ndarray
# changed obj.SamplePeriod and obj.Beta to SamplePeriod and Beta
# changed ].* -> ]*
# Fix if statements
# [0, Magnetometer] -> np.insert(Magnetometer, 0, 0)
# ^ -> **
norm = np.linalg.norm
npa = np.array


def quaternProd(a, b):

    ab = np.zeros(4)

    ab[0] = a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3]
    ab[1] = a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2]
    ab[2] = a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1]
    ab[3] = a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0]

    return ab


def quaternConj(q):
    qConj = npa( [q[0], -q[1], -q[2], -q[3]])
    return qConj

def Update(q, Gyroscope, Accelerometer, Magnetometer, Beta = 0.1, SamplePeriod = 1/512):
    # Normalise accelerometer measurement
    if (norm(Accelerometer) == 0):
        return q   # handle NaN

    Accelerometer = Accelerometer / norm(Accelerometer);	# normalise magnitude

    # Normalise magnetometer measurement
    if (norm(Magnetometer) == 0): 
        return q   # handle NaN

    Magnetometer = Magnetometer / norm(Magnetometer);	# normalise magnitude

        # Reference direction of Earth's magnetic feild
    h = quaternProd(q, quaternProd(np.insert(Magnetometer, 0, 0), quaternConj(q)))
    b = [0, norm([h[1], h[2]]), 0, h[3]]

    # Gradient decent algorithm corrective step
    F = npa([2*(q[1]*q[3] - q[0]*q[2]) - Accelerometer[0],
        2*(q[0]*q[1] + q[2]*q[3]) - Accelerometer[1],
        2*(0.5 - q[1]**2 - q[2]**2) - Accelerometer[2],
        2*b[1]*(0.5 - q[2]**2 - q[3]**2) + 2*b[3]*(q[1]*q[3] - q[0]*q[2]) - Magnetometer[0],
        2*b[1]*(q[1]*q[2] - q[0]*q[3]) + 2*b[3]*(q[0]*q[1] + q[2]*q[3]) - Magnetometer[1],
        2*b[1]*(q[0]*q[2] + q[1]*q[3]) + 2*b[3]*(0.5 - q[1]**2 - q[2]**2) - Magnetometer[2]])

    J = npa([[-2*q[2],                 	2*q[3],                    -2*q[0],                         2*q[1]],
        [2*q[1],                 	2*q[0],                    	2*q[3],                         2*q[2]],
        [0,                         -4*q[1],                    -4*q[2],                         0],
        [-2*b[3]*q[2],               2*b[3]*q[3],               -4*b[1]*q[2]-2*b[3]*q[0],       -4*b[1]*q[3]+2*b[3]*q[1]],
        [-2*b[1]*q[3]+2*b[3]*q[1],	2*b[1]*q[2]+2*b[3]*q[0],	2*b[1]*q[1]+2*b[3]*q[3],       -2*b[1]*q[0]+2*b[3]*q[2]],
        [2*b[1]*q[2],                2*b[1]*q[3]-4*b[3]*q[1],	2*b[1]*q[0]-4*b[3]*q[2],        2*b[1]*q[1]]])
    step = J.T @ F
    step = step / norm(step)	# normalise step magnitude

    # Compute rate of change of quaternion
    qDot = 0.5 * quaternProd(q, npa([0, Gyroscope[0], Gyroscope[1], Gyroscope[2]])) - Beta * step.T

    # Integrate to yield quaternion
    q = q + qDot * SamplePeriod
    quat = q / norm(q) # normalise quaternion
    return quat

def UpdateIMU(q, Gyroscope, Accelerometer, Beta = 0.1, SamplePeriod = 1/512):

    # # Normalise accelerometer measurement
    # if(norm(Accelerometer) == 0):
    #     return q	# handle NaN

    # Accelerometer = Accelerometer / norm(Accelerometer)	# normalise magnitude

    # # Gradient decent algorithm corrective step
    # F = [2*(q[1]*q[3] - q[0]*q[2]) - Accelerometer[0]
    #     2*(q[0]*q[1] + q[2]*q[3]) - Accelerometer[1]
    #     2*(0.5 - q[1]**2 - q[2]**2) - Accelerometer[2]]
    # J = [-2*q[2],	2*q[3],    -2*q[0],	2*q[1]
    #     2*q[1],     2*q[0],     2*q[3],	2*q[2]
    #     0,         -4*q[1],    -4*q[2],	0    ]
    # step = J.T @ F
    # step = step / norm(step)	# normalise step magnitude

    # # Compute rate of change of quaternion
    # qDot = 0.5 * quaternProd(q, [0 Gyroscope[0] Gyroscope[1] Gyroscope[2]]) - Beta * step'

    # # Integrate to yield quaternion
    # q = q + qDot * SamplePeriod
    quat = q / norm(q) # normalise quaternion
    return quat