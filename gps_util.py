# Parse NMEA packets from a UBlox M10 GPS module hooked up to a Bit Pirate.

from bitpirate import BitPirateWifi
import time
import os
import pynmea2 # pip install pynmea2
from uart_connect_helper import connect_uart
# Connect to the Bit Pirate
bp = BitPirateWifi("192.168.0.57")
bp.start()

connect_uart(bp, tx_pin=43, rx_pin=44, baudrate=115200, bits=8, parity="N", stop=1, inverted=False)

# Start UART read mode
bp.send("read")
bp.wait()
bp.clear_echoes(2)
print("GPS from UART started")

try:
    while True:
        lines = bp.receive(skip=0)
        if lines:
            for line in lines:
                try:
                    msg = pynmea2.parse(line + "\n")
                    print(repr(msg))
                except pynmea2.ParseError as e:
                    pass
except KeyboardInterrupt:
    print("\nStopping GPS read...")
finally:
    # Close the connection
    bp.stop()
