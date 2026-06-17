#!/usr/bin/env python3
import sys
from bitpirate.bpio2 import BPIOClient, BPIOSPI


print("NOTICE: Switch ESP32 Bit Pirate to USB adapter mode before running this script:")
print("  mode USB -> adapter -> BPIO2 GPIO/SPI/I2C\n")
port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
address = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0
length = int(sys.argv[3], 0) if len(sys.argv) > 3 else 256

with BPIOClient(port, timeout=10) as client:
    spi = BPIOSPI(client)

    if not spi.configure(
        speed=1_000_000,
        chip_select_idle=True,
    ):
        raise RuntimeError("SPI configuration failed")

    command = [
        0x03,
        (address >> 16) & 0xFF,
        (address >> 8) & 0xFF,
        address & 0xFF,
    ]

    data = spi.transfer(command, read_bytes=length)

    if data is False or data is None:
        raise RuntimeError("SPI read failed")

    for offset in range(0, len(data), 16):
        line = data[offset:offset + 16]

        print(
            "%06X:" % (address + offset),
            " ".join("%02X" % byte for byte in line),
        )

    client.configuration_request(mode="HiZ", mode_configuration={})
