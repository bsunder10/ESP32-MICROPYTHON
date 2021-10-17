from machine import Pin, Timer, SoftI2C
from time import sleep_ms
import ubluetooth
import json
import os
import neopixel

no_led = 24
np = neopixel.NeoPixel(Pin(15), no_led)

def led_off_all():
    for i in range(no_led):
        np[i] = (0, 0, 0)
    np.write()
        
def led_on(r, g, b, leds):
    if int(prev_led) > int(leds):
        led_off_all()
    for i in range(int(leds)):
        
        np[i] = (int(r), int(g), int(b))
        np[i+12] = (int(r), int(g), int(b))
        np.write()

def write_file(title, txt):
    update = False
    with open("data.json", 'r+') as file:
        data = json.load(file)
        if title == "wifi":
            if txt not in data[wifi_cred]:
                data[wifi_cred].append(txt)
                os.remove("data.json")
                update = True
                
        elif title == "name":
            if txt != data['name']:
                data["name"] = txt
                os.remove("data.json")
                update = True
                
        elif title == "value":
            data["values"]["r"] = txt[0]
            data["values"]["g"] = txt[1]
            data["values"]["b"] = txt[2]
            data["values"]["leds"] = txt[3]
            os.remove("data.json")
            update = True
        
        if update == True:
            with open("data.json", 'w') as file:
                print(data)
                json.dump(data, file)
        else:
            print("Data duplicate")

    file.close()




class BLE():
    def __init__(self, name):   
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)

        self.led = Pin(2, Pin.OUT)
        
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()


    def ble_irq(self, event, data):
        if event == 1:
            '''Central disconnected'''
            self.led(1)
        
        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
        
        elif event == 3:
            global message_rx, message_wifi
            '''New message received'''            
            buffer_rx = self.ble.gatts_read(self.rx)
            message_rx = buffer_rx.decode('UTF-8').strip()
            #print(message_rx)            
            
            buffer_wifi = self.ble.gatts_read(self.wifi)
            message_wifi = buffer_wifi.decode('UTF-8').strip()
            #print('buffer_wifi: ', buffer_wifi) 
            
    def register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        WIFI_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400004-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
        BLE_WIFI = (ubluetooth.UUID(WIFI_UUID), ubluetooth.FLAG_WRITE)    
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX, BLE_WIFI))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx, self.wifi), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)
        print("Advertising: ", name)
        
        
# test
led_off_all()
prev_led = 24

with open("data.json", "r") as file:
    data = json.load(file)
    val = data["values"]
    led_on(val["r"], val["g"], val["b"], val["leds"])
    print(data)

print(data["name"])
ble = BLE(data["name"])
message_rx, message_wifi = "", ""




while True:
    if message_rx:
        print(message_rx)
        splitted_msg = message_rx.split(',')
        if len(splitted_msg) == 4:
            r, g, b, leds = splitted_msg
            led_on(r, g, b, leds)
            write_file("value", splitted_msg)
            prev_led = leds
        
        elif len(splitted_msg) == 2:
            task, data = splitted_msg
            write_file(task, data)

        message_rx = ""
        
    if message_wifi:
        print("message_wifi:", message_wifi)
        ssid, password = message_wifi.split(',')
        print("ssid: ", ssid, ", password: ", password)
        
        #save_wifi_password(message_wifi)
        message_wifi = ""