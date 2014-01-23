#!/usr/bin/env python
"""
Get inbound faxes, print them, log them.
Get outbound faxes, print the first page, log them.
"""

import ConfigParser
import pickle
from os import mkdir
from interfax import client
from sys import stderr

print("Getting credentials.")
config = ConfigParser.ConfigParser()
config.read('.auth')

username = config.get('interfax', 'username', 0)
password = config.get('interfax', 'password', 0)

print("Getting inbound/outbound cache...")
try:
     pkl_file = open('.pickle-cache', 'rb')
     inbound_cache = pickle.load(pkl_file)
     while len(inbound_cache) > 20:
          inbound_cache.pop()
except IOError:
     print("\tNo cache found, creating new one.")
     inbound_cache = []

print("Connecting to interfax.")
c = client.InterFaxClient(username, password)

##########
# Inbound faxes
##########

print("Getting 20 most recent inbound faxes...")
in_result = c.getList('AllMessages', 20)
if in_result[0] != 0:
     print >> stderr, "ERROR: Inbound return code %d" % in_result[0]
     exit()
print 'GetList returned with %d items' % (len(in_result[1]))

try:
     # This is all on a ram drive for security.
     mkdir("inbound")
except OSError:
     pass

# Loop over inbound faxes
for in_item in in_result[1]:
     # Sanity check
     assert(int(in_item[0]) == in_item[0])

     if in_item[0] not in inbound_cache:
          inbound_cache.insert(0, in_item[0])

          # "\nmessageId: %d\nphoneNumber: %s\nremoteCSID: %s\nmessageStatus: %d\npages: %d\nmessageSize: %d\nmessageType: %d\nreceiveTime: %s\ncallerID: %s\nmessageRecodingDuration: %d"
          dl_return_code = c.getImageChunk(in_item[0], True, in_item[5], 0, "inbound/%d.pdf" % in_item[0] )          

          if dl_return_code == 0:
               print("Printing %d" % (in_item[0]))
               ### Call *** and print
          else:
               print("Error downloading message %d, code: %d" % (in_item[0], dl_return_code))

     # Write the log of inbound faxes.
     print "\nmessageId: %d\nphoneNumber: %s\nremoteCSID: %s\nmessageStatus: %d\npages: %d\nmessageSize: %d\nmessageType: %d\nreceiveTime: %s\ncallerID: %s\nmessageRecodingDuration: %d" % in_item



#############
# Outbound faxes
#############
