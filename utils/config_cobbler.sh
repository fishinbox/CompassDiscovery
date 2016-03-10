#!/bin/bash
source path.rc
DistroName=test_core
DistroArch=x86_64
ISO=$(readlink -f $1)

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

# Check distro status
if [ "$(sudo cobbler distro find --name=${DistroName}-${DistroArch})" != "" ]; then
	if [ "$(sudo cobbler distro find --name=${DistroName}-${DistroArch}.orig)" != "" ]; then
		sudo cobbler distro remove --name=${DistroName}-${DistroArch}.orig
	fi
	if [ "$(sudo cobbler profile find --name=${DistroName}-${DistroArch}.orig)" != "" ]; then
		sudo cobbler profile remove --name=${DistroName}-${DistroArch}.orig
	fi
	sudo cobbler distro rename \
		--name=${DistroName}-${DistroArch} \
		--newname=${DistroName}-${DistroArch}.orig
	sudo cobbler profile rename \
		--name=${DistroName}-${DistroArch} \
		--newname=${DistroName}-${DistroArch}.orig
fi

# import new distro
mkdir -p ${BASEDIR}/tmp/working/mnt
sudo mount -o loop $ISO ${BASEDIR}/tmp/working/mnt
sudo cobbler import --name=${DistroName} --arch=${DistroArch} --path=${BASEDIR}/tmp/working/mnt
sudo umount ${BASEDIR}/tmp/working/mnt
#rm -r ${BASEDIR}/tmp/working

# Check system status
if [ "$(sudo cobbler system find --name=default)" == "" ]; then
	sudo cobbler system create --name=default
fi

# Update system
sudo cobbler system edit --name=default --profile=${DistroName}-${DistroArch}

# Sync
sudo cobbler sync
