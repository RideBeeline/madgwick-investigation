# Implementations

This is a list of filter implementations found within this package.
***
# C / Cpp based Implementations


## Madgwick Original, largly unmodified.
[Source File](./cpp/madgwick_originals/MadgwickAHRS/MadgwickAHRS.cpp): `cpp/madgwick_originals/MadgwickAHRS/MadgwickAHRS.cpp` 

The original filter, downloaded from the [x-io website](https://x-io.co.uk/open-source-imu-and-ahrs-algorithms/) on 07/02/2021

Endings changed to .cpp for easier integration with *Cython* and added ability to change the sampling frequency but otherwise unmodified.

## Madgwick, fast_inv_sqrt -> 1/sqrt()
[Source File](./cpp/madgwick_originals/MadgwickAHRS_sqrt/MadgwickAHRS_sq.cpp): `cpp/madgwick_originals/MadgwickAHRS_sqrt/MadgwickAHRS_sq.cpp`

Same as the above but with fast_inv_sqrt() now using math::sqrtf(). Also added a namespace so all the madgwick implementations can be part of the same cython package.

## Madgwick, 1/sqrt() and float -> double
[Source File](./cpp/madgwick_originals/MadgwickAHRS_sqrt_d/MadgwickAHRS_sq_d.cpp):  `cpp/madgwick_originals/MadgwickAHRS_sqrt_d/MadgwickAHRS_sq_d.cpp`

Same as above, but all floats changed to doubles.

## Madgwick,, 1/sqrt() and *2 bug fix 

[Source File](./cpp/madgwick_originals/MadgwickAHRS_sqrt_fix/MadgwickAHRS_sq_fix.cpp): `cpp/madgwick_originals/MadgwickAHRS_sqrt_fix/MadgwickAHRS_sq_fix.cpp`

Same as the original + 1/sqrt() and the following change to fix the *2 bug
```C
_2bx = sqrt(hx * hx + hy * hy);
_2bz = -_2q0mx * q2 + _2q0my * q1 + mz + ...; // Truncated for brevity
_2bx *= 2.0f; // Added *2 Fix
_2bz *= 2.0f; // Added *2 Fix
_4bx = 2.0f * _2bx;
_4bz = 2.0f * _2bz;
```

*** 

## Madgwick Paper
[Source File](./cpp/madgwick_paper/src_original/MadgwickPaper.cpp): `cpp/madgwick_paper/src_original/MadgwickPaper.cpp`
The C code copied from the appendix of the [internal_report](http://x-io.co.uk/res/doc/madgwick_internal_report.pdf) on 07/02/2021. 

Changed to Cpp to support namespaces and added one, added `deltat`, `beta`, `zeta` as modifiable parameters instead of constants. Also created a header file for it.

## Madgwick Paper + Normalisation Bug Fix
[Source File](./cpp/madgwick_paper/src_norm_fix/MadgwickPaper_norm_fix.cpp): `cpp/madgwick_paper/src_norm_fix/MadgwickPaper_norm_fix.cpp` 

Same as above but with the normalisation code for acceration and magnetic field samples moved towards the top of the update function, before their results are used.

## Madgwick Paper + Norm Fix + No gyro compensation
[Source File](./cpp/madgwick_paper/src_nocomp/MadgwickPaper_nocomp.cpp): `cpp/madgwick_paper/src_nocomp/MadgwickPaper_nocomp.cpp` 

Same as above but with the gyro compensation disabled. This actually makes no difference when zeta set to 0 so is pointless.

***

## Adafruit AHRS
[Source File](./cpp/Adafruit_AHRS/src/Adafruit_AHRS_Madgwick.cpp): `cpp/Adafruit_AHRS/src/Adafruit_AHRS_Madgwick.cpp`

Adafruit's library from their [github](https://github.com/adafruit/Adafruit_AHRS/blob/master/src/Adafruit_AHRS_Madgwick.h), downloaded on 08/02/2020.

Small change to make members public, makes it possible to set q0 and others.

## Arduino Madgwick
[Source File](./cpp/ArduinoMadgwickAHRS/src/MadgwickAHRS.cpp): `cpp/ArduinoMadgwickAHRS/src/MadgwickAHRS.cpp`

Arduino's library from their [github](https://github.com/arduino-libraries/MadgwickAHRS)

Turns out it is very similar code to Adafruit's library, same small change to make members public.

## Installation

You have to be in the `cpp` directory before running `setup.py`. Like so:

```
cd madfilters/cpp
python setup.py
```

# Python Implementations

## AHRS
`py/ahrs_madgwick/ahrs_wrapper.py` 

Just a wrapper around the pip installed `ahrs` package from:
https://pypi.org/project/AHRS/

## Matlab Clone
[Source File](./py/matlab_clone/matlab_clone.py): `py/matlab_clone/matlab_clone.py`

Ported Madgwick's Matlab code to Python with as few changes as possible. All changes commented at the top of the file.

# Matlab Implementations
## Madgwick's Matlab Code
[Source File](./mat/madgwick_algorithm_matlab): `mat/madgwick_algorithm_matlab` 

The original filter, downloaded from the [x-io website](https://x-io.co.uk/open-source-imu-and-ahrs-algorithms/) on 07/02/2021

The code is unchanged with wrapper functions added on top of it. There is only loose integration with Python which involves HDF5 files to transfer data between Python and Matlab / Octave. For example, to run custom imu data through the Matlab filter:
 1. The python `utils.io.sync_with_matlab()`, called with the imu data checks if Matlab code needs to run and if so will create a hdf5 "input file" `input_data.hdf5`
 2. In Matlab / Octave, running `CustomDataRun.m` reads the input data, runs it through the filter, and outputs the quaternions into `output_data.hdf5`
 3. On the next run of the script, `sync_with_matlab()` reads the hdf5 file, saves the content in a local *pickle* cache and returns the quaternion. 