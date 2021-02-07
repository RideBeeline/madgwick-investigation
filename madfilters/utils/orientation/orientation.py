"""Useful functions for orientation calculations. """
import numpy as np

def q_to_euler_zyx_z(Q):
    """ Calculate Euler Angle Psi (rotation around z axis) for ZYX sequence. """
    x1 = 2 * Q[:, 1] * Q[:, 2] - 2 * Q[:, 0] * Q[:, 3]

    x2=2 * Q[:, 0]**2 + 2 * Q[:, 1]**2 - 1

    z=np.arctan2(x1, x2)

    return np.rad2deg(z)

def q_to_euler_zxy_z(Q):
    """ Calculate Euler Angle  Psi (rotation around z axis) for ZXY sequence. """
    x1=2 * Q[:, 0] * Q[:, 3] - 2 * Q[:, 1] * Q[:, 2]
    x2=2 * Q[:, 0] * Q[:, 0] + 2 * Q[:, 2] * Q[:, 2] - 1

    z=np.arctan2(x1, x2)

    return np.rad2deg(z)

def q_to_aero_yaw(Q):
    """ Yaw in aerospace is just psi for ZYX sequence."""
    return q_to_euler_zyx_z(Q)
