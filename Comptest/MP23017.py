#MPC23017 SPI test code
#Select librarys
import smbus
from time import sleep									#importeren
bus=smbus.SMBus(1)

#assign adresses, registers, ... To variables
MPC = 0x20
IODIRA = 0x00
GPIOA = 0x12

#select component, register, In/Output
bus.write_byte_data(MPC,IODIRA,0x00)

try:
    while True:
        bus.write_byte_data(MPC,GPIOA,0b10000000)
        sleep(1)
        bus.write_byte_data(MPC,GPIOA,0b00000000)
        sleep(1)

except KeyboardInterrupt:
    bus.write_byte_data(MPC,GPIOA,0x00)				#alle pinnen laag maken
    bus.write_byte_data(MPC,IODIRA,0x00)