import sys
import os
import secrets
import time
from rtl433stub import Rtl433Stub
#import Packet
import json
from ProcessManager import ProcessManager
from azure.iot.device import IoTHubDeviceClient, Message

DEFAULT_COMMAND = "rtl_433 -M utc -R 40 -C si -F json"

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(secrets.IO_CONNECTION_STRING)
    return client

def Create_packet(Acurite_):
    jsonobj = json.loads(txt)                    
    pkt = dict()
    pkt['dateTime'] = jsonobj['time']
    pkt['model'] = jsonobj['model']
    pkt['id'] = jsonobj['id']
    pkt['channel'] = jsonobj['channel']
    pkt['battery'] = jsonobj['battery_ok']
    msg_type = jsonobj['subtype']

    if msg_type == 49:
        pkt['wind_speed'] = jsonobj['wind_avg_km_h']
        pkt['wind_dir'] = jsonobj['wind_dir_deg']
        pkt['rain_mm'] = jsonobj['rain_mm']
    elif msg_type == 56:
        pkt['wind_speed'] = jsonobj['wind_avg_km_h']
        pkt['temperature'] = jsonobj['temperature_C']
        pkt['humidity'] = jsonobj['humidity']

def main():

    try:
        client = iothub_client_init()
        #manager = ProcessManager()
        #manager.start_process(DEFAULT_COMMAND)
        manager = Rtl433Stub()

        while True:
            #lines = manager.get_stdout()
            lines = manager.get_telemtry()

            for line in lines:
                prevMsg = None
                for txt in line:
                    jsonobj = json.loads(txt)                    
                    pkt = dict()
                    pkt['dateTime'] = jsonobj['time']
                    pkt['model'] = jsonobj['model']
                    pkt['id'] = jsonobj['id']
                    pkt['channel'] = jsonobj['channel']
                    pkt['battery'] = jsonobj['battery_ok']
                    msg_type = jsonobj['subtype']
                    pkt['wind_speed'] = jsonobj['wind_avg_km_h']

                    if msg_type == 49:
                        pkt['wind_dir'] = jsonobj['wind_dir_deg']
                        pkt['rain_mm'] = jsonobj['rain_mm']
                    elif msg_type == 56:
                        pkt['temperature'] = jsonobj['temperature_C']
                        pkt['humidity'] = jsonobj['humidity']

                    if pkt != prevMsg:
                        prevMsg = pkt
                        message = Message(json.dumps(pkt))
                        print(message)
                        print ("Sending message...")
                        try:
                            client.send_message(message)
                        except:
                            print("Sending failed")
                        time.sleep(.1)
    except KeyboardInterrupt:
        manager.stop_process()

if __name__ == '__main__':
    main()