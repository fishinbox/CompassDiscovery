#!/usr/bin/env python

from lxml import etree
from subprocess import Popen,PIPE


inventory = Popen(['lshw', '-xml', '-numeric'], stdout=PIPE).communicate()[0]
inventory = etree.XML(inventory)


def getProcessor(inventory):
	find_cpus = etree.XPath(".//node[@class='processor']")

	count = 0
	total_cores = 0
	total_enabledcores = 0
	total_threads = 0

	devices =[]

	for i in  find_cpus(inventory):
		if i.find('size') is not None:
			count = count + 1
			product = i.find('product').text
			# print "width: " + i.find('width').text
			cores = i.find('configuration/setting/[@id="cores"]').get('value')
			enabledcores = i.find('configuration/setting/[@id="enabledcores"]').get('value')
			threads = i.find('configuration/setting/[@id="threads"]').get('value')

			total_cores = total_cores + int(cores)
			total_enabledcores = total_enabledcores + int(enabledcores)
			total_threads = total_threads + int(threads)
			devices.append({'product':product, 'cores':cores, 'enabledcores': enabledcores, 'threads': threads})

	processor= {'count':count, 'total_cores':total_cores, 'total_enabledcores': total_enabledcores,
		'total_threads':total_threads,'devices':devices}

	return {'processor':processor}