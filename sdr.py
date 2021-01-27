import sys
import os

cmd = 'rtl_433 -M utc -F json'

process = os.popen(cmd)

while True:
    str = process.read()
    print(str)
    print("=======================")

process.close()
