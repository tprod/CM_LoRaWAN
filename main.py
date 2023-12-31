from network import LoRa
import socket
import time
import ubinascii
import struct
import machine
# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

print("DevEUI: " + ubinascii.hexlify(lora.mac()).decode('utf-8').upper())

# create an OTAA authentication parameters

app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('B9EC25063B907B9488501A12BBBD7738')

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

while not lora.has_joined():
    print('Not yet joined...')
    time.sleep(3)

print("Joined network")

# create socket to be used for LoRa communication
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# configure data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
for i in range (242):
    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)

    # send some data
    adc= machine.ADC()
    apin= adc.channel(pin='P13', attn=adc.ATTN_11DB)
    val = apin()
    print(val)

    str_val = str(val)
    l = ["A"]*i
    str_val = "".join([str(item) for item in l])
    #print(str_val)
    #print(str_val.encode())
    print("len" + str(len(str_val)))
    print("bytes size" + str(len(str_val.encode())))
    s.send(str_val.encode())

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    #get any data received (if any...)
    data = s.recv(64)
    print(data)
    time.sleep(5)
