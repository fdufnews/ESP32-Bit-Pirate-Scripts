#!/usr/bin/env python3
import sys
from bitpirate.bpio2 import BPIOClient, BPIOSPI


print("NOTICE: Switch ESP32 Bit Pirate to USB adapter mode before running this script:")
print("  mode USB -> adapter -> BPIO2 GPIO/SPI/I2C\n")
port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"

with BPIOClient(port, timeout=5) as client:
    spi = BPIOSPI(client)

    if not spi.configure(
        speed=1_000_000,
        clock_polarity=False,
        clock_phase=False,
        chip_select_idle=True,
        mode_bitorder_msb=True,
    ):
        raise RuntimeError("SPI configuration failed")

    data = spi.transfer([0x9F], read_bytes=3)

    if data is False or data is None:
        raise RuntimeError("JEDEC read failed")

    print("JEDEC:", " ".join("%02X" % byte for byte in data))

    client.configuration_request(mode="HiZ", mode_configuration={})
