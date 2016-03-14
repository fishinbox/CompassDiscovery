# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import time
import subprocess
import socket

#third party libs
from daemon import runner
from service_listener import get_server_info

class App():
    
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/agent_daemon.pid'
        self.pidfile_timeout = 5   

    def run(self):
        address, port, nics = get_server_info()
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((address, port))
        clientsocket.send(str(nics))

        while True:
            data = clientsocket.recv(64)
            if data == 'reboot':
                subprocess.call(['reboot'])
                break
            if data == '':
                time.sleep(5)
                continue


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
