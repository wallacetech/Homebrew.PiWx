import json
import time
from datetime import datetime
from random import uniform, randint


__version__ = '0.0.1'

class Rtl433Stub(object):

    def __init__(self):
        self._state = 56

    @staticmethod
    def _generate_rtl_msg(subtype):
        msg = dict()
        msg['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg['model'] = "Acurite-5n1"
        msg['subtype'] = subtype
        msg['id'] = 2035
        msg['channel'] = "C"
        msg['sequence_num'] = 0
        msg['battery_ok'] = 1
        msg['wind_avg_km_h'] = round(uniform(8, 10), randint(2, 3))
        if subtype == 49:
            msg['wind_dir_deg'] = round(uniform(0, 1), 3)
            msg['rain_mm'] = round(uniform(84, 85), 3)
        elif subtype == 56:
            msg['temperature_C'] = round(uniform(0, 1), 3)
            msg['humidity'] = randint(50, 75)
        msg['mic'] = "CHECKSUM"

        return json.dumps(msg)

    def get_telemtry(self):

        lines = []

        while True:
            try:
                message = self._generate_rtl_msg(self._state)
                lines.append(message)
                lines.append(message)
                lines.append(message)
                
                if self._state == 49:
                    self._state = 56
                else:
                    self._state = 49
                yield lines
                lines = []
                time.sleep(18)
            except KeyboardInterrupt:
                raise KeyboardInterrupt()

def main():
    x = Rtl433Stub()
    while True:
        lines = x.get_telemtry()
        for line in lines:
            print(line)


if __name__ == '__main__':
    main()