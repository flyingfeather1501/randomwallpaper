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

# Default values
sleep_time_global = 60
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
                    default=sleep_time_global)
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

print(args.wp_handler)
