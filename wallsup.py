"""
This is a simple script for the Gnome desktop environment that randomly picks an image
file from a directory tree and sets it as the wallpaper.
"""

import os
import subprocess as sp
import random
from urllib.request import pathname2url
from getpass import getuser
from syslog import LOG_INFO, syslog

# Change this to the top-level directory containing your wallpapers.
WALLPAPERS_PATH = f"/home/{getuser()}/Pictures/wallpapers"


def get_files_recursively(root_path):
    files_in_paths = ((root, files) for root, dirs, files in os.walk(root_path))
    return (f"{path}/{file}" for path, files in files_in_paths for file in files)


def file_has_extension(file, *extensions):
    has_dot = "." in file
    file_extension = file.rsplit(".", maxsplit=1)[-1].lower()
    return has_dot and file_extension in extensions


def set_wallpaper(wallpaper_path):
    url = f"file://{pathname2url(wallpaper_path)}"
    sp.run(f"gsettings set org.gnome.desktop.background picture-uri {url}".split())
    sp.run(f"gsettings set org.gnome.desktop.screensaver picture-uri {url}".split())


def log_message(message):
    syslog(LOG_INFO, message)


def main():
    files = get_files_recursively(WALLPAPERS_PATH)
    wallpaper_files = [file for file in files if file_has_extension(file, "jpg", "png")]
    random_wallpaper = random.choice(wallpaper_files)
    set_wallpaper(random_wallpaper)
    log_message(f"Wallpaper was set to: {random_wallpaper}")


if __name__ == "__main__":
    main()
