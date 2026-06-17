from bitpirate import BitPirate
from bitpirate import BitPirateWifi

# Small helper to connect to a UART port on the Bit Pirate.
def connect_uart(bp: BitPirate | BitPirateWifi, rx_pin: int, tx_pin: int,
    baudrate: int = 115200, bits = 8, parity = "N", stop = 1, inverted: bool = False):
    bp.send("mode uart")
    received = bp.receive()
    if "Mode changed to UART" in received:
        bp.send("config")
    bp.send(f"{rx_pin}\n")
    bp.send(f"{tx_pin}\n")
    bp.send(f"{baudrate}\n")
    bp.send(f"{bits}\n")
    bp.send(f"{parity}\n")
    bp.send(f"{stop}\n")
    if inverted:
        bp.send("y\n")
    else:
        bp.send("n\n")
        
    bp.wait()
    print(bp.receive())

if __name__ == "__main__":
    # Connect to the Bit Pirate
    bp = BitPirateWifi("192.168.0.57")
    bp.start()
    connect_uart(bp, 43, 44, 57600, 8, "N", 1, False)