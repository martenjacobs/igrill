import json
import time
import paho.mqtt.client as mqtt
import logging
from bluepy.btle import BTLEException

from igrill import IGrillV2Peripheral

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

ADDRESS = 'D4:81:CA:23:67:A1'
mqtt_server = "mqtt"
# DATA_FILE = '/tmp/igrill.json'
INTERVAL = 15

# MQTT Section
client = mqtt.Client()
client.connect(mqtt_server, 1883, 60)
client.loop_start()

if __name__ == '__main__':
 periph = IGrillV2Peripheral(ADDRESS)
 while True:
  bt_online=True
  while True:
    try:
      temperature=periph.read_temperature()
      battery=periph.read_battery()
    except BTLEException as ex:
      log.warn("Failed to get values", exc_info=True)
      if bt_online:
        bt_online=False
        client.publish("bbq/igrill_connected", "no")
      time.sleep(30)

  if not bt_online:
    client.publish("bbq/igrill_connected", "yes")

  # Probe 1
  if temperature[1] != 63536.0:
   client.publish("bbq/probe1", temperature[1])

  # Probe 2
  if temperature[2] != 63536.0:
   client.publish("bbq/probe2", temperature[2])

  # Probe 3
  if temperature[3] != 63536.0:
   client.publish("bbq/probe3", temperature[3])

  # Probe 4
  if temperature[4] != 63536.0:
   client.publish("bbq/probe4", temperature[4])

  client.publish("bbq/battery", battery)

  time.sleep(INTERVAL)
