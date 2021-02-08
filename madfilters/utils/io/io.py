""" Module with useful functions for importing and exporting. """
import pickle
import pathlib
import numpy as np
import h5py

import madfilters.mat as mat

_io_dir = pathlib.Path(__file__).parent.absolute()
sample_data_file = _io_dir / "data.pickle"

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


def import_from_matlab(beta, freq):
    """ Import quaternions from hdf5 file if beta and frequency match. """
    Q, mat_beta, mat_freq = load_hdf5(mat.output_data_filename)

    if beta != mat_beta:
        raise ValueError(
            "Matlab's beta does not match current beta. Run CustomDataRun.m script, then re-run!")

    if freq != mat_freq:
        raise ValueError(
            "Matlab's frequency does not match current frequency. Run CustomDataRun.m script, then re-run!")

    return Q

def export_to_matlab(acc, gyr, mag, q0, freq, beta):

    with h5py.File(mat.input_data_filename, "w") as f:
        dset_acc = f.create_dataset("acc", data=acc.T)
        dset_gyr = f.create_dataset("gyr", data=gyr.T)
        dset_mag = f.create_dataset("mag", data=mag.T)
        dset_q0 = f.create_dataset("q0", data=q0)
        dset_beta = f.create_dataset("beta", data=beta)
        dset_freq = f.create_dataset("frequency", data=freq)

def sync_with_matlab(pickle_file, acc, gyr, mag, q0, beta, freq):
    try:
        with open(pickle_file, 'rb') as f:
            obj = pickle.load(f)
            if obj['beta'] == beta and obj['freq'] == freq:
                return obj['Q']
    except (KeyError, FileNotFoundError) as err:
        pass

    try:
        Q = import_from_matlab(beta, freq)
    except ValueError as err:
        print("Outdate matlab file detected, exporting to matlab ...")
        export_to_matlab(acc, gyr, mag, q0, freq, beta)
        raise err

    # Store local copy of Q data
    obj = {
        'Q': Q,
        'beta': beta,
        'freq': freq
    }

    with open(pickle_file, 'wb') as f:
        pickle.dump(obj, f)

    return Q




def load_sample_data():
    """Loads the local imu data file. """
    with open(sample_data_file, 'rb') as f:
        obj = pickle.load(f)

    acc = np.array(obj['acc'], dtype=np.double)
    gyr = np.array(obj['gyr'], dtype=np.double)
    mag = np.array(obj['mag'], dtype=np.double)
    times = np.array(obj['times'], dtype=np.double)
    
    q0 = np.array(obj['q0'], dtype=np.double)
    freq = obj['frequency']
    
    return acc, gyr, mag, times, q0, freq
