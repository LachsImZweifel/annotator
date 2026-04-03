from dataclasses import dataclass

@dataclass
class ImageData:
    data: bytes
    width: int
    height: int
    bytes_per_line: int
    channels: int