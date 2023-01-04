# CM_LoRaWAN

LoRaWAN Project developed for Mobile Communications class.

Files description
main.py - Basic configuration and connection to the things network (TTN). Has a bonus feature that sends the values of a potetiometer via the TTN MQTT.

CM.txt - basic commands for a docker container and subscription to the TTN MQTT broker.

data.py - Python script that can be run in other machines to receive detailed and important information like the TTN gateway, snr, rssi, payload, consumed air time and the date and timestamp. All values are decoded.