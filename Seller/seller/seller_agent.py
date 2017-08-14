from __future__ import absolute_import, print_function
from __future__ import absolute_import

from datetime import datetime
import logging
import random
import sys
import gevent
import json
import time
from volttron.platform.vip.agent import Agent, Core, PubSub, compat
from volttron.platform.agent import utils
from volttron.platform.messaging import headers as headers_mod
from volttron.platform.vip.agent import Agent, Core, PubSub, compat
from volttron.platform.messaging.health import (STATUS_BAD,
                                                STATUS_GOOD, Status)

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
import numpy as np
import os
os.system('cls')

Sellers = ['WSU','PNNL','AVISTA']
print(Sellers)
N=len(Sellers)   # Number of Sellers

# Creating Random Bid Prices and Ramdom Bid MW Quantities
# np.random.seed(seed=0)

def seller_agent(config_path, **kwargs):
    config = utils.load_config(config_path)
    destination_vip = config.get('destination-vip')

    class Seller(Agent):
        '''
        This agent demonstrates usage of the 3.0 pubsub service as well as
        interfacting with the historian. This agent is mostly self-contained,
        but requires the histoiran be running to demonstrate the query feature.
        '''

        def __init__(self, **kwargs):
            super(Seller, self).__init__(**kwargs)


        while(True):
            def transactive(self):
                WSU_price = open('/home/rajveer-2/Desktop/volttron/data/WSU_AskingPrice.txt', 'r')
                PNNL_price = open('/home/rajveer-2/Desktop/volttron/data/WSU_AskingPrice.txt', 'r')
                AVISTA_price = open('/home/rajveer-2/Desktop/volttron/data/WSU_AskingPrice.txt', 'r')
                BidPrice = []
                BidPrice.append(WSU_price.readline())
                BidPrice.append(PNNL_price.readline())
                BidPrice.append(AVISTA_price.readline())
                BidPrice = map(float, BidPrice)
                WSU_Quant = open('/home/rajveer-2/Desktop/volttron/data/WSU_SellingAmount.txt', 'r')
                PNNL_Quant = open('/home/rajveer-2/Desktop/volttron/data/PNNL_SellingAmount.txt', 'r')
                AVISTA_Quant = open('/home/rajveer-2/Desktop/volttron/data/AVISTA_SellingAmount.txt', 'r')
                BidQuant = []
                BidQuant.append(WSU_Quant.readline())
                BidQuant.append(PNNL_Quant.readline())
                BidQuant.append(AVISTA_Quant.readline())
                BidQuant = map(float, BidQuant)
                print(BidQuant)
                print(BidPrice)
                BidQuant=np.round(np.random.randint(500,3000,len(Sellers))/1000,1)
                print(BidQuant)
                # Creating the MW that the PV requires to purchase
                ForecastValue=100;
                Qreq = np.sum(BidQuant) / 2
                print(Qreq)


                # -------------- BEGIN: Second Price auction Algorithm -----------------

                pos = np.argsort(BidPrice)
                # BidPriceSorted = BidPrice[pos]
                # BidQuantSorted = BidQuant[pos]

                Qreq_aux = Qreq
                Seller_i = 0
                Str = 'The winners are: '
                QuantBuyed = np.zeros(N)  # Results of the Auction Winners

                while Seller_i <= N and Qreq_aux > 0:  # Stack Algorithm.
                    # Taking into account the price ordered bids,
                    # If the Quantity offered by the Seller is lower thant the
                    # remaining PV required quantity, then, the energy offered by the seller
                    # is purchased (QuantBuyed vector). Remaining Quantity is updated
                    if BidQuant[Seller_i] <= Qreq_aux:
                        QuantBuyed[Seller_i] = BidQuant[Seller_i]
                        Qreq_aux = Qreq_aux - BidQuant[Seller_i]
                        Str = Str + Sellers[pos[Seller_i]] + "; "
                    elif BidQuant[Seller_i] > Qreq_aux:
                        QuantBuyed[Seller_i] = Qreq_aux
                        Str = Str + Sellers[pos[Seller_i]]
                        Qreq_aux = 0
                    Seller_i = Seller_i + 1
                    SecondPriceRes = BidPrice[min(Seller_i, N - 1)]
                # -------------- END: Second Price auction Algorithm -----------------

                # -------------- BEGIN: Showing Results  -----------------
                print('The Quantity required by the PV is: ', Qreq, " [MW]")
                print('The MW offered are: ', BidQuant, " [MW]")
                print('The bid prices are: ', BidPrice, " [USD]")
                print(Str)
                print('The Quantities buyed are: ', QuantBuyed, " [MW]")
                print('The closing price of the "Second price Auction" is: ', SecondPriceRes, " [USD]")

            # -------------- END: Showing Results  -----------------

        # @Core.receiver('onstart')
        # def setup(self, sender, **kwargs):
        #     # Demonstrate accessing a value from the config file
        #     self._agent_id = config['agentid']
        #     try:
        #         event = gevent.event.Event()
        #         agent = Agent(address=destination_vip)
        #         agent.core.onstart.connect(lambda *a, **kw: event.set(), event)
        #         gevent.spawn(agent.core.run)
        #         event.wait(timeout=10)
        #         self._target_platform = agent
        #

        #
        #     agent.vip.pubsub.subscribe(peer='pubsub', prefix='', callback=self.transactive)

        # def transactive(self, peer, sender, bus, topic, headers, message):
        #     '''
        #     Subscribes to the platform message bus on the actuator, record,
        #     datalogger, and device topics to capture data.
        #     '''
        #     if (topic == "devices/WSU/SellingAmount"):
        #         file = open('/home/rajveer-2/Desktop/volttron/data/WSU_SellingAmount.txt', 'w')
        #         file.write(str(message))
        #         print("SellingAmount", message)
        #
        #         file.close()
        #     if (topic == "devices/WSU/AskingPrice"):
        #         file = open('/home/rajveer-2/Desktop/volttron/data/WSU_AskingPrice.txt', 'w')
        #         file.write(str(message))
        #         print("sender is ", sender)
        #         _log.debug('GOT DATA FOR: {}'.format(topic))
        #         file.close()

        # Demonstrate periodic decorator and settings access


        @Core.periodic(10)
        def pub_fake_data(self):
            ''' This method publishes fake data for use by the rest of the agent.
            The format mimics the format used by VOLTTRON drivers.

            This method can be removed if you have real data to work against.
            '''

            # Create timestamp
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                headers_mod.DATE: now
            }

    return Seller(**kwargs)


def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(seller_agent)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':

    # Entry point for script
    sys.exit(main())
