#BMP_280 i2c test code
#Select librarys
import os
from time import sleep
import smbus
from bmp280 import BMP280

#configure sensor
i2c = smbus.SMBus(1)
bmp280 =  BMP280(i2c_dev=i2c)

try:
    while True:
        os.system('clear')
        temperature = bmp280.get_temperature()
        pressure = bmp280.get_pressure()
        print(f"{temperature:05.2f}*C")
        sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped by user")
    sleep(1)
    os.system('clear')