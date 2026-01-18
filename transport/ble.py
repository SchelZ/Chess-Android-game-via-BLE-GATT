from jnius import autoclass
from game.protocol import PACKET

UUID = autoclass("java.util.UUID")

SERVICE_UUID = UUID.fromString("0000BEEF-0000-1000-8000-00805F9B34FB")
CHAR_UUID = UUID.fromString("0000B001-0000-1000-8000-00805F9B34FB")


class BLETransport:
    def __init__(self):
        self.rx = []

    def send_move(self, x1, y1, x2, y2):
        # gattCharacteristic.setValue(data)
        # gatt.writeCharacteristic(gattCharacteristic)
        pass

    def on_notify(self, data):
        self.rx.append(bytes(data))

    def poll(self):
        if self.rx:
            return self.rx.pop(0)
        return None
