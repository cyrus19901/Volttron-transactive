

from __future__ import absolute_import

from datetime import datetime
import logging
import random
import sys
from volttron.platform.vip.agent import Agent, Core, PubSub, compat
from volttron.platform.agent import utils
from volttron.platform.messaging import headers as headers_mod
import os
import time
import math

utils.setup_logging()
_log = logging.getLogger(__name__)
__version__ = '4.0'
os.system('cls')
Sellers = ['AVISTA']
'''
Structuring the agent this way allows us to grab config file settings 
for use in subscriptions instead of hardcoding them.
'''

def bidder_agent(config_path, **kwargs):
    config = utils.load_config(config_path)
    SellingAmount= config.get('SellingAmount',
                          'devices/AVISTA/SellingAmount')
    AskingPrice = config.get('AskingPrice',
                           'devices/AVISTA/AskingPrice')

    class Bidder(Agent):

        @Core.periodic(10)
        def pub_fake_data(self):
            Qreq =random.randrange(90, 120, 1)
            oat_reading = random.uniform(30,100)
            # lenght = len(Sellers)
            param1= .1 *Qreq
            param2 = .5 * Qreq
            # Creating the Bid Quantities for each Seller.
            BidQuant = random.triangular(param1, param2, 1)
            print "testing"
            print BidQuant
            # The bid Quantities (MWh) should be lower than the Q required by the PV.
            BidQuant = min(BidQuant, Qreq)
            print("MW offered", BidQuant)
            UtilityRate = 80  # This is the tariff or rate for the Electricity in USD/MWh.
            # This is the price that the consumer (in this auction is the seller) have to
            # pay to the Utility company, for consuming electricity.
            # Parameter of the Bid Price seller function
            AlfaValue = .4
            BidPrice = UtilityRate * (1 - 1 / math.pow(1 + BidQuant, AlfaValue))
            BidPrice = round(BidPrice, 1)
            print("Bid price", BidPrice)

            message_price = [BidPrice,{'units': '$', 'tz': 'UTC', 'type': 'float'}]
            message_quantity = [BidQuant,{'units': 'MWH', 'tz': 'UTC', 'type': 'float'}]
            #Create timestamp
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                headers_mod.DATE: now
            }

            self.vip.pubsub.publish(
                'pubsub', SellingAmount, headers, BidPrice)

            self.vip.pubsub.publish(
                'pubsub', AskingPrice, headers, BidQuant)

    return Bidder(**kwargs)
def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(bidder_agent)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
