# Madgwick's Filter Implementation Analysis
Exploring how implementations differ, mainly focusing on a bug in the widely used C version of the filter.

## Summary
Madgwick's AHRS algorithm for orientation sensor fusion is a well regarded filter to fuse IMU / MARG sensor data to estimate the sensor's orientation with respect to the earth frame. It is widely used due to its efficiency, stability, and being open source. 

However, the C implementation has a bug that results in non-optimal fusion when using the full MARG filter. Specifically, the C version does not agree with the mathematics of the paper or the Matlab implementation, as well as open source pythen implementations that seem to be based on the Matlab implementation.

## Motivation
Todo

## Implementations and Bugs
There are actually two different, unrelated bugs. 

### Paper version
The first, and less important bug is in the code from the paper describing the filter and is due to where the magnetomer readings are normalised. So it would not be noticable when calling the function with already normalised data. We can only assume this is why it made it into the paper. 

This implementation is not very optimised and doesn't appear to be widely used. It is refered here as the "paper version" and is written in C.

### C version
The second, more important bug is in the distributed C code. A missing *2 for a magnetomer readings causes the filter to behave slightly differently during an AHRS update. The effect of the bug is not constant and it appears that one can compensate for it to some extend by choosing a different Beta. Still, it would be surprising if we were the first to discover it.

This implementation is optimised and code based on it is widely used. I expect most versions based on it have the same issue. It is refered here as the "C version".

### Code
The code describing the bugs and fixes is [here](./bug_description.md).

## Proof
The simple test of putting the same data in and getting different quaternion results out is shown in [Experiment 1](./experiment_1_mat_vs_c_org_data/README.md) and [Experiment 2](./experiment_2_mat_vs_c_short_data/README.md). Furthermore, applying the fix to the C implementations causes the outputs to agree with the Matlab version: [Experiment 4](./experiment_4_mat_vs_c_vs_paper/README.md).

## Implementations Tested
| Implementation                 | x2 Bug | norm Bug | no Bug |
|--------------------------------|:------:|:--------:|:------:|
| Matlab from x-io               |        |          |    x   |
| Python from ahrs package       |        |          |    x   |
| Python, translated from Matlab |        |          |    x   |
| C code from x-io               |   x    |          |        |
| Adafruit's Implementation      |   x    |          |        |
| Arduino's Implementation       |   x    |          |        |
| C code from Paper              |        |     x    |        |
| C code from Paper, with fix    |        |          |    x   |
| C code from x-io, with 1/sqrt()|   x    |          |        |
| C code from x-io, with fix     |        |          |    x   |

## Impact
The bug only effects the transient, dynamic response. However, if the compensation involves the choice of a different, non-optimum Beta value, the static performance may also be impacted. The size of the impact varies. It seems to depend on the orientation, sampling frequency, and chosen Beta. For example, in our testing, the bug was not detactable when moving the sensor flat around its yaw axis only.

## Compensating with Beta
 [Experiment 7](./experiment_7_beta_fix/README.md) attempts to make a filter with the x2 Bug behave as if it didn't have it by selecting an optimum value of Beta. This can mostly compensate for the bug in the test case but not fully. It is also not clear if that compensation works with different orientations, sample rates, noise, and selected reference Beta as it just optimises for the short test data. The chosen Beta is 5 times larger than the one used in the reference filter without the bug. Repeating the test with different data at a different frequency resulted in an optimum beta that was only ~2 times the original. More tests are needed.

## Analysis
Todo