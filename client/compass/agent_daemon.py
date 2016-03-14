# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import time
import subprocess
import socket

#third party libs
from daemon import runner
#from service_listener import get_server_info

class App():
    
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/agent_daemon.pid'
        self.pidfile_timeout = 5   

    def run(self):
        #TODO: get_server_info and send to compass server
        address = '10.108.126.182'
        port = 8889
        nics = {'vmnet1': '00:50:56:c0:00:01', 'vmnet8': '00:50:56:c0:00:08', 'vboxnet2': '0a:00:27:00:00:02', 'vboxnet0': '0a:00:27:00:00:00', 'vboxnet1': '0a:00:27:00:00:01', 'eth0': '44:37:e6:a9:d8:30'}
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((address, port))
        clientsocket.send(str(nics))

        while True:
            data = clientsocket.recv(256)
            if data == 'reboot':
                subprocess.call(['reboot'])
                break
            if data == '':
                time.sleep(5)
                continue


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
