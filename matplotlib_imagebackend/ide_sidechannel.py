import base64
import enum
import json
import os
import socket
import sys

from .util import get_runtime_directory

SOCKET_FILE = os.environ.get("MPL_IMAGEBACKEND_FEEDBACK_IO")
KEY = os.environ.get("MPL_IMAGEBACKEND_FEEDBACK_KEY")
MIMETYPES = {"svg": b"image/svg+xml", "png": b"image/png"}


def get_sidechannel_socket():
    if not SOCKET_FILE:
        return

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SOCKET_FILE)
    return sock


def encode_image(filename, format="png"):
    mimetype = MIMETYPES.get(format)
    if not mimetype:
        raise ArgumentError(f"Image format must be one of {MIMETYPES.keys()}")
    with open(filename, "rb") as f:
        encoded = base64.b64encode(f.read())
        return (b"data:" + mimetype + b";base64," + encoded).decode("ascii")


def send_image(sock, filename, format, **kwargs):
    """
    Send image encoded as base64
    """
    # TODO For apps that can share a directory it may be possible to share the file url directly.
    # TODO add info about what generated the file, time and process.
    # TODO should have messages + channels to make things more generic.
    # TODO file transfer can be via directory (decided by the channel) or base64 - may need negotiation.
    # TODO think about how matplotlib + figures fit in - is this metadata.
    data = {
        "key": KEY,
        "type": "image",
        "image": {
            "url": encode_image(filename, format),
        },
        "command": {
            "commandline": list(sys.argv),
            "cwd": os.getcwd(),
            "pid": os.getpid(),
        },
        "creator": "matplotlib_imagebackend",
        "dialect": "ide_sidechannel",
    }

    if kwargs:
        data["extra_data"] = kwargs

    # Encode data as newline delimited json and send.
    encoded_data = bytes(json.dumps(data).replace("\n", ""), encoding="utf-8") + b"\n"
    sock.send(encoded_data)
