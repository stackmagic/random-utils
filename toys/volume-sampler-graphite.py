#!/usr/bin/python
"""Copyright 2008 Orbitz WorldWide

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

"""adapted from the graphite example-client.py"""

import sys
import time
import os
import platform
import subprocess
from socket import socket

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003

delay = 0
if len(sys.argv) > 1:
  delay = int(sys.argv[1])

volLen = 5
if len(sys.argv) > 2:
  volLen = int(sys.argv[2])

volume = 0
if len(sys.argv) > 3:
  volume = sys.argv[3]

cpumhz = 0
if len(sys.argv) > 4:
  cpumhz = sys.argv[4]

def get_loadavg():
  # For more details, "man proc" and "man uptime"
  if platform.system() == "Linux":
    return open('/proc/loadavg').read().strip().split()[:3]
  else:
    command = "uptime"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    os.waitpid(process.pid, 0)
    output = process.stdout.read().replace(',', ' ').strip().split()
    length = len(output)
    return output[length - 3:length]

sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)

now = int( time.time() )
loadavg = get_loadavg()
lines = []
lines.append("poatest.poly-dev-nb-005.loadavg_1min %s %d" % (loadavg[0],now))
lines.append("poatest.poly-dev-nb-005.loadavg_5min %s %d" % (loadavg[1],now))
lines.append("poatest.poly-dev-nb-005.loadavg_15min %s %d" % (loadavg[2],now))
lines.append("poatest.poly-dev-nb-005.office-volume_%ds %s %d" % (volLen, volume, now))
lines.append("poatest.poly-dev-nb-005.cpumhz %s %d" % (cpumhz, now))
message = '\n'.join(lines) + '\n' #all lines must end in a newline
print "sending message\n"
print '-' * 80
print message
print
sock.sendall(message)


