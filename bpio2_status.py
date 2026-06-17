#!/usr/bin/env python3
import sys
from bitpirate.bpio2 import BPIOClient


print("NOTICE: Switch ESP32 Bit Pirate to USB adapter mode before running this script:")
print("  mode USB -> adapter -> BPIO2 GPIO/SPI/I2C\n")
port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"

with BPIOClient(port, timeout=3) as client:
    status = client.status_request()

    if status is None:
        raise RuntimeError("No BPIO2 response")

    print("Mode:", status["mode_current"])
    print("Pins:")

    for pin in status["mode_pin_labels"]:
        print(" ", pin)

    print("Max packet:", status["mode_max_packet_size"])
    print("Max write:", status["mode_max_write"])
    print("Max read:", status["mode_max_read"])
