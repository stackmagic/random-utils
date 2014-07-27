#!/bin/bash

# Copyright (c) 2013 Patrick Huber <stackmagic@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#
# this script increases and decreases the keyboard backlight on an asus ux32vd
# and probably other notebooks too.
#
# install xbindkeys and make sure it is started along with your desktop
#
# create a ~/.xbindkeyrc that maps the up/down keys to calling this script. in
# my case the file looks like this:
#
# "sudo /home/<YOUR_USER>/bin/keyboard-brightness.sh down"
#     m:0x0 + c:237
#     XF86KbdBrightnessDown
#
# "sudo /home/<YOUR_USER>/bin/keyboard-brightness.sh up"
#     m:0x0 + c:238
#     XF86KbdBrightnessUp
#
# and add this to your sudoers file, assuming you're in the sudo group
#
# %sudo   ALL=NOPASSWD: /home/<YOUR_USER>/bin/keyboard-brightness.sh
#

ledFile="/sys/class/leds/asus::kbd_backlight/brightness"

getBrightness () {
	cat ${ledFile}
}

setBrightness () {
	echo "new brightness: ${1}"
	echo "${1}" > ${ledFile}
}

if [ -z "${1}" ]; then
	getBrightness
else
	case "${1}" in
		up)
			setBrightness $(( $(getBrightness) + 1 ))
		;;
		down)
			setBrightness $(( $(getBrightness) - 1 ))
		;;
		*)
			setBrightness ${1}
		;;
	esac
fi

