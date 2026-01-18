class DebugTransport:
    def __init__(self, debug=True):
        self.queue = []
        self.debug = debug

    def log(self, msg):
        if self.debug:
            print(f"[TRANSPORT] {msg}")

    def send_move(self, x1, y1, x2, y2):
        self.queue.append((x1, y1, x2, y2))
        self.log(f"Send move queued: ({x1},{y1}) -> ({x2},{y2})")

    def poll(self):
        if self.queue:
            move = self.queue.pop(0)
            self.log(f"Polling move: {move}")
            return move
        return None
