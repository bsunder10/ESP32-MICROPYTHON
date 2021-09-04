import wifimgr
from time import sleep
import machine

try:
  import usocket as socket
except:
  import socket

led = machine.Pin(2, machine.Pin.OUT)

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D


print("ESP OK")
