#MCP3008 test code SPI
import os
import smbus
from time import sleep									#importeren
bus=smbus.SMBus(1)
from gpiozero import MCP3008

LM35 = MCP3008(channel=0)  # Specify channel 0

try:
    while True:
        voltage = LM35.value * 3.3  # Convert value to voltage (assuming 3.3V reference)
        temperature_celsius = voltage * 100  # Convert voltage to temperature in Celsius
        temperature_celsius -= 2
        print(f"Temperature: {temperature_celsius:.2f}°C")
        sleep(0.1)
except KeyboardInterrupt:
    print("\nProgram stopped by user")
    sleep(1)
    os.system('clear')