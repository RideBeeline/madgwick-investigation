# C / Cpp based filters


## Madgwick Original, largly unmodified.
`madgwick_originals/MadgwickAHRS/MadgwickAHRS.cpp`

The original filter, downloaded from the [x-io website](https://x-io.co.uk/open-source-imu-and-ahrs-algorithms/) and unpacked into `./madgwick_originals/MadgwickAHRS`.

Endings changed to .cpp for easier Cython integration and added ability to change the sampling frequency but otherwise unmodified.

## Madgwick Oiginal, 1/sqrt()
`madgwick_originals/MadgwickAHRS_sqrt/MadgwickAHRS_sqrt.cpp`

Same as above but with fast_inv_sqrt() now using math::sqrtf().

## Madgwick Oiginal, 1/sqrt() and double
`madgwick_originals/MadgwickAHRS_sqrt_d/MadgwickAHRS_sqrt_d.cpp`

Same as above, with fast_inv_sqrt() now using math::sqrt() and all floats changed to doubles.

## Madgwick Oiginal, 1/sqrt() and 2x bug fix applied

`madgwick_originals/MadgwickAHRS_sqrt_fix/MadgwickAHRS_sqrt_fix.cpp`

```C
    _2bx = sqrt(hx * hx + hy * hy);
    _2bz = -_2q0mx * q2 + _2q0my * q1 + mz * q0q0 + _2q1mx * q3 - mz * q1q1 + _2q2 * my * q3 - mz * q2q2 + mz * q3q3;
    _2bx *= 2.0f; // Added *2 Fix
    _2bz *= 2.0f; // Added *2 Fix
    _4bx = 2.0f * _2bx;
    _4bz = 2.0f * _2bz;
```

## Madgwick Paper
`madgwick_paper/src/MadgwickPaper.cpp`
The c code copied from the appending of the original report.

## Adafruit AHRS
`Adafruit_AHRS/src/Adafruit_AHRS_Madgwick.cpp`
Adafruit's library from their [github](https://github.com/adafruit/Adafruit_AHRS/blob/master/src/Adafruit_AHRS_Madgwick.h)

Small change to make members public, makes it possible to set q0.

## Arduino Madgwick
`Adafruit_AHRS/src/Adafruit_AHRS_Madgwick.cpp`
Arduino's library from their [github](https://github.com/arduino-libraries/MadgwickAHRS)

Turns out is just the same code as Adafruit's, same small change to make members public.

## Installation

You have to be in the `cpp` directory before running `setup.py`. Like so:

```
cd madfilters/cpp
python setup.py
```