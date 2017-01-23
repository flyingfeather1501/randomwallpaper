#!/usr/bin/env python
"""Sets a random wallpaper, able to set how long an image should stay."""
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>


# Initialize
import time
import subprocess
import argparse
import sys
import os
import random

# Default values
wp_handler_list = [
    "mate", "gnome",
    "xfce", "pcmanfm",
    "pcmanfm-qt", "cinnamon",
    "feh", "deepin"]
wp_dir = subprocess.check_output(
    ["xdg-user-dir PICTURES"],
    shell=True).decode("utf8").rstrip() + "/Wallpapers"
# implement config file later
# cfg_path = subprocess.check_output(
#    ["xdg-user-dir HOME"],
#    shell=True).decode("utf8").rstrip() + ".rwp.cfg"

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--time",
                    help='global sleep time, in seconds',
                    default=60,
                    dest='sleep_time_global',
                    type=float)
parser.add_argument("-d", "--directory",
                    help='wallpaper directory, default:Pictures/Wallpapers',
                    default=wp_dir)
parser.add_argument("-s", "--sleep-first",
                    help='sleep before wallpaper change',
                    action='store_true')
# parser.add_argument("-c", "--config-file",
#                     help='specify how long to sleep for individual images\
#                     using a config file')
parser.add_argument("-w", "--wallpaper-handler",
                    help='specify the wallpaper handler to use',
                    action='append',
                    dest='wp_handler',
                    choices=wp_handler_list)
parser.add_argument("-v", "--verbose",
                    help='be verbose',
                    action='store_true')
args = parser.parse_args()
print(args.directory)


def desktop_detect():
    """Detect current desktop environment and return it."""
    if sys.platform in ["win32", "cygwin"]:
        return "windows"
    elif sys.platform == "darwin":
        return "macosx"
    else:
        DESKTOP_SESSION = os.environ.get("DESKTOP_SESSION")
        GDMSESSION = os.environ.get("GDMSESSION")
        if DESKTOP_SESSION is None:
            return "unknown"
        DESKTOP_SESSION = DESKTOP_SESSION.lower()
        XDG_CURRENT_DESKTOP = os.environ.get("XDG_CURRENT_DESKTOP").lower()
        MIR_SERVER_NAME = os.environ.get("MIR_SERVER_NAME")
        if XDG_CURRENT_DESKTOP == "gnome":
            if GDMSESSION == "cinnamon":
                return GDMSESSION
            else:
                return XDG_CURRENT_DESKTOP
        elif XDG_CURRENT_DESKTOP == "x-cinnamon":
            return "cinnamon"
        elif XDG_CURRENT_DESKTOP == "Unity":
            if MIR_SERVER_NAME is None:
                return "unity"
            else:
                return "unity_mir"
        else:
            return XDG_CURRENT_DESKTOP


def handler_detect(desktop):
    """Read a DE string to pick a handler for."""
    if desktop in ("mate", "cinnamon", "deepin", "xfce"):
        return desktop
    elif desktop in ("pantheon", "budgie-desktop", "gnome", "unity"):
        return "gnome"
    elif desktop in ("lxde", "lubuntu"):
        return "pcmanfm"
    elif desktop == "lxqt":
        return "pcmanfm-qt"
    else:
        return "unsupported"


def wp_set(handler, wallpaper):
    """Set a wallpaper.

    Keyword arguments:
    handler -- the wallpaper handler, determines how the wallpaper is set
    wallpaper -- the path to the wallpaper
    """
    if handler == "mate":
        subprocess.run(
            ['gsettings', 'set', 'org.mate.background',
             'picture-filename', wallpaper])
    elif handler == "gnome":
        subprocess.run(
            ['gsettings', 'set', 'org.gnome.desktop.background',
             'picture-uri', "file://" + wallpaper])
    elif handler == "cinnamon":
        subprocess.run(
            ['gsettings', 'set', 'org.cinnamon.desktop.background',
             'picture-uri', "file://" + wallpaper])
    elif handler == "deepin":
        subprocess.run(
            ['gsettings', 'set', 'com.deepin.wrap.gnome.desktop.background',
             'picture-uri', "file://" + wallpaper])
    elif handler == "xfce":
        count = subprocess.check_output(
            'xfconf-query -c xfwm4 -p /general/workspace_count',
            shell=True).decode('utf8').rstrip()
        for i in range(0, count):
            subprocess.run(
                ['xfconf-query', '-c', 'xfce4-desktop', '-p',
                 "/backdrop/screen0/monitor0/workspace" + i + "/last-image"
                 '-s', wallpaper])
    elif handler == "pcmanfm":
        subprocess.run(['pcmanfm', '--set-wallpaper', wallpaper])
    elif handler == "pcmanfm-qt":
        subprocess.run(['pcmanfm-qt', '--set-wallpaper', wallpaper])
    elif handler == "unsupported":
        pass


if not os.path.isdir(args.directory):
    if os.path.exists(args.directory):
        print("Provided wallpaper directory is not actually one")
    else:
        print("Provided wallpaper directory does not exist")
    exit(1)
print(desktop_detect())

while True:
    if args.sleep_first:
        time.sleep(args.sleep_time_global)

    wp_file = args.directory + "/" + random.choice(os.listdir(args.directory))
    print(wp_file)
    if args.wp_handler is None:
        # handler is empty, auto detect
        wp_set(handler_detect(desktop_detect()), wp_file)
    else:
        # handler has been specified
        for i in args.wp_handler:
            wp_set(i, wp_file)

    if not args.sleep_first:
        time.sleep(args.sleep_time_global)