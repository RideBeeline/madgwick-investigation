"""Useful functions for orientation calculations. """
import numpy as np


def q_to_euler_zyx_z(Q):
    """ Calculate Euler Angle Psi (rotation around z axis) for ZYX sequence. """
    x1 = 2 * Q[:, 1] * Q[:, 2] - 2 * Q[:, 0] * Q[:, 3]

    x2 = 2 * Q[:, 0]**2 + 2 * Q[:, 1]**2 - 1

    z = np.arctan2(x1, x2)

    return np.rad2deg(z)


def q_to_euler_zxy_z(Q):
    """ Calculate Euler Angle  Psi (rotation around z axis) for ZXY sequence. """
    x1 = 2 * Q[:, 0] * Q[:, 3] - 2 * Q[:, 1] * Q[:, 2]
    x2 = 2 * Q[:, 0] * Q[:, 0] + 2 * Q[:, 2] * Q[:, 2] - 1

    z = np.arctan2(x1, x2)

    return np.rad2deg(z)


def q_to_aero_yaw(Q):
    """ Yaw in aerospace is just psi for ZYX sequence."""
    return q_to_euler_zyx_z(Q)

def q_to_euler_zyx(Q):
    """Calculate all euler rotations for a ZYX sequence."""
    R_00 = 2 * Q[:, 0]**2-1+2*Q[:, 1]**2
    R_10 = 2 * (Q[:, 1]*Q[:, 2]-Q[:, 0]*Q[:, 3])
    R_20 = 2 * (Q[:, 1]*Q[:, 3]+Q[:, 0]*Q[:, 2])
    R_21 = 2 * (Q[:, 2]*Q[:, 3]-Q[:, 0]*Q[:, 1])
    R_22 = 2 * Q[:, 0]**2-1+2*Q[:, 3]**2

    phi = np.arctan2(R_21, R_22)
    theta = -np.arctan(R_20 / np.sqrt(1-R_20**2))
    psi = np.arctan2(R_10, R_00)

    phi = np.rad2deg(phi)
    theta = np.rad2deg(theta)
    psi = np.rad2deg(psi)
    
    return phi, theta, psi


def q_conj(Q):
    return Q*np.array([1.0, -1.0, -1.0, -1.0])


def q_dot(A, B):
    """Row wise dot product of two numpy arrays.

    See https://stackoverflow.com/questions/26168363/elegant-expression-for-row-wise-dot-product-of-two-matrices/26168677
    """
    return np.einsum('ij, ij->i', A, B)

def q_prod(A, B):
    """Quaternion product"""
    AB = np.zeros_like(A)
    AB[:,0] = A[:,0] *B[:,0]-A[:,1] *B[:,1]-A[:,2] *B[:,2]-A[:,3] *B[:,3]
    AB[:,1] = A[:,0] *B[:,1]+A[:,1] *B[:,0]+A[:,2] *B[:,3]-A[:,3] *B[:,2]
    AB[:,2] = A[:,0] *B[:,2]-A[:,1] *B[:,3]+A[:,2] *B[:,0]+A[:,3] *B[:,1]
    AB[:,3] = A[:,0] *B[:,3]+A[:,1] *B[:,2]-A[:,2] *B[:,1]+A[:,3] *B[:,0]

    return AB

def q_angle_diff(A, B):
    """Calculate the smallest angle between two quaternions.
    
    See https://uk.mathworks.com/matlabcentral/answers/415936-angle-between-2-quaternions 
    """
    A = A / np.linalg.norm(A, axis=1, keepdims=True)
    B = B / np.linalg.norm(B, axis=1, keepdims=True)
    QAB = q_prod(q_conj(A), B) # quaternion from A->B

    angle = 2 * np.arccos(QAB[:,0])

    return np.rad2deg(angle)

def q_angle_diff_2(A, B):
    """ This also works, seems easier! """
    A = A / np.linalg.norm(A, axis=1, keepdims=True)
    B = B / np.linalg.norm(B, axis=1, keepdims=True)
    cos_omega = q_dot(A, B)
    omega = 2 * np.arccos(cos_omega)
    return np.rad2deg(omega)
    





