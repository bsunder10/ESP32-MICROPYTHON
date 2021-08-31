from time import sleep_ms, ticks_ms
from machine import I2C, Pin, ADC
from i2c_lcd import I2cLcd
from neopixel import NeoPixel
from math import ceil

# I2C LCD DISPLAY
DEFAULT_I2C_ADDR = 0x27
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

# NEOPIXEL LED
np = NeoPixel(Pin(15), 1)
np[0] = (0, 0, 0)     #Turn off the LED
np.write()

# SETUP
gas_pin = ADC(Pin(34))

lcd.putstr("YOUR TITLE")
sleep_ms(2000)
lcd.clear()

def percentage_calculation(val):
    pollution_percentage = ceil(val/41)
    oxygen_percentage = 100 - pollution_percentage
    
    return oxygen_percentage


def lcd_display(val):
    lcd.move_to(1,0)
    lcd.putstr("O2 PERCENTAGE:")
    lcd.move_to(6,1)
    lcd.putstr(str(val))
    lcd.putstr("%")
    
    
def led_color(val):
    np[0] = (100-val, val, 0)
    np.write()


while True:
    gas_value = gas_pin.read()
    
    o2_percent = percentage_calculation(gas_value)
    led_color(o2_percent)
    lcd_display(o2_percent)
    sleep_ms(500)
