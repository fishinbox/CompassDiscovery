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
	wget ${tcz_repo}${app} -O ${app}
	deplist=`wget -q -O - ${tcz_repo}${app}.dep 2>/dev/null`
	for depapp in $deplist; do
		get_dependencies $depapp 
	done
}


mkdir ${BASEDIR}/tmp/src/iso
cd ${BASEDIR}/tmp/src/iso
wget ${release} -O core.iso


mkdir ${BASEDIR}/tmp/src/tczs
cd ${BASEDIR}/tmp/src/tczs 
get_dependencies ${dependencies}

# start working
# iso root
# TODO

echo 'doing squash'
mkdir -p ${BASEDIR}/tmp/working/squashfs-root/
cd ${BASEDIR}/tmp/working/squashfs-root/
# unsquash tcz
ls ${BASEDIR}/tmp/src/tczs/
for i in $( ls ${BASEDIR}/tmp/src/tczs/ ); do
	if [ -f ${BASEDIR}/tmp/src/tczs/$i ]; then
		echo 
		echo ${BASEDIR}/tmp/src/tczs/$i
		unsquashfs -f ${BASEDIR}/tmp/src/tczs/$i
	fi
done

for i in $(find -name *.tar.gz); do
	echo $i
	tar xf $i -C ${BASEDIR}/tmp/working/squashfs-root/
done
# TODO 2nd time extract
# clean
#rm -r ${BASEDIR}/tmp


