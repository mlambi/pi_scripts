#!/usr/bin/python

# this is an attempt to collect system information from mqtt
# and display it on a Pimoroni Unicorn pHAT

# the mqtt is from from digi.com

import unicornhat as uh
import paho.mqtt.client as mqtt
import json
import colorsys
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


uh.set_layout(uh.PHAT)
uh.brightness(0.4)

# initialize a list for host data
hosts_list = list()


def on_connect(client, userdata, flags, rc):
    logging.info("OnConnect:  Connected with result code {0}".format(str(rc)))
    client.subscribe("IamAlive")


def on_message(client, userdata, msg):
    logging.info("OnMessage:  Message received-> " + msg.topic + " " + str(msg.payload))

    values =  json.loads(msg.payload)
    logging.debug("OnMessage:  The converted dictionary is : " + str(values))
    logging.debug(type(values))
    hostid = (values["id"])
    hostid_type = type(hostid)
    logging.debug("OnMessage:  The hostid is: %s and the type is %s",  hostid, hostid_type)
#    hosts_list[hostid]  = (values)
    host_data = (values["id"], values["hostname"], values["cpu_temp"])

    set_color(host_data)


def set_color(host_data):
    hostId, hostname, temp = host_data
#    host_temp = int(temp[0:5]) / 1000
    host_temp = temp
    if host_temp > 70:
        host_temp = 70
    id = int(hostId)
    hue = (70 - host_temp) / 100
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
    logging.debug(f"SetColor:  {hostId} {hostname} is {host_temp}C")
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
