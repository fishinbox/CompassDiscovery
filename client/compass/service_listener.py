from six.moves import input
from zeroconf import ServiceBrowser, Zeroconf
import time
import socket 
import netifaces


class ServiceListener(object):
    service_names = []
 
    def remove_service(self, zeroconf, type, name):
        self.service_names.remove(name)
 
    def add_service(self, zeroconf, type, name):
        self.service_names.append(name)
 

def get_server_info():
    zeroconf = Zeroconf()
    listener = ServiceListener()
    service_type = "_compass_discovery._tcp.local."
    browser = ServiceBrowser(zeroconf, service_type, listener)

    try:
        while len(listener.service_names)<=0:
            pass
        name = listener.service_names[0]
        service = zeroconf.get_service_info(service_type, name)
        address = socket.inet_ntoa(service.address)
        port = service.port
        # get net iface info
        ifaces = netifaces.interfaces()
        nics= {}
        for iface in ifaces:
            if iface.startswith('lo'):
                continue
            MAC = netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr']
            nics[iface]=MAC
        return (address, port, nics)
    finally:
        zeroconf.close()
        # for nicely shutdown
        time.sleep(1)

