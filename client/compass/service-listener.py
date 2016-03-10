from six.moves import input
from zeroconf import ServiceBrowser, Zeroconf
import time
import socket 
 
class ServiceListener(object):
    service_names = []
 
    def remove_service(self, zeroconf, type, name):
        self.service_names.remove(name)
 
    def add_service(self, zeroconf, type, name):
        self.service_names.append(name)
 
 
zeroconf = Zeroconf()
listener = ServiceListener()
service_type = "_compass_discovery._tcp.local."
browser = ServiceBrowser(zeroconf, service_type, listener)

try:
    while len(listener.service_names)<=0:
        pass
    name = listener.service_names[0]
    service = zeroconf.get_service_info(service_type, name)
    print(socket.inet_ntoa(service.address))
    print(service.port)

finally:
    zeroconf.close()
    # for nicely shutdown
    time.sleep(1)
