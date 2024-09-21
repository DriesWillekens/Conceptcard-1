#Complete CC1 Code
#import librarys
import os
from time import sleep
import smbus
from bmp280 import BMP280
from gpiozero import MCP3008
import _thread as thread
bus=smbus.SMBus(1)

#make variables
tempdif = 0
tempBMP = 0
tempANA = 0
lastCOL = 'X'

#assign adresses, registers, ... To variables
LEDB = 0x80
LEDR = 0x40
LEDG = 0X20
MPC = 0x20
IODIRA = 0x00
GPIOA = 0x12
LM35 = MCP3008(channel=0)  # Specify channel 0

#select component, register, In/Output
bus.write_byte_data(MPC,IODIRA,0x00)

#configure BMP280 sensor
i2c = smbus.SMBus(1)
bmp280 =  BMP280(i2c_dev=i2c)



def BMP_read():
    #read temperature
    temp = bmp280.get_temperature()
    return temp

def LM35_read_Temp():
    #read temperature
    voltage = LM35.value * 3.3  # Convert value to voltage (assuming 3.3V reference)
    temp = voltage * 100  # Convert voltage to temperature in Celsius
    temp -= 2
    return temp

def read_Temp_All():
    global tempANA, tempBMP, tempdif
    while True:
        tempANA = LM35_read_Temp()
        tempBMP = BMP_read()
        tempdif = tempANA -  tempBMP
        sleep(1)


def Display():
    print(f"The temperature read by the I2C sensor: {tempBMP:.2f}°C")
    print(f"The temperature read by the analog sensor: {tempANA:.2f}°C")
    print(f"The temperature difference between the sensors: {abs(tempdif):.2f}°C")
    sleep(1)
    os.system('clear')
    
def LED():
    global lastCOL
    if abs(tempdif) < 1 and lastCOL != 'G':  
        bus.write_byte_data(MPC,GPIOA,LEDG)
        lastCOL = 'G'
    elif 1 <= abs(tempdif) < 5 and lastCOL != 'B':  
        bus.write_byte_data(MPC,GPIOA,LEDB)
        lastCOL = 'B'
    elif abs(tempdif) >= 5 and lastCOL != 'R':  
        bus.write_byte_data(MPC,GPIOA,LEDR)
        lastCOL = 'R'
    else:
        pass
    
try:
    thread.start_new_thread(read_Temp_All, ())
    while True:
        Display()
        LED()

except KeyboardInterrupt:
    bus.write_byte_data(MPC,GPIOA,0x00)				
    bus.write_byte_data(MPC,IODIRA,0x00)
    print("\nProgram stopped by user")
    sleep(1)
    os.system('clear')