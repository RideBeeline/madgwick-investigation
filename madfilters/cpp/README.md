# C / Cpp based filters


## Madgwick Original, largly unmodified.
`madgwick_originals/MadgwickAHRS/MadgwickAHRS.cpp`

The original filter, downloaded from the [x-io website](https://x-io.co.uk/open-source-imu-and-ahrs-algorithms/) and unpacked into `./madgwick_originals/MadgwickAHRS`.

Endings changed to .cpp for easier Cython integration and added ability to change the sampling frequency but otherwise unmodified.

## Madgwick Oiginal, 1/sqrt()
`madgwick_originals/MadgwickAHRS_sqrt/MadgwickAHRS_sqrt.cpp`

Same as above but with fast_inv_sqrt() now using math::sqrtf().

## Madgwick Oiginal, 1/sqrt() and double
`madgwick_originals/MadgwickAHRS_sqrt/MadgwickAHRS_sqrt.cpp`

Same as above, with fast_inv_sqrt() now using math::sqrt() and all floats changed to doubles.

## Madgwick Paper
`madgwick_paper/src/MadgwickPaper.cpp`
The c code copied from the appending of the original report.

## Installation

You have to be in the `cpp` directory before running `setup.py`. Like so:

```
cd madfilters/cpp
python setup.py
```