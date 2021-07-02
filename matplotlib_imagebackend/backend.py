"""
Matplotlib backend to output figures to a folder.

This wraps existing non interactive backends, and delegates to them to generate images.

By default images are saved in the current directory, but the user may set MATPLOTLIB_IMAGEBACKEND_DIR to
specify a new directory.

Specify a delegate backend by setting MATPLOTLIB_IMAGEBACKEND_BACKEND, e.g. MATPLOTLIB_IMAGEBACKEND_BACKEND=cairo
If this is not set then agg and cairo will be tried in sequence.

"""

import importlib
import os
import pathlib

from matplotlib.backend_bases import Gcf
from matplotlib import rcsetup

MODULE_NAME = "matplotlib_imagebackend"
DEFAULT_BACKEND = "agg"
OUTPUT_DIRECTORY = os.environ.get("MATPLOTLIB_IMAGEBACKEND_DIR", ".")


def get_default_backend():
    for module, backend_name in [("aggdraw", "agg"), ("pycairo", "cairo")]:
        try:
            __import__(module)
            return backend_name
        except ImportError:
            pass


def get_delegate_backend():
    """
    :return: the matplotlib backend to delegate to.

    Backends can be set by setting a name in an environment variable:
    `$ MATPLOTLIB_IMAGEBACKEND_BACKEND=agg`

    If this is not set then agg, cairo will be tried in turn.
    """
    backend_name = os.environ.get("MATPLOTLIB_IMAGEBACKEND_BACKEND")
    if not backend_name:
        backend_name = get_default_backend()

    valid_backends = [
        name for name in rcsetup.non_interactive_bk if name != MODULE_NAME
    ]
    if backend_name not in valid_backends:
        raise ValueError(
            f"MATPLOTLIB_IMAGEBACKEND_BACKEND must be one of: {valid_backends}"
        )

    rcsetup.validate_backend(backend_name)

    module = importlib.import_module(f"matplotlib.backends.backend_{backend_name}")
    FigureCanvas = getattr(module, f"FigureCanvas{backend_name.capitalize()}")
    return FigureCanvas


FigureCanvas = get_delegate_backend()


def show(*args, **kwargs):
    output_dir = pathlib.Path(OUTPUT_DIRECTORY)
    output_dir.mkdir(parents=True, exist_ok=True)

    for num, figmanager in enumerate(Gcf.get_all_fig_managers()):
        figmanager.canvas.figure.savefig(output_dir / f"figure_{num}.png")
