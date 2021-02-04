import sys
import os
import secrets
from subprocess import Popen, PIPE
print(secrets.IO_CONNECTION_STRING)
DEFAULT_COMMAND = "rtl_433 -M utc -R 40 -C si -F json"
"""

print("Opening process")
process = Popen(DEFAULT_COMMAND.split(' '),stdout=PIPE,stderr=PIPE)


while True:

    line = process.stdout.readline()
    print("Readline")
    if not line:
        break
    print(line)

process.close()
"""