"""
This is a simple script for the Gnome desktop environment that randomly picks an image
file from a directory tree and sets it as the wallpaper.
"""

import os
import random
import subprocess as sp
from getpass import getuser
from os.path import join
from pathlib import Path
from syslog import LOG_INFO, syslog
from urllib.request import pathname2url

# Change this to the top-level directory containing your wallpapers.
WALLPAPERS_PATH = f"/home/{getuser()}/Pictures/wallpapers"


def get_files_recursively(root_path):
    for current_path, dir_names, file_names in os.walk(root_path):
        for file_name in file_names:
            yield join(current_path, file_name)


def file_has_extension(file_path, *extensions):
    path = Path(file_path)
    return path.suffix in extensions


def set_wallpaper(wallpaper_path):
    url = f"file://{pathname2url(wallpaper_path)}"
    sp.run(f"gsettings set org.gnome.desktop.background picture-uri {url}".split())
    sp.run(f"gsettings set org.gnome.desktop.screensaver picture-uri {url}".split())


def log_message(message):
    syslog(LOG_INFO, message)


def main():
    files = get_files_recursively(WALLPAPERS_PATH)
    wallpaper_files = [
        file for file in files if file_has_extension(file, ".jpg", ".png")
    ]

    if len(wallpaper_files) == 0:
        return

    random_wallpaper = random.choice(wallpaper_files)
    set_wallpaper(random_wallpaper)
    log_message(f"Wallpaper was set to: {random_wallpaper}")


if __name__ == "__main__":
    main()
