#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Template module for modifying a PriceChartDocumentData object via
#   modifyPriceChartDocument.py.
#
##############################################################################

# For logging.
import logging

# For logging.
logLevel = logging.DEBUG
#logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

##############################################################################

def modifyPCDD(pcdd, tag):
    """Modifies the PriceChartDocumentData object's internal artifacts
    with the given tag.

    Arguments:
    pcdd - PriceChartDocumentData object that will be modified.
    tag  - str containing the tag.

    Returns:
    0 if the changes are to be saved to file.
    1 if the changes are NOT to be saved to file.
    """

    #print("okay, so the object is this: {}".format(pcdd.toString()))
    log.debug("THIS IS FROM INSIDE")
    
    return 1

        
