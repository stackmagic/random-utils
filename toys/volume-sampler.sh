#!/bin/bash

# Copyright (c) 2012 Patrick Huber <stackmagic@gmail.com>
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

# sample the volume over a period of time, then calculate the mean of the
# values.

dur=5
if [ -n "$1" ]; then
	dur=$1
fi

LANG="en_US.UTF-8"

# copied and adapted from here:
# http://forums.whirlpool.net.au/archive/1853993
function sample() {
	arecord -c2 -d${dur} -fS16_LE /dev/null -vvv 2>&1 | grep --line-buffered "Max peak" | awk -W interactive '{print $7}' | cut -d% -f1 | paste -sd " "
}

# copied and adapted from here:
# http://www.onli-blogging.de/index.php?/1083/Statistik-mit-Bash.html
function calc_mean() {
	sum=0
	n="$#"

	while [[ "$#" -gt 0 ]];do
		value="$1"
		sum=$(echo "$sum + $value" | bc -l)
		shift
	done
	echo "$sum / $n" | bc -l
}

vals=$(sample)
mean=$(calc_mean $vals)
echo "${mean}"

