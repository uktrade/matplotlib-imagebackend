import pathlib
import platform
import os


RUNTIME_DIRECTORIES = {
    "Darwin": ("/tmp",),
    "Linux": ("${XDG_RUNTIME_DIR}", "/run", "/var/run", "/tmp"),
    "Windows": ("%TEMP%",),
}


def get_runtime_directory():
    paths = RUNTIME_DIRECTORIES.get(platform.system())
    for p in paths or []:
        expanded_path = pathlib.Path(os.path.expandvars(p))
        if expanded_path.is_dir():
            return expanded_path
    return Path(".")
