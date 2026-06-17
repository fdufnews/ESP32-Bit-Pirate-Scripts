# 
# Glitch all I2C devices on the bus
#

from bitpirate import BitPirate
from bitpirate import Helper

# Search and connect to the Bit Pirate
bp = BitPirate.auto_connect()

# Initialize the Bit Pirate
bp.start()

# Change to I2C mode
bp.change_mode("I2C")

# Scan I2C bus and get results
print("Scanning I2C bus, it may take few seconds...")
bp.send("scan")
bp.wait(2)
results = bp.receive(skip=2) # Skip the first two lines (echo and header)

# Extract addresses from results
addr_list = Helper.extractHexFromList(results)
print("Found addresses: ", addr_list)

# Glitch each address
for addr in addr_list:
    bp.send(f"glitch {addr}")
    bp.wait()
    print(f"Sent glitch to {addr}, it may take few seconds...")
    response = bp.receive_all(2)
    for line in response:
        print(" - " + line)

    bp.wait()
    bp.clear_echoes()

# Clean up the serial connection
bp.stop()
