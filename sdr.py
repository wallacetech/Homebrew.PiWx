import sys
import os
import secrets
import time
from ProcessManager import ProcessManager

DEFAULT_COMMAND = "rtl_433 -M utc -R 40 -C si -F json"

def main():

    try:
        manager = ProcessManager()
        manager.start_process(DEFAULT_COMMAND)

        while True:
            lines = manager.get_stdout()
            for line in lines:
                for txt in line:
                    print(txt)
                    time.sleep(.1)
    except KeyboardInterrupt:
        manager.stop_process()

if __name__ == '__main__':
    main()