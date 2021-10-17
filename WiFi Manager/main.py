from machine import Pin
from machine import Timer
from time import sleep_ms
from esp32_ble import ESP32_BLE

ble_msg = ""


led = Pin(2, Pin.OUT)
but = Pin(0, Pin.IN)
ble = ESP32_BLE("ESP32BLE")

def buttons_irq(pin):
    led.value(not led.value())
    ble.send('LED state will be toggled.')
    print('LED state will be toggled.')   
but.irq(trigger=Pin.IRQ_FALLING, handler=buttons_irq)

while True:
    if ble_msg == 'read_LED':
        print(ble_msg)
        ble_msg = ""
        print('LED is ON.' if led.value() else 'LED is OFF')
        ble.send('LED is ON.' if led.value() else 'LED is OFF')
    
    elif ble_msg:
        print(ble_msg)
        
    sleep_ms(100)