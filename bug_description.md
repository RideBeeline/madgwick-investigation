# The Bugs and Fixes

## Bug 1, in the paper version: position of sensor normalisation
Around line 76 we find:
```C
  float twom_x = 2.0f * m_x;
  float twom_y = 2.0f * m_y;
  float twom_z = 2.0f * m_z;
```
But later, around line 86 we find:
```
  // normalise the magnetometer measurement
  norm = sqrt(m_x * m_x + m_y * m_y + m_z * m_z);
  m_x /= norm;
  m_y /= norm;
  m_z /= norm;
```
The problem is that the magnetometer values are used before they are normalised. The fix is simply to move the normalisation code above the assignment code.

## Bug 2, in the C version: *2 missing
Around line 100 of the AHRS update function we find
```C
_2bx = sqrt(hx * hx + hy * hy);
_2bz = -_2q0mx * q2 + _2q0my * q1 + mz * q0q0 + _2q1mx * q3 - mz * q1q1 + _2q2 * my * q3 - mz * q2q2 + mz * q3q3;
```

`_2bx` and `_2bz` refer to two components of the b vector from the paper, multiplied by 2. However, the multiplication seems to be missing and the right hand side of above's equations actually represent what would be `_bx` and `_bz`.
### Fix
`_2bx` and `_2bz` are only half what they ought to be. A fix is the equivalent of this:

```C
_bx = sqrt(hx * hx + hy * hy);
_bz = -_2q0mx * q2 + _2q0my * q1 + mz * q0q0 + _2q1mx * q3 - mz * q1q1 + _2q2 * my * q3 - mz * q2q2 + mz * q3q3;
_2bx = 2.0f * _bx;
_2bz = 2.0f * _bz;
```
