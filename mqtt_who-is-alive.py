#!/usr/bin/python

# mqtt_who-is-alive.py
# this is an attempt to collect system information from mqtt
# and display it on a Pimoroni Unicorn pHAT

# the mqtt is from from digi.com

import unicornhat as uh
import paho.mqtt.client as mqtt
import json
import colorsys
import logging
# need to learn why other forms of importind datetime did not work
from datetime import datetime, timedelta

# logging.basicConfig(filename='who_is_alive.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

uh.set_layout(uh.PHAT)
uh.brightness(0.4)

# initialize a list for host data
# experimenting with different methods to initialize a list
# hosts_list = list()
# making it global!
global hosts_list
hosts_list = ['host1', 'host2', 'host3', 'host4', 'host5', 'host6', 'host7', 'host8']
logging.info("Hosts_list created")
for item in hosts_list:
    logging.debug(item)


def on_connect(client, userdata, flags, rc):
    logging.info("OnConnect:  Connected with result code {0}".format(str(rc)))
    client.subscribe("IamAlive")


def on_message(client, userdata, msg):
    logging.debug("OnMessage:  Message received-> " + msg.topic + " " + str(msg.payload))
    values =  json.loads(msg.payload)
    logging.debug("OnMessage:  The converted dictionary is : " + str(values))
    logging.debug(type(values))
    hostid = (values["id"])
    hostid_type = type(hostid)
    logging.debug("OnMessage:  The hostid is: %s and the type is %s",  hostid, hostid_type)
    logging.debug("onMessage:  The timestamp is:  %s", values["timestamp"])
    # this is where the msg is assigned to the list
    # the old timestamp needs to be read before now
    update_hosts_list(hostid, values)
    hosts_list[hostid]  = values
    # how to replace the above and put it in the above above
    logging.debug("OnMessage: Print hosts_list: %s", hosts_list)
    host_data = (values["timestamp"], values["id"], values["hostname"], values["cpu_temp"])
    set_color(host_data)

# this isnt finished...
# and it doesn't need anything passed in to it
# it just needs to run periodically and loop through the hosts_list to find stale hosts
# and then reset that index to the generic 'hostx' format.
# the logic is to add time to the timestamp we want to monitor
# if 
def update_hosts_list(hostid, values):
    print()
    new_timestamp = datetime.now()
    logging.info('New timestamp is: %s ', new_timestamp)
    for i in range(8):
        try:
            old_timestamp = datetime.strptime((hosts_list[i]["timestamp"]), "%Y%m%d %H:%M:%S")
            logging.info("HostIndex: %s:  old_timestamp:  %s", i, old_timestamp)
            time_diff = old_timestamp + timedelta(minutes = 1)
            if time_diff < new_timestamp:
                logging.info("time_diff + 1m is less than new_timestamp, Update hosts_list")
                hosts_list[i] = "host" + str(i)
                for x in range(4):
                    logging.info("setting pixel %s : %s", i, x)
                    uh.set_pixel(i,x,0,0,0)
                logging.info("all pixels set")
                uh.show()
            else:
                logging.info("time_diff + 1m is MORE than new_timestamp")
        except:
            logging.info("HostID %s:  no data.", i)



def set_color(host_data):
    timestamp, hostId, hostname, temp = host_data
#    host_temp = int(temp[0:5]) / 1000
    host_temp = temp
    if host_temp > 70:
        host_temp = 70
    id = int(hostId)
    hue = (70 - host_temp) / 100
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
    logging.debug(f"SetColor:  {hostId} {hostname} is {host_temp}C and {timestamp}")
    for y in range(4):
        uh.set_pixel(id, y, r, g, b)
    uh.show()

# somewhere i will need a watchdog to know
# def track_id(id):
    id = id
    logging.debug(f"Track id = {id}")



client = mqtt.Client("mqtt_iamalive_teston-BB")
client.on_connect = on_connect
client.on_message = on_message
client.connect('10.0.0.5', 1883)
client.loop_forever()
