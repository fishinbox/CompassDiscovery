# Copyright 2016 Network Intelligence Research Center,
# Beijing University of Posts and Telecommunications
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

# standard python libs
import time
import subprocess
import socket
import requests
import json

# third party libs
from daemon import runner
import netifaces

# agent libs
from common import *


class DiscoveryAgentApp():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/tmp/agent_stdout'
        self.stderr_path = '/tmp/agent_stderr'
        self.pidfile_path =  '/tmp/agent_daemon.pid'
        self.pidfile_timeout = 5
    	self.api_server = getApiServer()

    def run(self):
        from common import Log
        while True:
            try:
                # TODO Logic change, using service info as primary and configuration file as fallback
                if self.api_server is None:
                    with open(CONF.service_info_file) as data_file:
                        d = json.load(data_file)
                        url = 'http://%s:%s/servers' % (d['host'], d['port'])
                else:
                    url = 'http://%s:80/servers' % (self.api_server)
                headers = {'Content-Type': 'application/json'}

                # submit machine information to the Compass Service
                # TODO
                r = requests.post(url, data=json.dumps(nics), headers=headers)
                # Again and again
                # wait for n Seconds
                # TODO

                #r = requests.get(url)
                #if r.text == 'reboot':
                #    subprocess.call(['reboot'])
                #    break
            except:
                pass
            finally:
                time.sleep(5)



agent = DiscoveryAgentApp()
agent_runner = runner.DaemonRunner(agent)
agent_runner.do_action()


