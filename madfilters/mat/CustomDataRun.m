% CustomDataRun.m
%
% This script loads data from input_data.hdf5 and parses it
% through the filter. It then exports the resulting quaternions,
% and the used beta and frequency to an hdf5 file so it can be easily imported
% in Python.

addpath('madgwick_algorithm_matlab/@MadgwickAHRS', 'madgwick_algorithm_matlab/quaternion_library'); 

clear;

load input_data.hdf5;

AHRS = MadgwickAHRS('SamplePeriod', 1/frequency, 'Beta', beta, 'Quaternion', q0);


Q = zeros(length(acc), 4);
for t = 1:length(acc)
    AHRS.Update(gyr(t,:), acc(t,:), mag(t,:));
    Q(t, :) = AHRS.Quaternion;
end

save output_data.hdf5 Q beta frequency -hdf5;
