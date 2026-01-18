from dataclasses import dataclass

@dataclass(frozen=True)
class PacketType:
    MOVE: int = 0x01
    JOIN: int = 0x02
    LEAVE: int = 0x03
    SYNC_REQ: int = 0x04
    SYNC_BOARD: int = 0x05


PACKET = PacketType()


def encode_move(fx, fy, tx, ty):
    return bytes((
        ((fx & 0xF) << 4) | (fy & 0xF),
        ((tx & 0xF) << 4) | (ty & 0xF),
    ))


def decode_move(data: bytes):
    b1, b2 = data
    return (
        (b1 >> 4) & 0xF,
        b1 & 0xF,
        (b2 >> 4) & 0xF,
        b2 & 0xF,
    )
