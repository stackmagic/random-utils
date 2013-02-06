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

# Cleanup my git settings. Since I always check out my repos with a prefixed
# name that correlates to a source like github, codebase etc we can set the
# name and email or other local config very easily.

setGitConfig () {
	[ $# -lt 4 ] && return 1;
	name=$1
	email=$2
	for dir in "${@:3}"; do
		cd $dir
		echo ">>> $dir"
		git config user.name "$1"
		echo "    $(git config user.name)"
		git config user.email "$2"
		echo "    $(git config user.email)"
		echo ""
		cd - >/dev/null
	done
}

setGitConfig "Patrick Huber" "stackmagic@gmail.com"  gh-*
