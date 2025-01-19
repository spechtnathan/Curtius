NAME           = "Curtius"
FREQ           = 433.1
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID        = 120 # ID of this node (BaseStation)
BASESTATION_ID = 100 # ID of the node (base station) to be contacted
PAYLOAD_FORMAT = "{NAME}, {plCounter}, {lat}, {lon}, {alt}, {tem}, {pre}, {hum}, {maxStr1}, {maxStr2}"