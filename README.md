# matplotlib_imagebackend.

Matplotlib backend that outputs images to a folder.

Prerequisites:

You will need a python environment with matplotlib installed, along with the libraries needed to run one of it's noninteractive backends, e.g. Agg or Cairo:

For Agg:

`$ pip3 install aggdraw`

For Cairo:

`$ pip3 install pycairo`

Install:

Clone the github repo.

In a python environment that already has matplotlib installed, run:

`$ pip3 install .`


Environment variables:

By default images are saved in the current directory, the user may set an environment variable MATPLOTLIB_IMAGEBACKEND_DIR 
to specify a different new directory.

matplotlib_imagebackend will delegate to a backend specified by MATPLOTLIB_IMAGEBACKEND_BACKEND if it is set, e.g. MATPLOTLIB_IMAGEBACKEND_BACKEND=cairo
if this is not set then agg and cairo will be tried in sequence.


Running:

First, verify matplotlib works by running your a matplotlib file as normal.

`$ python3 example.py`

Run matplotlib with this backend:

`$ MPLBACKEND=module://matplotlib_imagebackend python3 example.py`

Output images to a directory named "output":

`$ MPLBACKEND=module://matplotlib_imagebackend MATPLOTLIB_IMAGEBACKEND_DIR=output python3 example.py`

