import sys
import os
from subprocess import Popen, PIPE

DEFAULT_COMMAND = "rtl_433 -M utc -F json"


print("Opening process")
process = Popen(DEFAULT_COMMAND.split(' '),stdout=PIPE,stderr=PIPE)


while True:

    line = process.stdout.readline()
    print("Readline")
    if not line:
        break
    print(line)

process.close()
