# Matlab based filter

The original filter, downloaded from the [x-io website](https://x-io.co.uk/open-source-imu-and-ahrs-algorithms/) and unpacked into `./madgwick_algorithm_matlab`.

Instead of writing python <-> matlab bindings you need to manually run the supplied scripts in Octave or Matlab.

## ExampleDataRun.m
Runs the ExampleData.mat supplied with the original algorithm and saves the IMU data as well as the quaternion outputs to `ExampleData.hdf5`.
