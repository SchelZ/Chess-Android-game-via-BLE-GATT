from game.config import DEBUG
from transport.debug import DebugTransport
from transport.ble import BLETransport

def create_transport():
    if DEBUG:
        print("DEBUG MODE: Local two-player")
        return DebugTransport()
    else:
        print("BLE MODE: Phone to phone")
        return BLETransport()
