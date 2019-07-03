'''
This program is created by Andrew Li for requiring the prices (live or open)

There are three inputs including:

    1. pathTicker: The path to store the tickers to download the prices
    2. openPricePath: The path to save the .csv file
    3. priceType: 'Live' or 'Open' (Live: current price and Open: today's open price)

The file is lastly modified on 2019/01/13
'''

from ibClass import *
from CheckSlippage import *
#########################################
# Modify the details here
#########################################

# Personal Account
Account = 'U9853025'

# The directory to store the execution report
pathOda = '/Users/andrew/Desktop/HKUST/Projects/IB/Test_1101/Input/SampleOrder2.csv'
pathLivePrice = '~/Desktop/LivePrice.csv'
priceType = 'Live'
#########################################

def main():
    SetupLogger()
    logging.debug("now is %s", datetime.datetime.now())
    logging.getLogger().setLevel(logging.INFO)

    # enable logging when member vars are assigned
    from ibapi import utils
    from ibapi.order import Order
    Order.__setattr__ = utils.setattr_log
    from ibapi.contract import Contract, DeltaNeutralContract
    Contract.__setattr__ = utils.setattr_log
    DeltaNeutralContract.__setattr__ = utils.setattr_log
    from ibapi.tag_value import TagValue
    TagValue.__setattr__ = utils.setattr_log
    TimeCondition.__setattr__ = utils.setattr_log
    ExecutionCondition.__setattr__ = utils.setattr_log
    MarginCondition.__setattr__ = utils.setattr_log
    PriceCondition.__setattr__ = utils.setattr_log
    PercentChangeCondition.__setattr__ = utils.setattr_log
    VolumeCondition.__setattr__ = utils.setattr_log

    cmdLineParser = argparse.ArgumentParser("api tests")
    # cmdLineParser.add_option("-c", action="store_True", dest="use_cache", default = False, help = "use the cache")
    # cmdLineParser.add_option("-f", action="store", type="string", dest="file", default="", help="the input file")
    cmdLineParser.add_argument("-p", "--port", action="store", type=int,
                               dest="port", default=7496, help="The TCP port to use")
    cmdLineParser.add_argument("-C", "--global-cancel", action="store_true",
                               dest="global_cancel", default=False,
                               help="whether to trigger a globalCancel req")
    args = cmdLineParser.parse_args()
    print("Using args", args)
    logging.debug("Using args %s", args)

    try:
        app = TestApp(action='LIVEPRICE', account=Account, openPricePath=pathLivePrice, tickerFile=pathOda, priceType=priceType)
        if args.global_cancel:
            app.globalCancelOnly = True

        app.connect("127.0.0.1", args.port, clientId=999)
        # ! [connect]
        print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                      app.twsConnectionTime()))
        app.run()
        app.disconnect()





    except:
        raise
    finally:
        app.dumpTestCoverageSituation()
        app.dumpReqAnsErrSituation()

if __name__ == "__main__":
    main()