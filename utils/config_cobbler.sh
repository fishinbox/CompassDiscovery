#!/bin/bash
# TODO configure cobbler signature
# Check SELinux status
if [ $(getenforce) == 'Enforcing' ]; then
	# workaround
	sudo setenforce 0
fi

# Check cobblerd service
if [ "$(ps -ef | grep cobblerd | grep -v grep)" == '' ]; then
	sudo systemctl start cobblerd
fi

# TODO Check distro status
# TODO Check system status
# TODO Update distro
# TODO Update system

