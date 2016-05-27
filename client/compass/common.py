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

import logging
import ConfigParser
import json

from daemon import runner


logging.basicConfig(filename='/tmp/agent_%s.log' % __name__, level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')
Log = logging.getLogger(__name__)

def getApiServer():
	config = ConfigParser.RawConfigParser()
	config.read('agent.conf')
	try:
		api_server = config.get('DEFAULT','api_server')
		Log.info(api_server)
		return api_server
	except:
		Log.debug('No api_server')
		return None

class Configuration(object):
    conf = {}
    machine_info_file = '/tmp/machine_info.json'
    service_info_file = '/tmp/service_info.json'
    def Save(self):
        try:
            with open('config.json','w') as file:
                json.dump(self.conf, file)
        except:
            print('Error on Save conf')

    def Load(self):
        try:
            with open('config.json') as file:
                json.load(self.conf, file)
        except:
            print('Error on Load conf')

    def __init__(self):
        super(type(self), self).__init__()

CONF = Configuration()
