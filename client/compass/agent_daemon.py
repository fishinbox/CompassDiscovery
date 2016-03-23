# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import time
import subprocess
import socket
import requests

#third party libs
from daemon import runner
from service_listener import get_server_info

class App():
    
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path =  '/tmp/agent_daemon.pid'
        self.pidfile_timeout = 5   

    def run(self):
        address, port, nics = get_server_info()
        url = 'http://'+address+':5000/servers'
        r = requests.post(url, data=nics)

        while True:
            r = requests.get(url)
            if r.text == 'reboot':
                subprocess.call(['reboot'])
                break
            else:
                time.sleep(5)
                continue


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
