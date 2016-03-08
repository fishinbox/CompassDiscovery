#!/bin/sh
. ./image.conf
SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname ${SCRIPT})

# make directories
mkdir -p ${BASEDIR}/tmp/src
mkdir -p ${BASEDIR}/tmp/working 
mkdir -p ${BASEDIR}/tmp/target

# start download

get_dependencies ()
{
	app=${1}
	curl -s ${tcz_repo}${app} -o ${BASEDIR}/tmp/src/tczs/${app}
	#echo ${app} dependencies are ${app}.dep
	deplist=`curl -fs ${tcz_repo}${app}.dep 2>/dev/null`
	echo ${app} deplist is
	for depapp in $deplist; do
		echo $depapp
		get_dependencies $depapp 
	done
}


mkdir -p ${BASEDIR}/tmp/src/iso
curl -s ${release} -o ${BASEDIR}/tmp/src/iso/core.iso


mkdir -p ${BASEDIR}/tmp/src/tczs
IFS=',' read -ra DEPS <<< ${dependencies}
for i in ${DEPS[@]}; do
	get_dependencies $i
done
# start working
# iso root
mkdir -p ${BASEDIR}/tmp/src/mnt
sudo mount -o loop ${BASEDIR}/tmp/src/iso/core.iso ${BASEDIR}/tmp/src/mnt
mkdir -p ${BASEDIR}/tmp/working/iso
sudo cp -rp ${BASEDIR}/tmp/src/mnt/* ${BASEDIR}/tmp/working/iso/

# extract initfs
mkdir -p ${BASEDIR}/tmp/working/initfs-root
cd ${BASEDIR}/tmp/working/initfs-root
sudo sh -c "zcat ${BASEDIR}/tmp/working/iso/${initfs} | cpio -i -H newc -d"

echo 'doing squash'
mkdir -p ${BASEDIR}/tmp/working/
# unsquash tcz
ls ${BASEDIR}/tmp/src/tczs/
for i in $( ls ${BASEDIR}/tmp/src/tczs/ ); do
	if [ -f ${BASEDIR}/tmp/src/tczs/$i ]; then
		echo 
		echo ${BASEDIR}/tmp/src/tczs/$i
		unsquashfs -n -d ${BASEDIR}/tmp/working/squashfs-root/ -f ${BASEDIR}/tmp/src/tczs/$i
	fi
done

# TODO 2nd time extract
for i in $(find ${BASEDIR} -path ${BASEDIR}/tmp/working/squashfs-root/*.tar.gz); do
	echo $i
	tar xf $i -C ${BASEDIR}/tmp/working/squashfs-root/
done

# Copyback
sudo cp -rp ${BASEDIR}/tmp/working/squashfs-root/* ${BASEDIR}/tmp/working/initfs-root/


# rebuild initfs image
sudo sh -c "find | cpio -o -H newc | gzip -9 > ${BASEDIR}/tmp/working/iso/${initfs}"

# make ISO image
mkisofs -o ${BASEDIR}/tmp/target/core.iso ${BASEDIR}/tmp/working/iso/

# clean
sudo umount ${BASEDIR}/tmp/src/mnt
rm -r ${BASEDIR}/tmp/working


