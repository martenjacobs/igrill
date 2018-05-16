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

def connect_igrill(addr):
  while True:
    try:
      return IGrillV2Peripheral(addr)
    except:
      log.warn("Failed to connect, will retry")
      time.sleep(30)


if __name__ == '__main__':
 periph = connect_igrill(ADDRESS)
 last_online_status=True
 while True:
  while True:
    try:
      temperature=periph.read_temperature()
      battery=periph.read_battery()
      break
    except BTLEException as ex:
      log.warn("Failed to get values", exc_info=True)
      if last_online_status:
        last_online_status=False
        client.publish("bbq/igrill_connected", "no")
    periph = connect_igrill(ADDRESS)


  if not last_online_status:
    client.publish("bbq/igrill_connected", "yes")
    last_online_status=True

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
