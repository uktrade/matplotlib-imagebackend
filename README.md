# matplotlib_imagebackend.

Matplotlib backend that outputs images to a folder.
=

Prerequisites:
==

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
==

| Environment variable          | Description                                                                                |
|-------------------------------|--------------------------------------------------------------------------------------------|
| MPL_IMAGEBACKEND_DIR          | Image output directory, defaults to current directory if not set.                          |
| MPL_IMAGEBACKEND_BACKEND      | Backend to delegate rendering to, if not set tries Agg and PyCairo in turn                 |
| MPL_IMAGEBACKEND_FEEDBACK_IO  | If set to domain socket, named pipe or filename reports each file generated.               |
| MPL_IMAGEBACKEND_FEEDBACK_KEY | Must be set if using MPL_IMAGEBACKEND_FEEDBACK to output to a domain socket or named pipe. |


Running:
==

First, verify matplotlib works by running the example matplotlib

`$ python3 example.py`

Run matplotlib with this backend:

`$ MPLBACKEND=module://matplotlib_imagebackend python3 example.py`

Output images to a directory named "output":

`$ MPLBACKEND=module://matplotlib_imagebackend MPL_IMAGEBACKEND_DIR=output python3 example.py`


Integration with IDEs and other tools:
==

matplot_imagebackend provides can use domain sockets (or named pipes) as a side channel to update IDEs 
as images are created, so they can display them live.



IDEs that wish to live display images should start a server and listen on domain socket / named pipe,
using the following naming conventioning:

IDEs wishing to display images as they are generated can listen on a domain socket / named pipe,
this scheme leaves all ports free for user programmes.


The recommended naming scheme for sockets incorporates the IDEs process number

`MPL_IMAGEBACKEND_FEEDBACK=ipc:///run/ide-sidechannel/mpl-12345`

Windows uses named pipes with a similar convention.

`MPL_IMAGEBACKEND_FEEDBACK=ipc:///namedpipe/ide-sidechannel-mpl-12345`
