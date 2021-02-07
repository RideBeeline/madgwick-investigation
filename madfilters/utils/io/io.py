""" Module with useful functions for importing and exporting. """
import numpy as np
import h5py


def load_hdf5(filename, load_imu_data=False):
    """Loads a hdf5 data file produced by the Matlab / Octave scripts"""
    with h5py.File(filename, "r") as f:
        Q = f['Q']['value'][()].T
        beta = f['beta']['value'][()]
        frequency = f['frequency']['value'][()]

        if load_imu_data:
            time = f['time']['value'][()].T
            acc = f['acc']['value'][()].T
            gyr = f['gyr']['value'][()].T
            mag = f['mag']['value'][()].T

            return Q, beta, frequency, time, acc, gyr, mag

        else:
            return Q, beta, frequency
