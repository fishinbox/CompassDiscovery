#!/bin/bash
# Copyright 2016 Network Intelligence Research Center, 
# Beijing University of Posts and Telecommunications
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

. ./image.conf
iso_file=$(readlink -f $1)
ini_file=$(readlink -f $2)

REBASEDIR=/tmp/compass_discovery_agent/repackage
MNTDIR=${REBASEDIR}/mnt
WORKDIR=${REBASEDIR}/working
TARGETDIR=${REBASEDIR}/target

mkdir -p ${MNTDIR}
mkdir -p ${WORKDIR}
mkdir -p ${TARGETDIR}

sudo mount -o loop,ro $iso_file ${MNTDIR}

sudo cp -rp ${MNTDIR} ${WORKDIR}/iso

# Extract initfs
mkdir -p ${WORKDIR}/initfs-root
cd ${WORKDIR}/initfs-root

sudo umount ${MNTDIR}
sudo sh -c "zcat ${WORKDIR}/iso/${initfs} | cpio -i -H newc -d"

# Copy INI File
sudo cp ${ini_file} ${WORKDIR}/initfs-root/opt/compass/agent.conf

# rebuild initfs image
sudo sh -c "find | cpio -o -H newc | gzip -9 > ${WORKDIR}/iso/${initfs}"

# make ISO image
sudo mkisofs -l -J -r \
-no-emul-boot \
-boot-load-size 4 \
-boot-info-table \
-b boot/isolinux/isolinux.bin \
-c boot/isolinux/boot.cat \
-o ${TARGETDIR}/core.iso ${WORKDIR}/iso/

