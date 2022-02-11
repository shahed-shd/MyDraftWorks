Dependency psutil can be installed via pip, like:
pip install psutil

To run, simply run the main.py file, like:
python main.py

You can pass optional network interface name.
If passed, then network I/O speed will be logged only for that interface,
otherwise for all network interface system wide.
Example:
python main.py en0

N.B.: The python binary of version 3 and compatible pip binary may be named as python3 & pip3 in your system.

The logs will be printed:
    - in console, having a compact format
    - in files in 'logs' directory, having a verbose format