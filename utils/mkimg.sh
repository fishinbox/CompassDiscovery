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
	echo app is ${app}
	curl ${tcz_repo}${app} -o ${app}
	echo app dependencies are ${tcz_repo}${app}.dep
	deplist=`curl -fs ${tcz_repo}${app}.dep 2>/dev/null`
	echo deplist is
	echo ${deplist}
	for depapp in $deplist; do
		get_dependencies $depapp 
	done
}


mkdir ${BASEDIR}/tmp/src/iso
cd ${BASEDIR}/tmp/src/iso
curl ${release} -o core.iso


mkdir ${BASEDIR}/tmp/src/tczs
cd ${BASEDIR}/tmp/src/tczs 
IFS=',' read -ra DEPS <<< ${dependencies}
for i in ${DEPS[@]}; do
	get_dependencies $i
done
# start working
# iso root
# TODO

echo 'doing squash'
mkdir -p ${BASEDIR}/tmp/working/
# unsquash tcz
ls ${BASEDIR}/tmp/src/tczs/
for i in $( ls ${BASEDIR}/tmp/src/tczs/ ); do
	if [ -f ${BASEDIR}/tmp/src/tczs/$i ]; then
		echo 
		echo ${BASEDIR}/tmp/src/tczs/$i
		unsquashfs -d ${BASEDIR}/tmp/working/squashfs-root/ -f ${BASEDIR}/tmp/src/tczs/$i
	fi
done

# TODO 2nd time extract
for i in $(find ${BASEDIR} -path ${BASEDIR}/tmp/working/squashfs-root/*.tar.gz); do
	echo $i
	tar xf $i -C ${BASEDIR}/tmp/working/squashfs-root/
done

# clean
#rm -r ${BASEDIR}/tmp


