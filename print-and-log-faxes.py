#!/usr/bin/env python
"""
Get inbound faxes, print them, log them.

Get outbound faxes, log them.

Author: Nick Semenkovich <semenko@alum.mit.edu>
License: MIT

This is a hackjob and could be trivially optimized (and hasn't been tested). You've been warned.
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

print("Getting inbound/outbound cache...")
try:
     pkl_file = open('.pickle-cache', 'rb')
     inbound_cache, outbound_cache = pickle.load(pkl_file)
     while len(inbound_cache) > 20:
          inbound_cache.pop()
     while len(outbound_cache) > 50:
          outbound_cache.pop()
except IOError:
     print("\tNo cache found, creating new one.")
     inbound_cache = []
     outbound_cache = []

print("Connecting to interfax.")
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

if in_result[0] != 0:
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
                    print >>sys.stderr, "Printing error, child was terminated by signal", -retcode
          else:
               print("Error downloading message %d, code: %d" % (in_item[0], dl_return_code))

     # Write the log of inbound faxes.
     t = in_item[7]
     rcv_time = "%d/%d/%d %02d:%02d" % (t[1], t[2], t[0], t[3], t[4])  # Meh, strftime lazy. 
     print >> in_log , "%s> From: %s (%s), Pages: %d, Message ID: %d\r" % (rcv_time, filter(str.isalnum, in_item[8]), filter(str.isalnum, in_item[2]), in_item[4], in_item[0])

in_log.close()

# Save the printed cache, only partially updated (outbound coming next!)
pickle.dump((inbound_cache, outbound_cache), open('.pickle-cache', 'w'))


#############
# Outbound faxes
#############

print("Getting 50 most recent outbound faxes...")
try:
     out_result = c.faxQuery( 'LT', 999999999, 50)
except socket.gaierror:
     print("Endpoint error, let's try later.")
     exit()
except socket.error:
     print("Other generic socket error. We'll try back later.")
     exit()
except TypeError:
     print("Endpoint error, returning HTML.")
     exit()

if out_result[0] != 0:
     print >> stderr, "ERROR: OUTbound return code %d" % in_result[0]
     exit()
print('\tFaxQuery returned with %d items' % (len(out_result[1])))

# Save those to our log
out_log = open('outbound_fax_log.txt', 'a')
for out_item in reversed(out_result[1]):
     if out_item[0] not in outbound_cache:
          outbound_cache.insert(0, out_item[0])

          # "\nparentTxId: %d\ntxId: %d\nsubmitTime: %s\npostponeTime: %s\ncompletionTime: %s\nuserId: %s\ncontact: %s\njobId: %s\ndestinationFax: %s\nreplyEmail: %s\nremoteCSID: %s\npagesSent: %s\nstatus: %d\nduration: %d\nsubject: %s\npagesSubmitted: %d\nsenderCSID: %s\npriority: %d\nunits: %d\ncostPerUnit: %d\npageSize: %s\npageOrientation: %s\npageResolution: %s\nrenderingQuality: %s\npageHeader: %s\nretriesToPerform: %d\ntrialsPerformed: %d" % currItem

          t = out_item[2]  # Submitted time.
          rcv_time = "%d/%d/%d %02d:%02d" % (t[1], t[2], t[0], t[3], t[4]) # Really, strftime could go here...

          status_code = int(out_item[12])
          if status_code == 0:
               status = "Ok"
          elif status_code < 0:
               status = "Sending"
          else:
               status = "ERROR! Code: %d" % (status_code)
          
          if out_item[9] == "secure-fax@aldinetravel.com" or out_item[9] == "info@aldinetravel.com":
               from_user = "(machine)"
          else:
               # Get the username.
               from_user = filter(str.isalnum, out_item[9].split('@')[0])

          print >> out_log, "%s> (%s) From: %s, To: %s, Pages: %d, Transaction: %d\r" % (rcv_time, status, from_user, filter(str.isalnum, out_item[8]), out_item[11], out_item[1])
     
          # Remove the fax.
          try:
               c.hideFax(int(out_item[1]))
          except socket.error:
               pass

out_log.close()

# Save the full cache now
pickle.dump((inbound_cache, outbound_cache), open('.pickle-cache', 'w'))
