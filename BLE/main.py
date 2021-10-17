from machine import TouchPad, Pin
from time import sleep

t = TouchPad(Pin(4))

while True:
    print(t.read())
    sleep(0.5)