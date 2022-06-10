from time import gmtime, strftime, localtime
import paho.mqtt.client as mqtt
import sqlite3
import ast
import sys, datetime, time
from influxdb import InfluxDBClient

readings_topic = "enviro"

dbFile = "data.db"	# for sqlite3
dbname = "enviro"	# for influxdb


# influxdb setup
host = "localhost"
port = 8086
user = "grafana"
password = "grafana"


# Allow user to set session and runno via args otherwise auto-generate
if len(sys.argv) > 1:
    if (len(sys.argv) < 3):
        print("Must define session and runNo!!")
        sys.exit()
    else:
        session = sys.argv[1]
        runNo = sys.argv[2]
else:
    session = "dev"
    now = datetime.datetime.now()
    runNo = now.strftime("%Y%m%d%H%M")

print("Session: ", session)
print("runNo: ", runNo)

# create the influxdb client
inclient = InfluxDBClient(host, port, user, password, dbname)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    print('\n')

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(readings_topic)
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Starting on_message.\n")
    theTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print(f'theTime is:  {theTime}.')

    result = (theTime + "\t" + str(msg.payload))
    print(msg.topic + ":\t" + result)

#    print(f'Message payload is type {type(msg.payload)}: {msg.payload},\n')

    message = str(msg.payload)
    message = message[2:-1]
#    print(f'Message string is type {type(message)}: {message}.\n')

    readings = eval(message)
#    print(f'Readings is {type(readings)} and: {readings}.\n')

    temperature = readings["temperature"]
    pressure = readings["pressure"]
    humidity = readings["humidity"]
    oxidised = readings["oxidised"]		# nitrogen dioxide
    reduced = readings["reduced"]		# carbon monoxide
    nh3 = readings["nh3"]			# ammonia
    lux = readings["lux"]
    serial = readings["serial"]

    writeToDb(theTime, temperature, pressure, humidity, oxidised, reduced, nh3, lux, serial)
    return




def writeToDb(theTime, temperature, pressure, humidity, oxidised, reduced, nh3, lux, serial):
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    print("Writing to db...")
    # c.execute("INSERT INTO climate VALUES (?,?,?)", (theTime, temperature, humidity))
    # changing this to reflect my longer list of values
    c.execute("INSERT INTO readings VALUES (?,?,?,?,?,?,?,?,?)", (theTime, temperature, pressure, humidity, oxidised, reduced, nh3, lux, serial))
    conn.commit()
    print('Done with sql commit.\n')

    iso = time.ctime()
    

    json_body = [
    {
        "measurement": session,
            "tags": {
                "run": runNo,
                },
            "time": iso,
            "fields": {
                "timestamp" : theTime,
                "temperature" : temperature,
                "pressure" : pressure,
                "humidity" : humidity,
                "oxidised" : oxidised,
                "reduced" : reduced,
                "nh3" : nh3,
                "lux" : lux,
                "serial" : serial 
            }
         }
     ]

    # Write JSON to InfluxDB
    print('Try to commit json_body to influx')
    inclient.write_points(json_body)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
