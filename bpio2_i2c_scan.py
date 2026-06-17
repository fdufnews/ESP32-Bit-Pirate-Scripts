#!/usr/bin/env python3
import sys
from bitpirate.bpio2 import BPIOClient, BPIOI2C


print("NOTICE: Switch ESP32 Bit Pirate to USB adapter mode before running this script:")
print("  mode USB -> adapter -> BPIO2 GPIO/SPI/I2C\n")
port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"

with BPIOClient(port, timeout=5) as client:
    i2c = BPIOI2C(client)

    if not i2c.configure(speed=100_000):
        raise RuntimeError("I2C configuration failed")

    found = []

    for address in range(0x08, 0x78):
        result = i2c.transfer(
            [address << 1],
            read_bytes=0,
        )

        if result is not False:
            found.append(address)

    print(
        "Found:",
        " ".join("0x%02X" % address for address in found) or "none",
    )

    client.configuration_request(mode="HiZ", mode_configuration={})
