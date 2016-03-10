#!/bin/sh
# put other system startup commands here
for i in $(find /opt/py -path *.tar.gz); do
	cd /tmp
	tar xf $i
	cd /tmp/$(basename $i .tar.gz)
	sudo python setup.py install
done
