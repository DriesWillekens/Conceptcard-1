# Import necessary libraries
import os
from time import sleep
import smbus
from bmp280 import BMP280
from gpiozero import MCP3008
import _thread as thread

# Initialize I2C bus
bus = smbus.SMBus(1)

# Initialize global variables
tempdif = 0  # temperature difference between sensors
tempBMP = 0  # temperature read by BMP280 sensor
tempANA = 0  # temperature read by LM35 analog sensor
lastCOL = 'X'  # last LED color displayed

# Assign addresses, registers, and constants to variables
LEDB = 0x80  # LED blue color
LEDR = 0x40  # LED red color
LEDG = 0X20  # LED green color
MPC = 0x20  # MCP3008 address
IODIRA = 0x00  # IODIRA register address
GPIOA = 0x12  # GPIOA register address

# Initialize LM35 analog sensor
LM35 = MCP3008(channel=0)  # Specify channel 0 for LM35

# Configure MCP3008 as output
bus.write_byte_data(MPC, IODIRA, 0x00)

# Configure BMP280 sensor
i2c = smbus.SMBus(1)
bmp280 = BMP280(i2c_dev=i2c)

# Function to read temperature from BMP280 sensor
def BMP_read():
    # Read temperature from BMP280 sensor
    temp = bmp280.get_temperature()
    return temp

# Function to read temperature from LM35 analog sensor
def LM35_read_Temp():
    # Read voltage from LM35 sensor
    voltage = LM35.value * 3.3  # Convert value to voltage (assuming 3.3V reference)
    # Convert voltage to temperature in Celsius
    temp = voltage * 100
    return temp

# Function to read temperatures from both sensors and calculate difference
def read_Temp_All():
    global tempANA, tempBMP, tempdif
    while True:
        # Read temperatures from both sensors
        tempANA = LM35_read_Temp()
        tempBMP = BMP_read()
        # Calculate temperature difference
        tempdif = tempANA - tempBMP
        sleep(1)  # Wait 1 second before next reading

# Function to display temperatures and temperature difference
def Display():
    print(f"The temperature read by the I2C sensor: {tempBMP:.2f}°C")
    print(f"The temperature read by the analog sensor: {tempANA:.2f}°C")
    print(f"The temperature difference between the sensors: {abs(tempdif):.2f}°C")
    sleep(1)  # Wait 1 second before next display
    os.system('clear')  # Clear the terminal screen

# Function to control LED based on temperature difference
def LED():
    global lastCOL
    if abs(tempdif) < 1 and lastCOL != 'G':  
        # Set LED to green if temperature difference is less than 1°C
        bus.write_byte_data(MPC, GPIOA, LEDG)
        lastCOL = 'G'
    elif 1 <= abs(tempdif) < 5 and lastCOL != 'B':  
        # Set LED to blue if temperature difference is between 1°C and 5°C
        bus.write_byte_data(MPC, GPIOA, LEDB)
        lastCOL = 'B'
    elif abs(tempdif) >= 5 and lastCOL != 'R':  
        # Set LED to red if temperature difference is 5°C or more
        bus.write_byte_data(MPC, GPIOA, LEDR)
        lastCOL = 'R'
    else:
        pass  # Do nothing if LED is already set to the correct color

try:
    # Start a new thread to read temperatures continuously
    thread.start_new_thread(read_Temp_All, ())
    while True:
        # Display temperatures and control LED
        Display()
        LED()

except KeyboardInterrupt:
    # Clean up when program is stopped by user
    bus.write_byte_data(MPC, GPIOA, 0x00)  # Turn off LED
    bus.write_byte_data(MPC, IODIRA, 0x00)  # Reset MCP3008
    print("\nProgram stopped by user")
    sleep(1)
    os.system('clear')  # Clear the terminal screen