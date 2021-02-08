
"""Runs the setup.py with build_ext -i in all specified sub directories.

Makes it easy to build all the cypthon packages.
"""

import subprocess
from setuptools import setup, find_packages

directories = ["madgwick_originals", "madgwick_paper"]

for directory in directories:
    print(f"\nStarting setup.py build in ./{directory} ...\n")
    p = subprocess.Popen(["python", "setup.py","build_ext", "-i"], cwd=directory)
    p.wait()
