#!/bin/bash

export SSH_ASKPASS=/usr/bin/ksshaskpass

for identity in `find ${HOME}/.ssh/ -type f -name "id_*" | grep -v ".pub"`; do
	if [ "`ssh-add -l | cut -d" " -f3 | grep $identity`" == "" ]; then
		ssh-add $identity
	fi
done

