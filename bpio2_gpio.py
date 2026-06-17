#!/usr/bin/env python3
import sys
import time
from bitpirate.bpio2 import BPIOClient


print("NOTICE: Switch ESP32 Bit Pirate to USB adapter mode before running this script:")
print("  mode USB -> adapter -> BPIO2 GPIO/SPI/I2C\n")
port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
io = int(sys.argv[2]) if len(sys.argv) > 2 else 4
bit = 1 << io

with BPIOClient(port, timeout=3) as client:
    client.configuration_request(mode="HiZ", mode_configuration={})

    client.configuration_request(
        io_value_mask=bit,
        io_value=0,
        io_direction_mask=bit,
        io_direction=bit,
    )

    for value in (1, 0, 1, 0):
        client.configuration_request(
            io_value_mask=bit,
            io_value=bit if value else 0,
        )

        print("IO%d =" % io, value)
        time.sleep(0.5)

    client.configuration_request(
        io_direction_mask=bit,
        io_direction=0,
    )

    client.configuration_request(mode="HiZ", mode_configuration={})
