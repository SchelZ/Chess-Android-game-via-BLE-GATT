class DebugTransport:
    def __init__(self):
        self.queue = []

    def send_move(self, x1, y1, x2, y2):
        self.queue.append((x1, y1, x2, y2))

    def poll(self):
        if self.queue:
            return self.queue.pop(0)
        return None
