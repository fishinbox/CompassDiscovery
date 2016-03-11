# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import time
import subprocess

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

        while True:
            #if no answer from compass server yet:
            time.sleep(10)
            #if receive reboot signal
            #subprocess.call(['reboot'])


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
