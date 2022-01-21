"""
Matplotlib backend to output figures to a folder.

This wraps existing non interactive backends, and delegates to them to generate images.

By default images are saved in the current directory, but the user may set MPL_IMAGEBACKEND_DIR to
specify a new directory.

Specify a delegate backend by setting MPL_IMAGEBACKEND_BACKEND, e.g. MPL_IMAGEBACKEND_BACKEND=cairo
If this is not set then agg and cairo will be tried in sequence.

"""

import importlib
import os
import pathlib

from matplotlib.backend_bases import Gcf
from matplotlib import rcsetup

from matplotlib_imagebackend.ide_sidechannel import (
    get_runtime_directory,
    get_sidechannel_socket,
    send_image,
)

from .util import get_runtime_directory

MODULE_NAME = "matplotlib_imagebackend"
DEFAULT_BACKEND = "agg"
OUTPUT_DIRECTORY = os.environ.get("MPL_IMAGEBACKEND_DIR")
FORMAT = os.environ.get("MPL_IMAGEBACKEND_FORMAT", "svg")

# Map backend names to modules they import
BACKEND_MODULES = {"agg": "aggdraw", "cairo": "cairo"}


def get_default_backend():
    for backend_name, module in BACKEND_MODULES.items():
        try:
            __import__(module)
            return backend_name
        except ImportError:
            pass


def get_delegate_backend():
    """
    :return: the matplotlib backend to delegate to.

    Backends can be set by setting a name in an environment variable:
    `$ MPL_IMAGEBACKEND_BACKEND=agg`

    If this is not set then agg, cairo will be tried in turn.
    """
    backend_name = os.environ.get("MPL_IMAGEBACKEND_BACKEND")
    if not backend_name:
        backend_name = get_default_backend()
        if not backend_name:
            raise ValueError(
                f"MPL_IMAGEBACKEND_BACKEND not specified and could not import of the default backends: {BACKEND_MODULES.keys()}"
            )

    valid_backends = [
        name for name in rcsetup.non_interactive_bk if name != MODULE_NAME
    ]
    if backend_name not in valid_backends:
        raise ValueError(f"MPL_IMAGEBACKEND_BACKEND must be one of: {valid_backends}")

    rcsetup.validate_backend(backend_name)

    module = importlib.import_module(f"matplotlib.backends.backend_{backend_name}")
    FigureCanvas = getattr(module, f"FigureCanvas{backend_name.capitalize()}")
    return FigureCanvas


FigureCanvas = get_delegate_backend()


def show(*args, **kwargs):
    # TODO if user hasn't specified OUTPUT_DIRECTORY get runtime directory.
    sock = get_sidechannel_socket()
    output_dir = pathlib.Path(OUTPUT_DIRECTORY or get_runtime_directory())
    output_dir.mkdir(parents=True, exist_ok=True)

    for num, figure_manager in enumerate(Gcf.get_all_fig_managers()):
        output_image = str(output_dir / f"figure_{num}.{FORMAT}")
        figure_manager.canvas.figure.savefig(output_image)
        if sock:
            send_image(sock, output_image, FORMAT, matplotlib_figure=num)

    if sock:
        sock.close()
