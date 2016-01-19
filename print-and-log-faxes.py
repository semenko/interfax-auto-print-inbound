#!/usr/bin/env python
"""
Download inbound faxes, print them, log them.

Author: Nick Semenkovich <semenko@alum.mit.edu>
License: MIT

This is a hackjob and could be trivially optimized and is barely tested. You've been warned.
"""

import ConfigParser
import pickle
import subprocess
import time
import socket
from os import mkdir
from interfax import client
from sys import stderr

print("Getting credentials.")
config = ConfigParser.ConfigParser()
config.read('.auth')

username = config.get('interfax', 'username', 0)
password = config.get('interfax', 'password', 0)

print("Getting inbound cache...")
try:
     pkl_file = open('.pickle-cache', 'rb')
     inbound_cache = pickle.load(pkl_file)
     while len(inbound_cache) > 20:
          inbound_cache.pop()
except IOError:
     print("\tNo cache found, creating new one.")
     inbound_cache = []

print("Connecting to Interfax.")
c = client.InterFaxClient(username, password)

##########
# Inbound faxes
##########

print("Getting 20 most recent inbound faxes...")

try:
     in_result = c.getList('AllMessages', 20)
except socket.gaierror:
     print("Endpoint error, let's try later.")
     exit()
except socket.error:
     print("Other generic socket error. We'll try back later.")
     exit()
except TypeError:
     print("Endpoint error, returning HTML.")
     exit()

if in_result[0] == -150:
     print("Inbound internal error. Trying back later.")
     exit()
elif in_result[0] != 0:
     print >> stderr, "ERROR: Inbound return code %d" % in_result[0]
     exit()
print('\tGetList returned with %d items' % (len(in_result[1])))

try:
     # This is all on a ram drive for security.
     mkdir("inbound")
except OSError:
     pass

# Loop over inbound faxes
in_log = open('inbound_fax_log.txt', 'a')
for in_item in reversed(in_result[1]):
     # Sanity check
     assert(int(in_item[0]) == in_item[0])

     if in_item[0] not in inbound_cache:
          inbound_cache.insert(0, in_item[0])

          # "\nmessageId: %d\nphoneNumber: %s\nremoteCSID: %s\nmessageStatus: %d\npages: %d\nmessageSize: %d\nmessageType: %d\nreceiveTime: %s\ncallerID: %s\nmessageRecodingDuration: %d"
          dl_return_code = c.getImageChunk(in_item[0], True, in_item[5], 0, "inbound/%d.pdf" % in_item[0] )          

          if dl_return_code == 0:
               print("*** Printing %d" % (in_item[0]))
               ### Call lpr and print
               retcode = subprocess.call(['lpr', '-P', 'Brother_MFC-8910DW', 'inbound/%d.pdf' % in_item[0]])
               if retcode < 0:
                    print >>stderr, "Printing error, child was terminated by signal", -retcode
          else:
               print("Error downloading message %d, code: %d" % (in_item[0], dl_return_code))

     # Write the log of inbound faxes.
     t = in_item[7]
     rcv_time = "%d/%d/%d %02d:%02d" % (t[1], t[2], t[0], t[3], t[4])  # Meh, strftime lazy. 
     print >> in_log , "%s> From: %s (%s), Pages: %d, Message ID: %d\r" % (rcv_time, filter(str.isalnum, in_item[8]), filter(str.isalnum, in_item[2]), in_item[4], in_item[0])

in_log.close()

# Save the printed cache
pickle.dump((inbound_cache), open('.pickle-cache', 'w'))
