import paho.mqtt.client as mqtt
import json
import base64
from datetime import datetime


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("v3/projetocm-2022@ttn/devices/eui-70b3d549915fc504/up")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	f = open("airtime.txt","a")
	y = json.loads(msg.payload)
	try:
		gw = y["uplink_message"]["rx_metadata"][1]["gateway_ids"]["gateway_id"]
	except Exception as e:
		gw = "None"
	try:	
		snr=y["uplink_message"]["rx_metadata"][1]["snr"]
	except Exception as e:
		snr = "None"
	try:		
		rssi=y["uplink_message"]["rx_metadata"][1]["rssi"]
	except Exception as e:
		rssi = "None"
	try:	
		payload=base64.b64decode(y["uplink_message"]["frm_payload"].encode('ascii'))
	except Exception as e:
		payload = "None"
	try:
		cons_airtime=y["uplink_message"]["consumed_airtime"]
	except Exception as e:
		cons_airtime = "None"
	received = y["received_at"]
	print(received)
	datetime_object = datetime.strptime(received.split(".")[0], "%Y-%m-%dT%H:%M:%S")
	print("\nMessage received"+"\nGateway:"+str(gw)+
		"\nsnr: "+ str(snr)+
		"\nrssi: "+ str(rssi)+
		"\npayload: "+ str(payload)+
		"\nconsumed air time: \n"+ str(cons_airtime))
	f.write(str(payload)+"\t" +str(len(payload)) +"\t"+str(cons_airtime)+"\n")
	f.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("projetocm-2022@ttn", "NNSXS.QDRZLOSNBD7R27IVEAKD5OTDHSGQGVFWKZG26VQ.M42JIVQB2OXOTS2Y7IRARJJFDVXZCBZ2VODR7QC2JX6E5MT7TG5Q")
client.connect("eu1.cloud.thethings.network", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()