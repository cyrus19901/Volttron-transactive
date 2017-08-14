
from __future__ import absolute_import, print_function
from __future__ import absolute_import

from datetime import datetime
import logging
import random
import sys
import gevent
import json
from volttron.platform.vip.agent import Agent, Core, PubSub, compat
from volttron.platform.agent import utils
from volttron.platform.messaging import headers as headers_mod
from volttron.platform.vip.agent import Agent, Core, PubSub, compat
from volttron.platform.messaging.health import (STATUS_BAD,
                                                STATUS_GOOD, Status)


# import numpy as np
import os
os.system('cls')

utils.setup_logging()
_log = logging.getLogger(__name__)
__version__ = '4.0'
FORWARD_TIMEOUT_KEY = 'FORWARD_TIMEOUT_KEY'
'''
Structuring the agent this way allows us to grab config file settings 
for use in subscriptions instead of hardcoding them.
'''

def subscriber_agent2(config_path, **kwargs):
    config = utils.load_config(config_path)
    destination_vip= config.get('destination-vip')



    class Subscriber(Agent):
        '''
        This agent demonstrates usage of the 3.0 pubsub service as well as 
        interfacting with the historian. This agent is mostly self-contained, 
        but requires the histoiran be running to demonstrate the query feature.
        '''
    
        def __init__(self, **kwargs):
            super(Subscriber, self).__init__(**kwargs)

        def setup(self, sender, **kwargs):
            # Demonstrate accessing a value from the config file
            self._agent_id = config['agentid']
            try:
                event = gevent.event.Event()
                agent = Agent(address=destination_vip)
                agent.core.onstart.connect(lambda *a, **kw: event.set(), event)
                gevent.spawn(agent.core.run)
                event.wait(timeout=10)
                self._target_platform = agent

            except gevent.Timeout:
                self.vip.health.set_status(
                    STATUS_BAD, "Timeout in setup of agent")
                status = Status.from_json(self.vip.health.get_status())
                self.vip.health.send_alert(FORWARD_TIMEOUT_KEY,
                                           status)
                event.wait(timeout=10)

            agent.vip.pubsub.subscribe(peer='pubsub', prefix='', callback=self.on_match)

        def on_match(self, peer, sender, bus, topic, headers, message):
            '''
            Subscribes to the platform message bus on the actuator, record,
            datalogger, and device topics to capture data.
            '''
            if (topic == "devices/PNNL/SellingAmount"):
                file = open('/home/rajveer-2/Desktop/volttron/data/PNNL_SellingAmount.txt','w')
                file.write(str(message))
                print("SellingAmount", message)

                file.close()
            if (topic == "devices/PNNL/AskingPrice"):
                file = open('/home/rajveer-2/Desktop/volttron/data/PNNL_AskingPrice.txt','w')
                file.write(str(message))
                print("sender is ", sender)
                _log.debug('GOT DATA FOR: {}'.format(topic))
                file.close()



    
        # Demonstrate periodic decorator and settings access


        @Core.periodic(10)
        def pub_fake_data(self):
            ''' This method publishes fake data for use by the rest of the agent.
            The format mimics the format used by VOLTTRON drivers.
            
            This method can be removed if you have real data to work against.
            '''
            

            #Create timestamp
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                headers_mod.DATE: now
            }

    return Subscriber(**kwargs)

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(subscriber_agent2)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
